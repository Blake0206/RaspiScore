import requests
from bs4 import BeautifulSoup

# nfl, college-football, mlb, nba, wnba, college-basketball, womens-college-basketball, nhl

def main(sport):
    url = "https://www.foxsports.com/stories/" + sport
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    headlines = soup.find_all('h2')
    dates = soup.find_all(attrs={"class": "article-time"})

    final_dates = []
    for date in dates:
        new_date = date.string.strip()
        if new_date.find("hours") != -1 or new_date.find("hour") != -1 or new_date.find("mins") != -1 or new_date.find("min") != -1:
            final_dates.append(new_date)

    final_headlines = []
    i = 0
    for headline in headlines:
        if headline.string and len(headline.string) > 30 and i < len(final_dates):    
            new_headline = headline.string.strip()
            final_headlines.append(new_headline)
            i = i +1

    print("\n" + "-"*80)
    for headline in final_headlines:
        print(headline, end="\n" + "-"*80 + "\n")
    print()

if __name__ == "__main__":
    main()
