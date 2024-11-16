import time
from RGBMatrixEmulator import graphics
from PIL import Image, ImageEnhance

def display_headline(headline, matrix, config):

    if config["news"]["source"] == 'espn':
        title = headline[0]
        teams = headline[1]
    else:
        title = headline

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./matrix_display/fonts/7x13.bdf")

    r, g, b = config["other"]["text_color"]
    text_color = graphics.Color(r, g, b)

    r, g, b = config["other"]["outline_color"]
    outline_color = graphics.Color(r, g, b)

    offscreen_canvas.Clear()

    if config["news"]["display_source_logo"]:
        logo = Image.open("./media/news/" + str(config["news"]["source"]) + "_logo.png")
        logo = ImageEnhance.Brightness(logo).enhance(config["news"]["source_logo_opacity"])
        logo.thumbnail((150, 64), Image.Resampling.BOX)
        matrix.SetImage(logo.convert('RGB'), int(matrix.options.cols/2) - int(logo.width/2), int(matrix.options.rows/2) - int(logo.height/2))


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
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) -1, ((64-height)/2 + (10*line_count) + 6) - 1, outline_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) +1, ((64-height)/2 + (10*line_count) + 6) + 1, outline_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) -1, ((64-height)/2 + (10*line_count) + 6) + 1, outline_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) +1, ((64-height)/2 + (10*line_count) + 6) - 1, outline_color, line)

        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) -1, ((64-height)/2 + (10*line_count) + 6), outline_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)) +1, ((64-height)/2 + (10*line_count) + 6), outline_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)), ((64-height)/2 + (10*line_count) + 6) + 1, outline_color, line)
        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)), ((64-height)/2 + (10*line_count) + 6) - 1, outline_color, line)

        graphics.DrawText(offscreen_canvas, font, (64 - ((len(line)*7)/2)), (64-height)/2 + (10*line_count) + 6, text_color, line)
    
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
