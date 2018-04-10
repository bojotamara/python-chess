###### Arun Woosaree
###### Tamara Bojovic


# CMPUT 275 Final Project - Python Chess Game

For our final project, we decided to make a player versus computer implementation
of chess using the pygame library for Python. It includes all the essential rules
for chess. The computer player uses the minmax strategy
for generating and deciding moves. A graphical representation of the board is rendered
with a side menu with contextual tips, that displays useful information such as
whose turn it is, if the move you're attempting is invalid, if someone is in
check, among other things. The mouse is used to select pieces and move them.
The program only allows you to make valid moves according to the rules of chess,
and also includes the special moves: castling, and promotion.
The program automatically detects check and checkmate, and for the latter,
ends the game and declares the winner.

For more specific instructions on how to play, see 'Usage Instructions'.

## Setup Instructions:
###### Make sure you're using python 3

### Ubuntu
'''
sudo apt install python3-pip
pip3 -m install --user pygame
python3 chess.py
'''

### Arch
'''
sudo pacman -S python-pip
pip -m install --user pygame
python chess.py
'''

### Windows
###### In the installer, make sure to add python to your PATH
https://www.python.org/downloads/release/python-365/
Open a command prompt window:
'''
pip -m install --user pygame
python chess.py
'''



#### Moving A Piece On Your Turn:
Use the mouse to select one of your pieces and then select the square you want to move it to
If you choose an invalid place to move to, a message will be displayed informing
you of the rule infringement, and you will be able to try again.

#### Checking:
If your opponent places you in check, a message will be displayed informing you
that you are in check. Your next move MUST get you out of the check. If you attempt
to make a move that doesn't get you out of check, a warning message will be
displayed, and the move will not be allowed. Once you get out of check, the game
proceeds as normal.

#### Checkmate/End Game:
When you or your opponent enters the check state, the program will automatically
check for a checkmate. If there is indeed a checkmate, the game will end and the
winner will be displayed. To play again, just press the reset button.

#### Castling:
If the rook and the king have not yet moved, the spaces are empty between them,
none of the in betweens or the new location of the king are in check,
you can castle. To perform the castling maneuver, select your king, and then
select the rook you want to castle with, and the move will be performed automatically.
Refer to https://en.wikipedia.org/wiki/Castling
for valid criteria for castling, if you are unfamiliar with this rule.

#### Promotion:
If one of your pawns reaches the opposite end of the board, it will automatically
be promoted to a queen.

----

## File Layout / Description:

##### chess.py:
Run this if you want to play the game

##### modules/board,py:
Contains the board class

##### modules/computer.py


##### modules/pieces.py
Contains all the chess piece classes

##### assets/
Contains picture assets


## Acknowledgments:

The images of the chess pieces were taken off of
https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
re converted to lcd format using the bmptolcd tool posted

The camstream() function is modified from a gist. It's used to take a picture of the player https://gist.github.com/snim2/255151
The assets/draw_chessboard.py function is modified from a gist as well. It generates the background chess board image using pillow
(since the image is already generated, there is no need to install pillow) https://gist.github.com/victorfei/1843ffd5fe871ef74d6bb3ce2a01dee8

king and queen from the menu are from:
https://thenounproject.com
Vasily Gedzun from the Noun Project

Font: Google Roboto
