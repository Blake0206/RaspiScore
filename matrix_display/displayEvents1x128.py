import time
from RGBMatrixEmulator import graphics
from PIL import Image, ImageEnhance
import urllib.request

def display_event(event, matrix, config):
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
    font.LoadFont("./matrix_display/fonts/ic16x16u.bdf")
    font_width = 13

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

        logo.thumbnail((config["team_logo_size"], config["team_logo_size"]), Image.Resampling.BOX)

        if i == 1:
            matrix.SetImage(logo.convert('RGB'), -config["team_logo_offset"], int(matrix.options.rows/2) - int(logo.height/2))
        else:
            matrix.SetImage(logo.convert('RGB'), 128 - config["team_logo_size"] + config["team_logo_offset"], int(matrix.options.rows/2) - int(logo.height/2))

    if len(short_detail) > 12:
        short_detail = event["start time"]
    elif (short_detail.find(":") != -1 or short_detail.find(".") != -1) and short_detail.find("EST") == -1:
        time_detail = short_detail.split(" - ")[0]
        short_detail = short_detail.split(" - ")[1]

        graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(time_detail)*font_width)/2)) -1,  36-1, black_color, time_detail)
        graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(time_detail)*font_width)/2)) +1,  36+1, black_color, time_detail)
        graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(time_detail)*font_width)/2)) -1,  36+1, black_color, time_detail)
        graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(time_detail)*font_width)/2)) +1,  36-1, black_color, time_detail)
        graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(time_detail)*font_width)/2)),  36, white_color, time_detail)

    if (short_detail.find("End of ")) != -1:
        short_detail = short_detail[:-2]
        
    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(short_detail)*font_width)/2)) - 1,  20-1, black_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(short_detail)*font_width)/2)) + 1,  20+1, black_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(short_detail)*font_width)/2)) - 1,  20+1, black_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(short_detail)*font_width)/2)) + 1,  20-1, black_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(short_detail)*font_width)/2)),  20, white_color, short_detail)

    graphics.DrawText(offscreen_canvas, font, config["score_offset"] - 1,  60-1, black_color, home_team_score)
    graphics.DrawText(offscreen_canvas, font, config["score_offset"] + 1,  60+1, black_color, home_team_score)
    graphics.DrawText(offscreen_canvas, font, config["score_offset"] - 1,  60+1, black_color, home_team_score)
    graphics.DrawText(offscreen_canvas, font, config["score_offset"] + 1,  60-1, black_color, home_team_score)
    graphics.DrawText(offscreen_canvas, font, config["score_offset"],  60, white_color, home_team_score)

    graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["score_offset"] - (len(away_team_score)*font_width) - 1,  60-1, black_color, away_team_score)
    graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["score_offset"] - (len(away_team_score)*font_width) + 1,  60+1, black_color, away_team_score)
    graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["score_offset"] - (len(away_team_score)*font_width) - 1,  60+1, black_color, away_team_score)
    graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["score_offset"] - (len(away_team_score)*font_width) + 1,  60-1, black_color, away_team_score)
    graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["score_offset"] - (len(away_team_score)*font_width),  60, white_color, away_team_score)
    
    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def main(events_data, matrix, config):
    try:
        for event in events_data:
            display_event(event, matrix, config)
            time.sleep(3) # default to 5
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit
        

if __name__ == "__main__":
    main()
