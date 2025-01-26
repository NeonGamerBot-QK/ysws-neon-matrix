import board
import displayio
import framebufferio
import terminalio
from adafruit_display_text import label
import time
import rgbmatrix
import requests


matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1
)


display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

loading_screen = displayio.Group()

background_bitmap = displayio.Bitmap(display.width, display.height, 1)  # 1 color
background_palette = displayio.Palette(1)
background_palette[0] = 0x0000FF  # Blue color
background_tilegrid = displayio.TileGrid(background_bitmap, pixel_shader=background_palette)
loading_screen.append(background_tilegrid)

display.root_group = loading_screen
display.refresh()

print("Fetching quote..")
def get_quote():
    response = requests.get("https://api.saahild.com/api/quotesdb/random")
    return response.json().get("quote", '"I dont have a quote" - Neon')
info_screen = displayio.Group()

# Create a label for the scrolling text
quote_label = label.Label(
    terminalio.FONT,
    text=get_quote(),
    color=0xCBA6F7,
    scale=1,
    anchor_point=(0.5, 0.5),
    anchored_position=(display.width, display.height // 2),  # Start from the right side
)

info_screen.append(quote_label)
display.root_group = info_screen
display.refresh()

# Scroll the text
scroll_speed = 0.15  # Adjust the speed of the scrolling
while True:
    quote_label.x -= 1  # Move the text left by 1 pixel
    if quote_label.x + quote_label.bounding_box[2] < 0:  # Reset position when it goes off-screen
        quote_label.text = get_quote()
        quote_label.x = display.width
    display.refresh()  # Update the display
    time.sleep(scroll_speed)  # Control scroll speed
