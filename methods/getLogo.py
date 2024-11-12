import urllib.request
from PIL import Image
import base64

def main(team):
    logo_url = team["team"]["logo"]
    logo_url = logo_url.replace("https", "http")
    #img = urllib.request.urlretrieve(logo_url, "team_logo.png")
    #img = Image.open("team_logo.png")
    #encoded_img = base64.encodebytes(img)
    #img.show()
    return logo_url

if __name__ == "__main__":
    main()