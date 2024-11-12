import time
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageEnhance
import urllib.request

def setup_matrix():
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 128
    options.chain_length = 1
    options.parallel = 1
    options.brightness = 75
    options.hardware_mapping = 'regular'
    return RGBMatrix(options=options)

def display_event(matrix, event):
    #broadcasts = event["broadcasts"]
    short_detail = event["short detail"]
    #show_outs = event["show outs"]
    #odds = event["odds"]
    #firstBase = event["first base"]
    #secondBase = event["second base"]
    #thirdBase = event["third base"]
    #outs = event["outs"]
    #strikes = event["strikes"]
    #balls = event["balls"]
    #home_team_name = event["team1 name"]
    home_team_score = event["team1 score"]
    #away_team_name = event["team2 name"]
    away_team_score = event["team2 score"]
    #home_logo_url = event["logo1"]
    #away_logo_url = event["logo2"]
    #home_team_score = '00'
    #away_team_score = '00'

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./matrix_display/ic16x16u.bdf")

    white_color = graphics.Color(255, 255, 255)
    black_color = graphics.Color(0, 0, 0)

    offscreen_canvas.Clear()

    i = 0
    while (i < 2):
        i += 1
        logo_url = event["logo" + str(i)]
        logo = urllib.request.urlretrieve(logo_url, "team_logo.png")
        logo = Image.open("team_logo.png")
        logo = ImageEnhance.Brightness(logo).enhance(0.6)
        #if i == 2:
        #    logo = ImageOps.mirror(logo)

        logo.thumbnail((90, 90), Image.Resampling.BOX)

        if i == 1:
            matrix.SetImage(logo.convert('RGB'), -30, -13)
        else:
            matrix.SetImage(logo.convert('RGB'), 128-60, -13)

    if len(short_detail) > 12:
        short_detail = event["start time"]
    elif short_detail.find(":") != -1 and short_detail.find("EST") == -1:
        time_detail = short_detail.split(" - ")[0]
        short_detail = short_detail.split(" - ")[1]

        graphics.DrawText(offscreen_canvas, font, (64 - ((len(time_detail)*14)/2)) -1,  36-1, black_color, time_detail)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(time_detail)*14)/2)) +1,  36+1, black_color, time_detail)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(time_detail)*14)/2)) -1,  36+1, black_color, time_detail)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(time_detail)*14)/2)) +1,  36-1, black_color, time_detail)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(time_detail)*14)/2)),  36, white_color, time_detail)

        
    graphics.DrawText(offscreen_canvas, font, (64 - ((len(short_detail)*14)/2)) -1,  20-1, black_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, (64 - ((len(short_detail)*14)/2)) +1,  20+1, black_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, (64 - ((len(short_detail)*14)/2)) -1,  20+1, black_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, (64 - ((len(short_detail)*14)/2)) +1,  20-1, black_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, (64 - ((len(short_detail)*14)/2)),  20, white_color, short_detail)

    graphics.DrawText(offscreen_canvas, font, 20-1,  60-1, black_color, home_team_score)
    graphics.DrawText(offscreen_canvas, font, 20+1,  60+1, black_color, home_team_score)
    graphics.DrawText(offscreen_canvas, font, 20-1,  60+1, black_color, home_team_score)
    graphics.DrawText(offscreen_canvas, font, 20+1,  60-1, black_color, home_team_score)
    graphics.DrawText(offscreen_canvas, font, 20,  60, white_color, home_team_score)

    graphics.DrawText(offscreen_canvas, font, 108-28-1,  60-1, black_color, away_team_score)
    graphics.DrawText(offscreen_canvas, font, 108-28+1,  60+1, black_color, away_team_score)
    graphics.DrawText(offscreen_canvas, font, 108-28-1,  60+1, black_color, away_team_score)
    graphics.DrawText(offscreen_canvas, font, 108-28+1,  60-1, black_color, away_team_score)
    graphics.DrawText(offscreen_canvas, font, 108-28,  60, white_color, away_team_score)
    
    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def main(events_data):
    matrix = setup_matrix()

    try:
        for event in events_data:
            display_event(matrix, event)
            time.sleep(3) # default to 5
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit
        

if __name__ == "__main__":
    main()
