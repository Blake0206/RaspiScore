# Displays scores from ESPN onto an led matrix
Currently everything is being ran on an emulator using [RGBMatrixEmulator](https://github.com/ty-porter/RGBMatrixEmulator#customization) \
Information is gathered from ESPN using the [espn_scraper](https://github.com/andr3w321/espn_scraper)


## Installation
Run `pip install -r requirements.txt` to install the required packages


## Run
From the root directory, run the main program by using `python3 main.py` \
By default, the emulator will run on [http://localhost:8888](http://localhost:8888) \
Any errors will be displayed in the terminal


## Configuration

### RaspiScore
*Configuration is done within `main_config.json`*

`leagues` - sports leagues that are displayed, accepted strings of "mlb", "nba", "nfl", "ncaaf", "ncaam", "ncaaw", "wnba", "nhl" \
`news` - source of news data, accepted string of "espn" or "fox" \
`first_display` - first information that is displayed, accepted string of "leagues" or "news"

### RGBMatrixEmulator
*Configuration is done within `emulator_config.json`* \
*For full details on the emulator config, visit the documentation [here](https://github.com/ty-porter/RGBMatrixEmulator#customization)*

`pixel_size` - size of the emulated LED \
`pixel_style` - style of the emulated LED, either "square" or "circle"
