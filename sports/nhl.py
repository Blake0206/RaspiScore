import espn_scraper as espn
import json
import methods.getOdds as getOdds
import methods.getBroadcasts as getBroadcasts
import methods.changeTime as changeTime
import methods.getLogo as getLogo


def getData():
    urls = espn.get_current_scoreboard_urls(league='nhl')

    for scoreboard_url in urls:
        data = espn.get_url(scoreboard_url)

    print("\n" + "-"*40 + "\n")

    for event in data["events"]:

        short_detail = event["status"]["type"]["shortDetail"]

        if short_detail.find("Final") != 0:
            print(getBroadcasts.main(event))
        else:
            print(f"{short_detail}")

        print(getOdds.main('hockey', 'nhl', event, short_detail))

        if short_detail.find(":") != -1:
            print(changeTime.main(short_detail))

        for competition in event["competitions"]:

            for team in competition["competitors"]:

                team_abbreviation = team["team"]["shortDisplayName"]
                team_score = team["score"]

                #showLogo.main(team)

                if short_detail.find('EDT') == -1:
                    print(f"{team_abbreviation} - {team_score}")
                else:
                    print(f"{team_abbreviation}")

        print("\n" + "-"*40 + "\n")


if __name__ == "__main__":
    getData()