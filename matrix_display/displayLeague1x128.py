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

def display_league(matrix, league):

    offscreen_canvas = matrix.CreateFrameCanvas()
    #font = graphics.Font()
    #font.LoadFont("./matrix_display/7x13.bdf")

    #white_color = graphics.Color(255, 255, 255)
    #black_color = graphics.Color(0, 0, 0)

    offscreen_canvas.Clear()

    logo_file = str("./media/" + str(league) + ".png")
    logo = Image.open(logo_file)
    #logo = ImageEnhance.Brightness(logo).enhance(0.6)
    logo.thumbnail((150, 64), Image.Resampling.BOX)
    matrix.SetImage(logo.convert('RGB'), -7, 0)

    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def main(league):
    matrix = setup_matrix()

    try:
        display_league(matrix, league)
        time.sleep(3) # default to 5
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit
        

if __name__ == "__main__":
    main()
