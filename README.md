# mumo-sports
Mumo module for Mumble 1.5+ that delivers live, hyperlinked sports scores and schedules for major leagues directly to text chat channels.

✨ Features

* **No API Key Required:** Uses ESPN's public scoreboard endpoints—no developer accounts, registration tokens, or configurations needed.
* **Smart URL Routing:** Automatically maps teams and matches to clean, user-facing ESPN links, utilizing custom routing overrides for complex soccer and college football layouts.
* **Fault-Tolerant Parsing:** Built using defensive nested key lookups (`.get()`) to safely handle pre-game states, postponements, doubleheaders, or unexpected payload changes without crashing the background thread.
* **Mumble-Optimized Layouts:** Keeps chat feeds clean by limiting outputs to a maximum of 6 concurrent games and formatting text payloads into clean HTML fragments.
* **Zero Heavy Dependencies:** Written entirely using native Python 3 libraries (`urllib.request`, `json`, `re`).

---

🏀 Supported Leagues


| `!scores nfl` | NFL Football  

| `!scores nba` | NBA Basketball

| `!scores mlb` | MLB Baseball

| `!scores nhl` | NHL Hockey 

| `!scores cfb` | College Football 

| `!scores wc` | FIFA World Cup


*Note: Executing `!scores` without arguments defaults automatically to the NFL scoreboard.*


Example Command: !scores mlb

Output:

   🏆 Live MLB Scoreboard:
   
    • Marlins vs Phillies (6/15 - 6:40 PM EDT)
    • Royals 4 @ Nationals 2 (Final)
    • Twins vs Rangers (6/15 - 8:05 PM EDT)
    
---

🛠️ Installation

### 1. Save the Module
Copy `sports.py` into your primary Mumo `modules/` directory.

### 2. Enable the Module
Depending on how your Mumo environment is configured, choose one of the methods below:

#### Method A: If your setup uses a single mumo.ini file
Open your `mumo.ini` file and add `sports` to your active modules list, then append the configuration at the bottom:
[modules]
sports =

[sports]
enabled = true

Method B: If your setup uses a modules-enabled/ directory

Create a new file called sports.ini inside your modules-enabled/ folder:
[sports]
enabled = true

3. Restart Mumo

Restart your Mumo bot framework instance to load the new extension.

⚙️ Compatibility

    Works natively with Mumble 1.4.x / 1.5.x+ server deployments.

    Written using the standardized mumo_module namespace layer.

    Mumo Required: https://github.com/mumble-voip/mumo

📄 License

This project is open-source and available under the terms of the 3-Clause BSD License. See the header of sports.py for full details.
