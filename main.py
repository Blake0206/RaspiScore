import news.foxnews as foxnews, news.espnnews as espnnews
import matrix_display.displayLeague1x128 as displayLeague1x128
import matrix_display.displayEvents1x128 as displayEvents1x128
import matrix_display.displayNews1x128 as displayNews1x128
import sports.mlb as mlb, sports.nfl as nfl, sports.nba as nba, sports.ncaaf as ncaaf
import sports.ncaam as ncaam, sports.ncaaw as ncaaw, sports.wnba as wnba, sports.nhl as nhl
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from config.config_loader import ConfigError, ConfigLoader

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

    if news_source == 'espn':
        headlines_data = espnnews.main(category, espn_sport)
    elif news_source == 'fox':
        headlines_data = foxnews.main(fox_sport) 

    for article in headlines_data:
        if config["news"]["source"] == 'espn':
            print(article[0])
            print("/".join(article[1]))
        else:
            print(article)
        print('-'*80)

    displayLeague1x128.main(league, matrix, config)
    first_display = config['other']['first_display']

    if first_display == 'events':
        displayEvents1x128.main(events_data, matrix, config)
        if config['news']['display_news']:
            displayNews1x128.main(headlines_data, matrix, config)
    elif first_display == 'news':
        displayNews1x128.main(headlines_data, matrix, config)
        if config['events']['display_events']:
            displayEvents1x128.main(events_data, matrix, config)


if __name__ == "__main__":
    try:
        config_loader = ConfigLoader("./config/main_config.json")
        config = config_loader.config
        matrix = setup_matrix()

        leagues = config['leagues']['displayed_leagues']
        news = config['news']['source']
        
        while True:
            for league in leagues:
                run_app(league, news, matrix, config)
    except ConfigError as e:
        print(f"Configuration Error: {e}")
    except KeyboardInterrupt:
        print("Quitting program...")
