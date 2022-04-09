import sys
import os
import datetime 
import time 
from dominate import document
from dominate.tags import *

FOLDER_NAME = sys.argv[1]
FILE_NAME = 'ocrresult.txt'
WORKING_DIR = os.path.join(os.getcwd(), FOLDER_NAME)
FILE_DIR = os.path.join(WORKING_DIR, FILE_NAME)
SEPERATOR = "-"*20
FRAME = 1

def group_paragraphs(lines):
	# organize ocr txt report to timestamp, text pairs
	dic = {}

	if(len(lines) == 0):
		return dic

	timestamp = ""
	for i, line in enumerate(lines):
		if(line.strip() == SEPERATOR):
			timestamp = lines[i+1]
		else: 
			if(timestamp not in dic):
				dic[timestamp] = {"text": ""}
			dic[timestamp]["text"] += line
			
	return dic	
			

def generate_html(dic):
	
	#map images to corresponding timestamp
	image_paths = os.listdir(WORKING_DIR)
	dic_timestamp_in_sec = []
	
	#filter out image paths that the timestamp are not in dic as timestamp
	for key in dic:
		ftr = [3600,60,1]
		second = sum([a*b for a,b in zip(ftr, map(int,key.split(':')))])
		second //= FRAME
		dic_timestamp_in_sec.append(str(second).zfill(6))
	
	clean_image_paths = []
	for second in dic_timestamp_in_sec:
		frame = second * FRAME
		for image in image_paths:
			image_frame = image[-10:-4]
			if(frame == image_frame):
				clean_image_paths.append(image)
				break
			
				
	#add image paths to dic
	for i, key in enumerate(dic):
		dic[key]["image_path"] = clean_image_paths[i]
	

	#build html
	with document(title="OCR Results") as doc:
		for timestamp, content in dic.items():
			div(img(src=content["image_path"], height='300px'), _class='photo')
			div(p(content["text"]))
			
	with open(WORKING_DIR+'/'+FOLDER_NAME+'.html', 'w') as file:
		file.write(doc.render())
		
		
with open(FILE_DIR, 'r') as file:
	lines = file.readlines()
	dic = group_paragraphs(lines)
	generate_html(dic)


	
