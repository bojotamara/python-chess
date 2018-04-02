#ifndef _SPECIALCASES_H
#define _SPECIALCASES_H

extern bool p1_kingMoved;
extern bool p1_leftRookmoved;
extern bool p1_rightRookmoved;

extern bool p2_kingMoved;
extern bool p2_leftRookmoved;
extern bool p2_rightRookmoved;

extern bool p1_pawn2spaces[9];
extern bool p2_pawn2spaces[9];
//last index holds boolean which lets program know if the player has played
//his/her turn. Other indices represent pawns, and the corresponding index is
//changed to 1 if the player moved his/her pawn 2 spaces

void promote_to_Queen(int x, int y);

bool checkSpecialcases(int x, int y, int piece);

bool castling(int x, int y);

bool en_passant(int x, int y);

#endif
