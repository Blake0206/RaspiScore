import time
from RGBMatrixEmulator import graphics
from PIL import Image

def display_splash(ip_address, matrix, config):

    offscreen_canvas = matrix.CreateFrameCanvas()
    offscreen_canvas.Clear()

    font = graphics.Font()
    #font.LoadFont("./matrix_display/fonts/ic16x16u.bdf")
    font.LoadFont("./matrix_display/fonts/7x13.bdf")
    font_width = 7

    r, g, b = config["other"]["text_color"]
    text_color = graphics.Color(r, g, b)

    r, g, b = config["other"]["outline_color"]
    outline_color = graphics.Color(r, g, b)

    logo = Image.open("./media/pi_logo.png")
    logo.thumbnail((64, 40), Image.Resampling.BOX)
    matrix.SetImage(logo.convert('RGB'), int(matrix.options.cols/2) - int(logo.width/2), int(matrix.options.rows/2) - int(logo.height/2) - 8)

    ip_address += ":5001"

    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(ip_address)*font_width)/2)) - 1,  57-1, outline_color, ip_address)
    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(ip_address)*font_width)/2)) + 1,  57+1, outline_color, ip_address)
    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(ip_address)*font_width)/2)) - 1,  57+1, outline_color, ip_address)
    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(ip_address)*font_width)/2)) + 1,  57-1, outline_color, ip_address)
    graphics.DrawText(offscreen_canvas, font, (int(matrix.options.cols/2) - ((len(ip_address)*font_width)/2)),  57, text_color, ip_address)

    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def main(ip_address, matrix, config):
    try:
        display_splash(ip_address, matrix, config)
        time.sleep(10)
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit
        

if __name__ == "__main__":
    main()