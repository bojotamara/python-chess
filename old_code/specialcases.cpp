#include <Arduino.h>
#include "chessfunctions.h"
#include "validmoves.h"
#include "specialcases.h"

#define EMPTY 0

#define W_PAWN 1
#define W_ROOK 2
#define W_KNIGHT 3
#define W_BISHOP 4
#define W_KING 5
#define W_QUEEN 6

#define B_PAWN -1
#define B_ROOK -2
#define B_KNIGHT -3
#define B_BISHOP -4
#define B_KING -5
#define B_QUEEN -6

/*==============================================================================
Functions in this file handle special cases for weird things that happen in
the game, like promotion, castling, or en passant
==============================================================================*/

void specialmovepiece(int oldx, int oldy, int x, int y, int piece){
  //function based on movePiece in chessfunctions.cpp but modified to
  //work for the purpose of castling and other special functions
  	board[oldy][oldx] = EMPTY;
  	board[y][x] = piece;
  	emptySquare(oldx,oldy);
  	drawPiece(x,y,piece);
}

void promote_to_Queen(int x, int y){
  //this function assumes requrements for promotion have been met, and it does
  //the move
  switch(currentplayer){

    case 1:
      board[y][x] = W_QUEEN;
      drawPiece(x,y,W_QUEEN);
      //Serial.print("Position: "); Serial.print(x); Serial.print(" "); Serial.println(y);
    break;

    case 2:
      board[y][x] = B_QUEEN;
      drawPiece(x,y,B_QUEEN);
    break;
  }
}

bool en_passant(int x, int y){
  //returns boolean 1 if the en passant capture is performed

  switch (currentplayer){
    case 1:
      if(chosenY==3){//white can only do this capture if the pawn itself is on y=3
        //check if enemy pawn is beside and it has moved for the first time
        if(y==2 && x==chosenX-1 && board[chosenY][x]==B_PAWN && p2_pawn2spaces[x]){
          if(board[y][x]==EMPTY){
            //do the move!
            specialmovepiece(chosenX,chosenY,x,y,W_PAWN);
            board[chosenY][x]=EMPTY;
            emptySquare(x,chosenY);
            return 1;
          }
        }
        else if(y==2 && x==chosenX+1 && board[chosenY][x]==B_PAWN && p2_pawn2spaces[x]){
          if(board[y][x]==EMPTY){
            //do the move!
            specialmovepiece(chosenX,chosenY,x,y,W_PAWN);
            board[chosenY][x]=EMPTY;
            emptySquare(x,chosenY);
            return 1;
          }
        }
      }
    break;

    case 2:
      if(chosenY==4){//black can only do this capture if the pawn itself is on y=4
        //check if enemy pawn is beside and it has moved for the first time
        if(y==5 && x==chosenX-1 && board[chosenY][x]==W_PAWN && p1_pawn2spaces[x]){
          if(board[y][x]==EMPTY){
            //do the move!
            specialmovepiece(chosenX,chosenY,x,y,B_PAWN);
            board[chosenY][x]=EMPTY;
            emptySquare(x,chosenY);
            return 1;
          }
        }
        else if(y==5 && x==chosenX+1 && board[chosenY][x]==W_PAWN && p1_pawn2spaces[x]){
          if(board[y][x]==EMPTY){
            //do the move!
            specialmovepiece(chosenX,chosenY,x,y,B_PAWN);
            board[chosenY][x]=EMPTY;
            emptySquare(x,chosenY);
            return 1;
          }
        }
      }
    break;
  }
  return 0; //requirements not met for en passant
}

bool castling(int x, int y){
  //castling will be handled in a weirdly intuitive way.
  //If the user wishes to castle, he/she must select the king, and then
  //highlight the rook to be castled with. If this is possible, the switch will
  //happen automatically

  switch (currentplayer){
    case 1:
      if ( x==0 && y==7 && !p1_leftRookmoved && !p1_kingMoved ){//left rook
        if(board[y][3]==EMPTY && board[y][2]==EMPTY && board[y][1] == EMPTY){
          if(!checkOnWhite(W_KING,3,y) && !checkOnWhite(W_KING,2,y) && !checkOnWhite(W_KING,4,y)){
            //need to check if king would be in check along the squares
            specialmovepiece(4,7,2,7,W_KING);
            specialmovepiece(0,7,3,7,W_ROOK);
            return 1;
          }
        }
      }
      else if ( x==7 && y==7 && !p1_rightRookmoved && !p1_kingMoved ){//right rook
        if(board[y][5]==EMPTY && board[y][6]==EMPTY){
          if(!checkOnWhite(W_KING,4,y) && !checkOnWhite(W_KING,5,y) && !checkOnWhite(W_KING,6,y)){
            //need to check if king would be in check along the squares
            specialmovepiece(4,7,6,7,W_KING);
            specialmovepiece(7,7,5,7,W_ROOK);
            return 1;
          }
        }
      }
    break;

    case 2:
      if ( x==0 && y==0 && !p2_leftRookmoved && !p2_kingMoved ){//left rook
        if(board[y][2]==EMPTY && board[y][3]==EMPTY && board[y][1] == EMPTY){
          if(!checkOnBlack(B_KING,2,y) && !checkOnBlack(B_KING,3,y) && !checkOnBlack(B_KING,4,y)){
            //need to check if king would be in check along the squares
            specialmovepiece(4,0,2,0,B_KING);
            specialmovepiece(0,0,3,0,B_ROOK);
            return 1;
          }

        }
      }
      else if ( x==7 && y==0 && !p2_rightRookmoved && !p2_kingMoved ){//right rook
        if(board[y][5]==EMPTY && board[y][6]==EMPTY){
          if(!checkOnBlack(B_KING,4,y) && !checkOnBlack(B_KING,5,y) && !checkOnBlack(B_KING,6,y)){
            //need to check if king would be in check along the squares
            specialmovepiece(4,0,6,0,B_KING);
            specialmovepiece(7,0,5,0,B_ROOK);
            return 1;
          }
        }
      }
    break;
  }


  return 0; //castling did not happen
}

bool checkSpecialcases(int x, int y, int piece){
  //input args x,y are the square that the piece will be moved to

  //returns a boolean, to let function in chessfunctions.cpp know that
  //the movment of pieces has already been taken care of here.

  switch (piece){
    case W_PAWN:
      if(y==0){
        promote_to_Queen(x,y);
        dispTips("promotion");
        delay(1000);
        return 1;
      }
      else if(en_passant(x,y)){
        dispTips("enpassant");
        delay(2000);
        return 1;
      }
    break;

    case B_PAWN:
      if(y==7){
        promote_to_Queen(x,y);
        dispTips("promotion");
        delay(1000);
        return 1;
      }
      else if(en_passant(x,y)){
        dispTips("enpassant");
        delay(2000);
        return 1;
      }
    break;

    case W_KING:
      if(castling(x,y)){
        dispTips("castled");
        delay(2000);
        return 1;
      }
    break;

    case B_KING:
      if(castling(x,y)){
        dispTips("castled");
        delay(2000);
        return 1;
      }
    break;
  }
  return 0; //no special cases happened
}
