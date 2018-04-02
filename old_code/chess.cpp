/*
	Chess game final project
*/

#include <Arduino.h>
#include "chessfunctions.h"

//pins for joystick button press
#define JOY1_SEL   2
#define JOY2_SEL   8

//keeps track of current player
//1 is player 1, and 2 is player 2
int currentplayer=1;
//0 is state when game is still going on
int gameover = 0;

int main() {
	setup();

	while(gameover == 0) {

		scroll();


		switch (currentplayer){
			case 1:
			// when joystick is pressed
				if (digitalRead(JOY1_SEL) == 0) {
					while (digitalRead(JOY1_SEL) == LOW) { delay(10); }
					delay(100);
					// a piece is selected, now, move it somewhere
					moveMode();
					if (gameover == 0 ) {
						dispCurrentPlayer(); //updates sidemenu
						dispTips("select");
					}

				}
				break;

			case 2:
				if (digitalRead(JOY2_SEL) == 0) {
					while (digitalRead(JOY2_SEL) == LOW) { delay(10); }
					delay(100);
					// a piece is selected, now, move it somewhere
					moveMode();
					if (gameover == 0 ) {
						dispCurrentPlayer(); //updates sidemenu
						dispTips("select");
					}
				}
				break;

		}

	}

	endGame(gameover);

	Serial.end();
	return 0;
}
