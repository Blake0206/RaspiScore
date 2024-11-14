import time
from PIL import Image

def display_league(league, matrix, config):

    offscreen_canvas = matrix.CreateFrameCanvas()
    offscreen_canvas.Clear()

    logo_file = str("./media/" + str(league) + ".png")
    logo = Image.open(logo_file).convert('RGBA')
    logo.thumbnail((config["league_logo_size"], config["league_logo_size"]), Image.Resampling.BOX)
    matrix.SetImage(logo.convert('RGB'), int(matrix.options.cols/2) - int(logo.width/2), int(matrix.options.rows/2) - int(logo.height/2))

    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def main(league, matrix, config):
    try:
        display_league(league, matrix, config)
        time.sleep(3) # default to 5
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit
        

if __name__ == "__main__":
    main()
