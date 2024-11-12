import news_sources.foxnews as foxnews, news_sources.espnnews as espnnews, matrix_display.displayLeague1x128 as displayLeague1x128, matrix_display.displayData1x128 as displayData1x128, matrix_display.displayNews1x128 as displayNews1x128, sports.mlb as mlb, sports.nfl as nfl, sports.nba as nba, sports.ncaaf as ncaaf, sports.ncaam as ncaam, sports.ncaaw as ncaaw, sports.wnba as wnba, sports.nhl as nhl

def run_app(league, news_source):

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
        print(article[0])
        print("/".join(article[1]))
        print('-'*80)

    
    #for event_data in events_data:
    #    for k, v in event_data.items():
    #        print(str(k) + ": " + str(v) + " " + str(type(v)).removeprefix('<class ').removesuffix('>'))
    #    print('-'*30)

    displayLeague1x128.main(league)
    displayData1x128.main(events_data)
    displayNews1x128.main(headlines_data)


if __name__ == "__main__":
    #leagues = ['mlb', 'nba', 'nfl', 'ncaaf', 'ncaam', 'ncaaw', 'wnba', 'nhl']
    leagues = ['nba', 'nfl']
    
    try:
        while True:
            for league in leagues:
                run_app(league, 'espn')
    except KeyboardInterrupt:
        # Ctrl+C to quit
        print("Quitting program...")
    