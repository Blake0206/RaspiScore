import news.foxnews as foxnews, news.espnnews as espnnews
import matrix_display.displayLeague1x128 as displayLeague1x128
import matrix_display.displayEvents1x128 as displayEvents1x128
import matrix_display.displayNews1x128 as displayNews1x128
import sports.mlb as mlb, sports.nfl as nfl, sports.nba as nba, sports.ncaaf as ncaaf
import sports.ncaam as ncaam, sports.ncaaw as ncaaw, sports.wnba as wnba, sports.nhl as nhl
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
import json

class ConfigError(Exception):
    # Custom exception for configuration errors
    pass

class ConfigLoader:
    VALID_LEAGUES = {"mlb", "nba", "nfl", "ncaaf", "ncaam", "ncaaw", "wnba", "nhl"}
    VALID_NEWS_SOURCES = {"espn", "fox"}
    VALID_FIRST_DISPLAY = {"leagues", "news"}

    def __init__(self, config_file):
        with open(config_file, "r") as f:
            self.config = json.load(f)
        self.validate_config()

    def validate_config(self):
        # Validate time_correction
        if not isinstance(self.config.get("time_correction"), int):
            raise ConfigError("time_correction must be an integer")

        # Validate leagues
        leagues = self.config.get("leagues", [])
        if not isinstance(leagues, list) or not all(league in self.VALID_LEAGUES for league in leagues):
            raise ConfigError(f"leagues must be a list containing only of {self.VALID_LEAGUES}.")

        # Validate news
        news = self.config.get("news")
        if news not in self.VALID_NEWS_SOURCES:
            raise ConfigError(f"news must be one of {self.VALID_NEWS_SOURCES}")

        # Validate first_display
        first_display = self.config.get("first_display")
        if first_display not in self.VALID_FIRST_DISPLAY:
            raise ConfigError(f"first_display must be one of {self.VALID_FIRST_DISPLAY}")

        # Validate league_logo_size
        league_logo_size = self.config.get("league_logo_size")
        if not isinstance(league_logo_size, int) or league_logo_size <= 0:
            raise ConfigError("league_logo_size must be a positive intege.")

        # Validate team_logo_size
        team_logo_size = self.config.get("team_logo_size")
        if not isinstance(team_logo_size, int) or team_logo_size <= 0:
            raise ConfigError("team_logo_size must be a positive integer")

        # Validate team_logo_offset
        team_logo_offset = self.config.get("team_logo_offset")
        if not isinstance(team_logo_offset, int):
            raise ConfigError("team_logo_offset must be an integer")
        
        # Validate team_logo_mirrored
        if not isinstance(self.config.get("team_logo_mirrored"), bool):
            raise ConfigError("team_logo_mirrored must be a boolean")

        # Validate score_offset
        score_offset = self.config.get("score_offset")
        if not isinstance(score_offset, int) or score_offset <= 0:
            raise ConfigError("score_offset must be a positive integer")

def setup_matrix():
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 128
    options.chain_length = 1
    options.parallel = 1
    options.brightness = 75
    options.hardware_mapping = 'regular'
    return RGBMatrix(options=options)

def run_app(league, news_source, matrix, config):

    match league: 
        case 'mlb':
            category = 'baseball'
            espn_sport = 'mlb'
            fox_sport = 'mlb'
            events_data = mlb.getData()
        case 'nba':
            category = 'basketball'
            espn_sport = 'nba'
            fox_sport = 'nba'
            events_data = nba.getData()
        case 'nfl':
            category = 'football'
            espn_sport = 'nfl'
            fox_sport = 'nfl'
            events_data = nfl.getData()
        case 'ncaaf':
            category = 'football'
            espn_sport = 'college-football'
            fox_sport = 'college-football'
            events_data = ncaaf.getData()
        case 'ncaam':
            category = 'basketball'
            espn_sport = 'mens-college-basketball'
            fox_sport = 'college-basketball'
            events_data = ncaam.getData()
        case 'ncaaw':
            category = 'basketball'
            espn_sport = 'womens-college-basketball'
            fox_sport = 'womens-college-basketball'
            events_data = ncaaw.getData()
        case 'wnba':
            category = 'basketball'
            espn_sport = 'wnba'
            fox_sport = 'wnba'
            events_data = wnba.getData()
        case 'nhl':
            category = 'hockey'
            espn_sport = 'nhl'
            fox_sport = 'nhl'
            events_data = nhl.getData()
        case _:
            print("Error with 'leagues' specified in main_config.json")
            return

    if news_source == 'espn':
        headlines_data = espnnews.main(category, espn_sport)
    elif news_source == 'fox':
        headlines_data = foxnews.main(fox_sport) 

    for article in headlines_data:
        print(article[0])
        print("/".join(article[1]))
        print('-'*80)

    first_display = config["first_display"]
    displayLeague1x128.main(league, matrix, config)

    if first_display == 'leagues':
        displayEvents1x128.main(events_data, matrix, config)
        displayNews1x128.main(headlines_data, matrix, config)
    elif first_display == 'news':
        displayNews1x128.main(headlines_data, matrix, config)
        displayEvents1x128.main(events_data, matrix, config)
    else:
        print("Error with 'first_display' specified in main_config.json")

if __name__ == "__main__":
    try:
        config_loader = ConfigLoader("main_config.json")
        config = config_loader.config
        matrix = setup_matrix()

        leagues = config['leagues']
        news = config['news']
        
        while True:
            for league in leagues:
                run_app(league, news, matrix, config)
    except ConfigError as e:
        print(f"Configuration Error: {e}")
    except KeyboardInterrupt:
        print("Quitting program...")
