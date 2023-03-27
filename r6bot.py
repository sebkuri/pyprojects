import pyautogui
import pydirectinput
from pynput import mouse, keyboard
from time import sleep
import waiting


print("R6 Renown farm bot. Press Enter to begin. Hold down the down arrow to stop macro.")

wantsToStart = False
wantsToContinue = True
pydirectinput.FAILSAFE = True


def on_press(key):
	if key == keyboard.Key.enter:
		global wantsToStart
		wantsToStart = True

	if key == keyboard.Key.down:
		global wantsToContinue
		wantsToContinue = False


def bot():
	while(wantsToContinue):
		pydirectinput.click(66,524)
		pydirectinput.press('enter')
		sleep(1)

		if (wantsToContinue == False):
			break

		pydirectinput.click(603, 405)
		pydirectinput.press('enter')
		sleep(1)

		if (wantsToContinue == False):
			break

		pydirectinput.click(603, 405)
		pydirectinput.press('enter')
		sleep(1)

		if (wantsToContinue == False):
			break

		pydirectinput.click(496, 249)
		pydirectinput.press('enter')
		pydirectinput.press('esc')
		sleep(1)

		if (wantsToContinue == False):
			break

		pydirectinput.click(499, 157)
		pydirectinput.press('enter')
		sleep(1)

		if (wantsToContinue == False):
			break


def starting_function():
	if wantsToStart == False:
		return False
	else:
		return True


klistener = keyboard.Listener(on_press = on_press)
klistener.start()




while(True):
	try:
		waiting.wait(starting_function, timeout_seconds = 60)
		bot()
		if(wantsToContinue == False):
			break
	except waiting.exceptions.TimeoutExpired as e:
		break

print("Program terminated. Enjoy the renown")
	





