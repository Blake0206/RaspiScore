# Displays scores from ESPN onto an LED matrix
Currently everything is being ran on an emulator using [RGBMatrixEmulator](https://github.com/ty-porter/RGBMatrixEmulator) \
Information is gathered from ESPN using the [espn_scraper](https://github.com/andr3w321/espn_scraper)


## Install
Clone the repository using `git clone https://github.com/Blake0206/RaspiScore.git` \
From the `RaspiScore` folder, run `pip install -r requirements.txt` to install the required packages


## Run
Run the main program by using `python3 main.py` \
By default, the emulator will run on [http://localhost:8888](http://localhost:8888)

*Any errors and additional information will be displayed in the terminal*


## Main Configuration
*Configuration is done within `main_config.json`*

### Leagues
`displayed_leagues` - sports leagues that are displayed, accepts list containing "mlb", "nba", "nfl", "ncaaf", "ncaam", "ncaaw", "wnba", "nhl" \
`league_display_time` - time in seconds that the league logo is displayed, positive integers are accepted \
`league_logo_size` - size in pixels of the league logo displayed before events/news, positive integers are accepted

### Events
`event_display_time` - time in seconds that each event is display, positive integers are accepted \
`team_logo_size` - size in pixels of the team logo displayed for events, positive integers are accepted \
`team_logo_offset` - negative offset in pixels from the left/right edges for the team logos, positive and negative integers are accepted \
`team_logo_mirrored` - mirrors the logo on the right if set to true, booleans are accepted \
`team_logo_opacity` - opacity of the team logo, positive floats less than 5 are accepted \
`score_offset` - offset in pixels from the left/right edges for the scores, positive integers are accepted

### News
`source` - source of news data, accepted string of "espn" or "fox" \
`news_display_time` - time in seconds that each news headline is displayed, positive integers are accepted \
`display_source_logo` - enables/disables the news source logo displayed behind text, booleans are accepted \
`source_logo_opacity` - opacity of the news source logo, positive floats less than 5 are accepted

### Other
`first_display` - first information that is displayed, accepted string of "leagues" or "news" \
`time_correction` - hour difference from EST, positive and negative integers are accepted \
`text_color` - color of the text, list of RGB values \
`outline_color` - color of the text outline, list of RGB values


## RGBMatrixEmulator Configuration
*Configuration is done within `emulator_config.json`*

`pixel_size` - size of the emulated LED \
`pixel_style` - style of the emulated LED, either "square" or "circle"

*For full details on the emulator config, visit the documentation [here](https://github.com/ty-porter/RGBMatrixEmulator#customization)*
