import espn_scraper as espn


def main(category, sport, event, short_detail): 
    if short_detail.find(":") != -1 and (short_detail.find("EST") != -1 or short_detail.find("EDT") != -1):
        event_id = event["id"]
        if len(event_id) == 9 and event_id.isdigit():
            event_id = str(event_id)
            odds = espn.get_new_json("https://sports.core.api.espn.com/v2/sports/" + category + "/leagues/" + sport + "/events/" + event_id + "/competitions/" + event_id + "/odds")
            if type(odds) == dict:
                spread = odds["items"][0]["details"]
                total = odds["items"][0]["current"]["total"]["alternateDisplayValue"]
                try:
                    money_line_away = odds["items"][0]["awayTeamOdds"]["current"]["moneyLine"]["alternateDisplayValue"]
                    money_line_home = odds["items"][0]["homeTeamOdds"]["current"]["moneyLine"]["alternateDisplayValue"]
                except:
                    money_line_away = 0
                    money_line_home = 0
                try:
                    money_line = max(int(money_line_away), int(money_line_home))
                except:
                    money_line = 0

                return f"Spread: {spread} | Total: {total} | ML: {money_line}"
            else:
                return "No odds available"


if __name__ == "__main__":
    main()