# Displays scores from ESPN onto an led matrix
Currently everything is being ran on an emulator using [RGBMatrixEmulator](https://github.com/ty-porter/RGBMatrixEmulator) \
Information is gathered from ESPN using the [espn_scraper](https://github.com/andr3w321/espn_scraper)


## Install
Clone the repository using `git clone https://github.com/Blake0206/RaspiScore.git` \
From the `RaspiScore` folder, run `pip install -r requirements.txt` to install the required packages


## Run
Run the main program by using `python3 main.py` \
By default, the emulator will run on [http://localhost:8888](http://localhost:8888) \
*Any errors and additional information will be displayed in the terminal*


## Configuration
*Configuration is done within `main_config.json`*

`time_correction` - hour difference from EST, positive and negative integers are accepted \
`leagues` - sports leagues that are displayed, accepted strings of "mlb", "nba", "nfl", "ncaaf", "ncaam", "ncaaw", "wnba", "nhl" \
`news` - source of news data, accepted string of "espn" or "fox" \
`first_display` - first information that is displayed, accepted string of "leagues" or "news" \
`league_logo_size` - size in pixels of the league logo displayed before events/news, positive integers are accepted \
`team_logo_size` - size in pixels of the team logo displayed for events, positive integers are accepted \
`team_logo_offset` - negative offset in pixels from the left/right edges for the team logos, positive and negative integers are accepted \
`team_logo_mirrored` - mirrors the logo on the right if set to true, boolean values are accepted \
`score_offset` - offset in pixels from the left/right edges for the scores, positive integers are accepted

### RGBMatrixEmulator
*Configuration is done within `emulator_config.json`* \
*For full details on the emulator config, visit the documentation [here](https://github.com/ty-porter/RGBMatrixEmulator#customization)*

`pixel_size` - size of the emulated LED \
`pixel_style` - style of the emulated LED, either "square" or "circle"
