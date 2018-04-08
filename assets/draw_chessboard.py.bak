#This code not written by us. It was used to generate a Background chessboard image
#It was modified to make brown squares, and the chess board was resized

#!/usr/bin/python
# adapted from:
#   http://wordaligned.org/articles/drawing-chessboards
from PIL import Image, ImageDraw
from itertools import cycle

def draw_chessboard(n=8, pixel_width=60*8):
    """
    Draw an n x n chessboard using PIL.
    """
    def sq_start(i):
        """
        Return the square corners, suitable for use in PIL drawings
        """
        return i*pixel_width / n

    def square(i, j):
        """
        Return the square corners, suitable for use in PIL drawing
        """
        return map(sq_start, [i, j, i+1, j+1])

    image = Image.new("L", (pixel_width, pixel_width))
    draw_square = ImageDraw.Draw(image).rectangle
    squares = (square(i,j)
              for i_start, j in zip(cycle((0, 1)), range(n))
               for i in range(i_start, n, 2))

    for sq in squares:
        draw_square(sq, fill='white')
        image.save("chessboard.png")

# draw 8 x 8 chess board with 500 pixel as pixel width
draw_chessboard(8)
