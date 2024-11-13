import time
from PIL import Image, ImageEnhance

def display_league(league, matrix):

    offscreen_canvas = matrix.CreateFrameCanvas()
    offscreen_canvas.Clear()

    logo_file = str("./media/" + str(league) + ".png")
    logo = Image.open(logo_file)
    logo = ImageEnhance.Brightness(logo).enhance(0.6)
    logo.thumbnail((150, 64), Image.Resampling.BOX)
    matrix.SetImage(logo.convert('RGB'), -7, 0)

    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def main(league, matrix):
    try:
        display_league(league, matrix)
        time.sleep(3) # default to 5
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit
        

if __name__ == "__main__":
    main()
