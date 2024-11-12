import espn_scraper as espn
import json
import methods.getOdds as getOdds
import methods.getBroadcasts as getBroadcasts
import methods.changeTime as changeTime
import methods.getLogo as getLogo


def getData():
    urls = espn.get_current_scoreboard_urls(league='ncf')

    for scoreboard_url in urls:
        data = espn.get_url(scoreboard_url)

    print("\n" + "-"*40 + "\n")

    for event in data["events"]:
        short_detail = event["status"]["type"]["shortDetail"]

        if short_detail.find("Final") != 0:
            print(getBroadcasts.main(event))
        
        print(getOdds.main('football', 'college-football', event, short_detail))

        if short_detail.find(":") != -1 and short_detail.find("EDT") != -1:
            print(changeTime.main(short_detail))
        else:
            print(f"{short_detail}")

        for competition in event["competitions"]:

            down_distance_text = str(competition.get("situation", {}).get("downDistanceText"))
            possession_id = competition.get("situation", {}).get("possession")

            if down_distance_text == 'None':
                pass
            else:
                print(down_distance_text)

            for team in competition["competitors"]:
                rank = team["curatedRank"].get("current", "NR")
                team_abbreviation = team["team"]["shortDisplayName"]
                team_score = team["score"]

                #showLogo.main(team)

                possession_marker = "*" if team["id"] == possession_id else ""

                if short_detail.find('EDT') == -1:
                    if rank < 25:
                        print(f"#{rank:<2} {team_abbreviation} - {team_score} {possession_marker}")
                    else:
                        print(f"    {team_abbreviation} - {team_score} {possession_marker}")
                else:
                    print(f"{team_abbreviation}")

        print("\n" + "-"*40 + "\n")


if __name__ == "__main__":
    getData()