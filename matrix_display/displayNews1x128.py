import time
from RGBMatrixEmulator import graphics
from PIL import Image, ImageEnhance

def display_headline(headline, matrix, config):
    title = headline[0]
    teams = headline[1]

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./matrix_display/fonts/7x13.bdf")

    white_color = graphics.Color(255, 255, 255)
    black_color = graphics.Color(0, 0, 0)

    offscreen_canvas.Clear()

    logo = Image.open("./media/espn_logo.png")
    logo = ImageEnhance.Brightness(logo).enhance(0.6)
    logo.thumbnail((150, 64), Image.Resampling.BOX)
    matrix.SetImage(logo.convert('RGB'), -7, 0)


    def split_text_by_words(text, n=18):
        words = title.split()
        result = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 > n:
                result.append(current_line.strip())
                current_line = word
            else:
                current_line += " " + word
        
        if current_line:
            result.append(current_line.strip())
        
        return result
    
    new_title = split_text_by_words(title)
    
    if len(new_title) > 6:
        new_title.pop()
        new_title[5] += '...'

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


def main(headlines_data, matrix, config):
    try:
        for headline in headlines_data:
            display_headline(headline, matrix, config)
            time.sleep(config["news"]["news_display_time"])
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit
        

if __name__ == "__main__":
    main()
