from mss import mss
import mss.tools
import numpy as np
import cv2
import easyocr
import PIL
from PIL import Image
import pyautogui
import keyboard
import time



#Takes the tuple returned by the location function and converts it into a calibrated dictionary that can be inputted into MSS to screen capture lab names
def tupleModifier(labsTuple):
	step1 = list(labsTuple)
	placeholder = step1[0] 
	step1[0] = step1[1]
	step1[1] = placeholder

	mssDict = {"top": step1[0], "left": 42, "width":600, "height":26}

	return mssDict

#Takes the tuple returned by the location function and converts it into a calibrated dictionary that can be inputted into MSS to screen capture # of iterations
def tupleModifier2(iterationTuple):
	step1 = list(iterationTuple)
	placeholder = step1[0] 
	step1[0] = step1[1]
	step1[1] = placeholder

	mssDict = {"top": step1[0]-10, "left": step1[1]-100, "width":75, "height":50}

	return mssDict


#Image scaling function to increase the pixels of the input image
def set_image_dpi(file_path, file_name, factor):
	im = cv2.imread(file_path)
	im = cv2.resize(im, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)
	cv2.imwrite(file_name, im)



def find_on_screen(needleImg):
	with mss.mss() as sct:
		screenshot = sct.shot()
		needleImg = cv2.imread(needleImg)
		haystackImg = cv2.imread('monitor-1.png')
		res =  res = cv2.matchTemplate(haystackImg, needleImg, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		return max_loc




def lab_function():
	#Extract patient data image from screen using MSS

	with mss.mss() as sct:

		monitor = {"top": 169, "left": 106, "width": 600, "height": 73}
		testImg = sct.grab(monitor)
		output = "patient_data_img.png"

		mss.tools.to_png(testImg.rgb, testImg.size, output = output)


	#Cropping extracted patient data image into sub-images

	patient_data_img = cv2.imread("patient_data_img.png")
	crop_1 = patient_data_img[0:45, 0:600].copy()
	cv2.imwrite("crop1.png", crop_1)
	crop_2 = patient_data_img[41:73, 30:75].copy()
	cv2.imwrite("crop2.png", crop_2)
	crop_3 = patient_data_img[37:73, 75:189].copy()
	cv2.imwrite("crop3.png", crop_3)
	crop_4 = patient_data_img[37:73, 183:265].copy()
	cv2.imwrite("crop4.png", crop_4)

	#Preprocessing step 1: increase pixel amt of sub images using set_image_dpi

	images = ["crop1.png", "crop2.png", "crop3.png", "crop4.png"]
	i = 1
	for image in images:
		set_image_dpi(image, f"crop{i}processed.png", 1.2)		
		i+=1

	#Perform OCR on the images, then add the OCR phrases into a list

	processedimgs = ["crop1processed.png", "crop2processed.png", "crop3processed.png", "crop4processed.png"]
	patient_data = ["1","2","3","4"]
	z = 0
	for img in processedimgs:
		patient_data[z] = str((reader.readtext(img, detail = 0)))
		z+=1

	patient_data[1] = str(patient_data[1])[5:6] 

	#Print the list 
	print(patient_data)

	#This section begins lab pulling. Hotkey to ctrl+f the labs page, then labs is input into the parameter field
	pyautogui.hotkey("ctrl","f")
	time.sleep(0.05)
	pyautogui.press('backspace')
	pyautogui.write("labs", interval = 0.01)

	iterationPreLocation = find_on_screen('ctrlfanchor.png')



	#This section screen captures and performs OCR on the number of times the word "labs" is found in the page on the ctrl+f popup box. 
	with mss.mss() as sct:
		iterationImgLocation = tupleModifier2(iterationPreLocation)
		iterationImg = sct.grab(iterationImgLocation)
		output = "iterationImg.png"
		mss.tools.to_png(iterationImg.rgb, iterationImg.size, output = output)
	
	set_image_dpi("iterationImg.png", "processedIterationImg.png", 5)

	iterationText = reader.readtext("processedIterationImg.png", detail = 0)

	#The number of times is saved as the variable labIterationCount, to determine how many times a lab name needs to be read

	print(iterationText)
	labIterationCount = ((str(iterationText)[4:len(str(iterationText))]).split("'", 1))[0]
	print("Iteration Count = "+str(labIterationCount))
	


	x = 1
	listOfLabs = []
	confidence = 0.95
	downCoords = pyautogui.locateCenterOnScreen('ctrlfdown.png', confidence = 0.9)
	#The lab reading function loops using labIterationCount in order to successfully pull every lab that the patient has
	while x < int(labIterationCount):
		pyautogui.click(downCoords)

		#The location of the highlighted word "labs" is found as a tuple.

		#labsLocationTuple = pyautogui.locateOnScreen("labshighlight.png", confidence = confidence)
	
		#while labsLocationTuple == None:
			#confidence -= 0.01
			#labsLocationTuple = pyautogui.locateOnScreen("labshighlight.png", confidence = confidence)

		labsLocationTuple = find_on_screen("labshighlight.png")
		leftLabsLocationDict = tupleModifier(labsLocationTuple)
		
		#Screenshot is taken of the lab name corresponding to the highlighted "labs" text on the right
		with mss.mss() as sct:
			labimg = sct.grab(leftLabsLocationDict)
			output = f"labname{x}.png"
			mss.tools.to_png(labimg.rgb, labimg.size, output = output)

		#Preprocessing of lab name screenshot
		set_image_dpi(f"labname{x}.png", f"labprocessed{x}.png", 1.2)

		#OCR reading of lab name
		cutlab1 = str((reader.readtext(f"labprocessed{x}.png", detail = 0))).split("task", 1)[0]
		cutlab2 = cutlab1.split("[", 1)[1]
		listOfLabs.append(cutlab2)

		#Clicking the check mark next to the lab to remove it from the printing list

		pyautogui.click(35,(leftLabsLocationDict["top"]+15))
		x+=1


	#lab list is printed
	for lab in listOfLabs:
		print(lab)

	#Inputs data into lab sheet then pull up the print screen.
	pyautogui.click(443, 19)
	pyautogui.click(837, 463, clicks = 3)
	pyautogui.write(patient_data[0])
	pyautogui.click(791, 486, clicks = 3)
	pyautogui.write(patient_data[3])
	pyautogui.click(928, 485, clicks = 3)
	pyautogui.write(patient_data[2])
	pyautogui.click(1003, 484, clicks = 3)
	pyautogui.write(patient_data[1])
	pyautogui.click(863, 805, clicks = 3)

	for lab in listOfLabs:
		pyautogui.write(lab)
		pyautogui.write("   |||   ")
	
	pyautogui.click(437, 539)
	pyautogui.hotkey("ctrl", "p")
	time.sleep(3)


	#pyautogui.click(pyautogui.locateCenterOnScreen("print.png"))






#Following section has setup details, as well as waits for user input of enter to start OCR on screen.
print("Please wait until OCR is initialized.")
reader = easyocr.Reader(['en'])
print("OCR has been initialized. Press ctrl+enter to begin.")


while True:
    if keyboard.is_pressed("ctrl+enter"):
        lab_function()
        #Things left to automate: Uncheck Consults, print patient info + prescriptions + imaging, 

    elif keyboard.read_key() == "esc":
    	print("Program terminated.")
    	break


