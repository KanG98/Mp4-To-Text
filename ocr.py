# Import required packages
import cv2
import pytesseract
from os import listdir
from os.path import isfile, join
import time
from tqdm import tqdm
import difflib
import sys
 
# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.1.0/bin/tesseract'
 
FRAME = 1
SIMILARITY_SCORE = 0.9
FOLDER_NAME = sys.argv[1]

onlyfiles = [f for f in listdir(FOLDER_NAME) if isfile(join(FOLDER_NAME, f))]
onlyfiles.sort()

frame_count = 0
previous_text = ""


# Compare two strings and get their similarity scores. 0 -> not like, 1 -> equal
def string_similarity(a, b):
	return difflib.SequenceMatcher(a=a.lower(), b=b.lower()).ratio()

for filename in tqdm(onlyfiles):

	frame_count += 1
	# Read image from which text needs to be extracted
	img = cv2.imread(FOLDER_NAME + '/' + filename)
 
	# Preprocessing the image starts
 
	# Convert the image to gray scale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
	# Performing OTSU threshold
	ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
 
	# Specify structure shape and kernel size.
	# Kernel size increases or decreases the area
	# of the rectangle to be detected.
	# A smaller value like (10, 10) will detect
	# each word instead of a sentence.
	rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
 	
	# Applying dilation on the threshold image
	dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
 	
	# Finding contours
	contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
												 	cv2.CHAIN_APPROX_NONE)
 	
	# Creating a copy of image
	im2 = img.copy()
 	
	# A text file is created and flushed
	file = open("ocrresult.txt", "a")
	file.write("")
	file.close()
 	
	# Looping through the identified contours
	# Then rectangular part is cropped and passed on
	# to pytesseract for extracting text from it
	# Extracted text is then written into the text file

	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
	 	
		# Drawing a rectangle on copied image
		rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
	 	
		# Cropping the text block for giving input to OCR
		cropped = im2[y:y + h, x:x + w]
	 	
		# Open the file in append mode
		file = open(join(FOLDER_NAME, "ocrresult.txt"), "a")
	 	
		# Apply OCR on the cropped image
		text = pytesseract.image_to_string(cropped)
	 	
		if(string_similarity(text, previous_text) < SIMILARITY_SCORE and text != ""):
			time_sec = frame_count // FRAME
			time_str = time.strftime('%H:%M:%S', time.gmtime(time_sec))
			# Appending the text into file 
			file.write("-" * 20)
			file.write("\n")
			file.write(time_str)
			file.write("\n")
			file.write(text)
			file.write("\n")
			previous_text = text
	 	
		# Close the file
		file.close() 
	
	# convert ocrresult.txt to html 
