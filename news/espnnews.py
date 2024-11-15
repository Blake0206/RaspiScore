import espn_scraper as espn

def main(category, sport):
    data = espn.get_new_json("https://site.api.espn.com/apis/site/v2/sports/" + category + "/" + sport + "/news?limit=10")

    #f = open("news.json", "w")
    #f.write(json.dumps(data, indent=2, sort_keys=True))

    print("\n" + "-"*80)
    headlines = []
    for article in data["articles"]:
        if "headline" in article:
            headline = article["headline"]
            teams = []
            for category in article["categories"]:
                if "team" in category:
                    team = category["team"]["description"]
                    teams.append(team)
            if len(teams) > 0:
                headlines.append([headline, teams])
                #print(teams, end="\n" + "-"*80 + "\n")
            
    return headlines


if __name__ == "__main__":
    main()
