import pyautogui
from pynput import mouse, keyboard


print("Mouse cooordinate program. Press esc to end.")


n = 1

def on_click(x, y, button, pressed):
	if button == button.left and pressed:
		global n
		print("Mouse click number "+str(n)+" = "+str(pyautogui.position()))
		n += 1



def on_press(key):
	if key == key.esc:
		mlistener.stop()
		klistener.stop()
		print("Program terminated.")

klistener=keyboard.Listener(on_press = on_press) 
klistener.start()

with mouse.Listener(on_click = on_click) as mlistener:
			mlistener.join()



	












