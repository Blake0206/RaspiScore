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

def display_headline(matrix, headline):
    title = headline[0]
    teams = headline[1]

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./matrix_display/7x13.bdf")

    white_color = graphics.Color(255, 255, 255)
    black_color = graphics.Color(0, 0, 0)

    offscreen_canvas.Clear()

    logo = Image.open("espn_logo.png")
    logo = ImageEnhance.Brightness(logo).enhance(0.6)
    logo.thumbnail((150, 64), Image.Resampling.BOX)
    matrix.SetImage(logo.convert('RGB'), -7, 0)


    def split_text_by_words(text, n=18):
        words = title.split()  # Split by spaces into words
        result = []
        current_line = ""
        
        for word in words:
            # If adding the next word exceeds the desired length, save the current line and start a new one
            if len(current_line) + len(word) + 1 > n:
                result.append(current_line.strip())  # Remove any extra spaces
                current_line = word
            else:
                current_line += " " + word
        
        # Add the last line if it's not empty
        if current_line:
            result.append(current_line.strip())
        
        return result
    
    new_title = split_text_by_words(title)

    line_count = 0
    for line in new_title:
        line_count += 1
        height = len(new_title) * 13
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) -1, ((64-height)/2 + (10*line_count) + 6) - 1, black_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) +1, ((64-height)/2 + (10*line_count) + 6) + 1, black_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) -1, ((64-height)/2 + (10*line_count) + 6) + 1, black_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) +1, ((64-height)/2 + (10*line_count) + 6) - 1, black_color, line)

        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) -1, ((64-height)/2 + (10*line_count) + 6), black_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) +1, ((64-height)/2 + (10*line_count) + 6), black_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)), ((64-height)/2 + (10*line_count) + 6) + 1, black_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)), ((64-height)/2 + (10*line_count) + 6) - 1, black_color, line)

        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)), (64-height)/2 + (10*line_count) + 6, white_color, line)
    
    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def main(headlines_data):
    matrix = setup_matrix()

    try:
        for headline in headlines_data:
            display_headline(matrix, headline)
            time.sleep(3) # default to 5
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit
        

if __name__ == "__main__":
    main()
