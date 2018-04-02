#ifndef _CHESSFUNCTIONS_H
#define _CHESSFUNCTIONS_H

//keeps track of checkmates
extern int gameover;

//keeps track of whose turn it is
extern int currentplayer;

//2-D array that represents the board
extern int board [8][8];

// hold the position of square selected
extern int selectedY;
extern int oldSelectedY;
extern int selectedX;
extern int oldSelectedX;
extern int chosenX;
extern int chosenY;

void drawBoard();

void fillBoardArray();

void emptySquare(int squarex, int squarey);

void drawPiece(int squarex, int squarey, int piecetype);

void drawArray();

void unhighlightSquare(int squarex, int squarey);

void highlightSquare(int squarex, int squarey, uint16_t bordercolor= 0xFFFF);

void scroll();

void movePiece(int oldx, int oldy, int pieceToMove);

void moveMode();

void dispCurrentPlayer();

void dispTips(String tip);

void endGame(int player);

#endif
