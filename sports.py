#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2026 KizCo (https://github.com/KizCo)
# Licensed under the 3-Clause BSD License.
# 
# This software is provided "as is", without warranty of any kind.
# Redistribution and use in source/binary forms are permitted provided
# that all original copyright notices and disclaimers are retained.
#
# sports.py
# Sports score fetcher module for Mumo 
#

import re
import json
import urllib.request
from datetime import datetime
from mumo_module import MumoModule

class sports(MumoModule):
    default_config = {'sports': ()}

    def __init__(self, name, manager, configuration=None):
        MumoModule.__init__(self, name, manager, configuration)
        self.murmur = manager.getMurmurModule()
        self.keyword = "!scores"

    def connected(self):
        manager = self.manager()
        self.log().debug("Registering Live Sports Scores module")
        manager.subscribeServerCallbacks(self, manager.SERVERS_ALL)

    def disconnected(self):
        pass

    def sendMessage(self, server, user, message, msg):
        if message.channels:
            server.sendMessageChannel(user.channel, False, msg)
        else:
            server.sendMessage(user.session, msg)

    def userTextMessage(self, server, user, message, current=None):
        clean_text = re.sub(r'<[^>]*>', ' ', message.text).strip().lower()

        if clean_text.startswith(self.keyword):
            args = clean_text[len(self.keyword):].strip().split()
            league = args[0] if args else "nfl"
            
            # Map input arguments to ESPN's internal JSON API endpoints
            league_map = {
                "nfl": ("football", "nfl"),
                "nba": ("basketball", "nba"),
                "mlb": ("baseball", "mlb"),
                "nhl": ("hockey", "nhl"),
                "cfb": ("football", "college-football"),
                "wc":  ("soccer", "fifa.world")
            }

            if league not in league_map:
                self.sendMessage(server, user, message, "❌ <b>Valid leagues:</b> !scores nfl, nba, mlb, nhl, cfb, wc")
                return

            sport_type, league_name = league_map[league]
            espn_url = f"https://site.api.espn.com/apis/site/v2/sports/{sport_type}/{league_name}/scoreboard"
            
            # College Football optimization: pass groups=80 to return all FBS matchups instead of just Top 25
            if league == "cfb":
                espn_url += "?groups=80"

            try:
                req = urllib.request.Request(espn_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req, timeout=7) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    events = data.get('events', [])
                    if not events:
                        self.sendMessage(server, user, message, f"🏈 No active games scheduled today for **{league.upper()}**.")
                        return

                    # Format header display name smoothly
                    display_header = "World Cup" if league == "wc" else league.upper()
                    output_lines = [f"🏆 <b>Live {display_header} Scoreboard:</b>"]
                    
                    for event in events[:6]:
                        # Safeguard data structures
                        game_id = event.get('id', '')
                        status_obj = event.get('status', {}).get('type', {})
                        state = status_obj.get('state', 'pre')
                        short_status = status_obj.get('shortDetail', 'TBD')
                        
                        competitions = event.get('competitions', [])
                        if not competitions:
                            continue
                            
                        competitors = competitions[0].get('competitors', [])
                        if len(competitors) < 2:
                            continue
                        
                        home_team = next((c for c in competitors if c.get('side') == 'home'), competitors[0])
                        away_team = next((c for c in competitors if c.get('side') == 'away'), competitors[1])
                        
                        home_name = home_team.get('team', {}).get('shortDisplayName', 'Home')
                        away_name = away_team.get('team', {}).get('shortDisplayName', 'Away')
                        
                        home_score = home_team.get('score', '0')
                        away_score = away_team.get('score', '0')

                        # Formulate the game layout line based on current status
                        if "pre" in state:
                            game_text = f"{away_name} vs {home_name} ({short_status})"
                        else:
                            game_text = f"<b>{away_name}</b> {away_score} @ <b>{home_name}</b> {home_score} ({short_status})"

                        # Wrap the display text with an absolute web link anchor to the ESPN Boxscore/Match page
                        if game_id:
                            # Soccer / World cup links use /soccer/match/_/gameId/######/match
                            if league == "wc":
                                boxscore_url = f"https://www.espn.com/soccer/match/_/gameId/{game_id}/match"
                            else:
                                # Standard boxscore layout for NFL, NBA, MLB, NHL, CFB
                                web_slug = league_name
                                if league == "cfb":
                                    web_slug = "college-football"
                                boxscore_url = f"https://www.espn.com/{web_slug}/boxscore/_/gameId/{game_id}"
                                
                            output_lines.append(f"• <a href='{boxscore_url}'>{game_text}</a>")
                        else:
                            output_lines.append(f"• {game_text}")

                    self.sendMessage(server, user, message, "<br>".join(output_lines))

            except Exception as e:
                import traceback
                self.log().error(f"Sports bot API error: {str(e)}")
                self.log().error(traceback.format_exc())
                self.sendMessage(server, user, message, "⚠️ <b>Error:</b> Unable to fetch scores from data engine.")

    def userConnected(self, server, state, context=None): pass
    def userDisconnected(self, server, state, context=None): pass
    def userStateChanged(self, server, state, context=None): pass
    def channelCreated(self, server, state, context=None): pass
    def channelRemoved(self, server, state, context=None): pass
    def channelStateChanged(self, server, state, context=None): pass
