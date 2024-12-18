import json

class ConfigError(Exception):
    # Custom exception for configuration errors
    pass

class ConfigLoader:
    VALID_LEAGUES = {"mlb", "nba", "nfl", "ncaaf", "ncaam", "ncaaw", "wnba", "nhl"}
    VALID_CONFERENCE_IDs = {0, 80, 81, 1, 4, 5, 8, 9, 12, 15, 17, 18, 20, 21, 22, 24, 25, 27, 28, 29, 30, 31, 32, 35, 37, 48, 151, 177, 179}
    VALID_NEWS_SOURCES = {"espn", "fox"}
    VALID_FIRST_DISPLAY = {"events", "news"}

    def __init__(self, config_file):
        with open(config_file, "r") as f:
            self.config = json.load(f)
        self.validate_config()

    def validate_config(self):
        leagues = self.config.get("leagues", {})
        events = self.config.get("events", {})
        news = self.config.get("news", {})
        other = self.config.get("other", {})

        # Validate leagues
        displayed_leagues = leagues.get("displayed_leagues", [])
        if not isinstance(displayed_leagues, list) or not all(l in self.VALID_LEAGUES for l in displayed_leagues):
            raise ConfigError(f"displayed_leagues must be a list containing only {self.VALID_LEAGUES}")

        if leagues.get("ncaaf_conference") not in self.VALID_CONFERENCE_IDs:
            raise ConfigError(f"ncaaf_conference must be one of {self.VALID_CONFERENCE_IDs}")

        if leagues.get("ncaam_conference") not in self.VALID_CONFERENCE_IDs:
            raise ConfigError(f"ncaam_conference must be one of {self.VALID_CONFERENCE_IDs}")

        if leagues.get("ncaaw_conference") not in self.VALID_CONFERENCE_IDs:
            raise ConfigError(f"ncaaw_conference must be one of {self.VALID_CONFERENCE_IDs}")
                                
        if not isinstance(leagues.get("league_display_time"), int) or leagues["league_display_time"] <= 0:
            raise ConfigError("league_display_time must be a positive integer")
        
        if not isinstance(leagues.get("league_logo_size"), int) or leagues["league_logo_size"] <= 0:
            raise ConfigError("league_logo_size must be a positive integer")


        # Validate events
        if not isinstance(events.get("display_events"), bool):
            raise ConfigError("display_events must be a boolean")
        
        if not isinstance(events.get("event_display_time"), int) or events["event_display_time"] <= 0:
            raise ConfigError("event_display_time must be a positive integer")
        
        if not isinstance(events.get("team_logo_size"), int) or events["team_logo_size"] <= 0:
            raise ConfigError("team_logo_size must be a positive integer")
        
        if not isinstance(events.get("team_logo_offset"), int):
            raise ConfigError("team_logo_offset must be an integer")
        
        if not isinstance(events.get("team_logo_mirrored"), bool):
            raise ConfigError("team_logo_mirrored must be a boolean")
        
        if not isinstance(events.get("team_logo_opacity"), float) or events["team_logo_opacity"] < 0 or events["team_logo_opacity"] > 5:
            raise ConfigError("team_logo_opacity must be a positive float between 0 and 5")
        
        if not isinstance(events.get("score_offset"), int) or events["score_offset"] < 0:
            raise ConfigError("score_offset must be a positive integer")
        

        # Validate news
        if not isinstance(news.get("display_news"), bool):
            raise ConfigError("display_news must be a boolean")
        
        if news.get("source") not in self.VALID_NEWS_SOURCES:
            raise ConfigError(f"source must be one of {self.VALID_NEWS_SOURCES}")
        
        if not isinstance(news.get("news_display_time"), int) or news["news_display_time"] <= 0:
            raise ConfigError("news_display_time must be a positive integer")
        
        if not isinstance(news.get("display_source_logo"), bool):
            raise ConfigError("display_source_logo must be a boolean")
        
        if not isinstance(news.get("source_logo_opacity"), float) or news["source_logo_opacity"] < 0 or news["source_logo_opacity"] > 5:
            raise ConfigError("source_logo_opacity must be a positive float between 0 and 5")
        
        if not isinstance(news.get("line_spacing"), int) or news["line_spacing"] < 10:
            raise ConfigError("line_spacing must be a positive integer greater than 10")


        # Validate other settings
        if not isinstance(other.get("time_correction"), int):
            raise ConfigError("time_correction must be an integer")
        
        if other.get("first_display") not in self.VALID_FIRST_DISPLAY:
            raise ConfigError(f"first_display must be one of {self.VALID_FIRST_DISPLAY}")
        
        if not isinstance(other.get("text_color"), list) or len(other["text_color"]) != 3:
            raise ConfigError("text_color must be a list of three values")
        
        if not isinstance(other.get("outline_color"), list) or len(other["outline_color"]) != 3:
            raise ConfigError("outline_color must be a list of three values")