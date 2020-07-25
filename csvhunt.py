################################################################################################################################
#
# Program to check if files listed in a csv file are in folder name 0, and move the matching files to folder name 1. 
#
################################################################################################################################
# imports

import csv
import os
import shutil
import re
import glob

############## function definitions #########

_to_esc = re.compile(r'\s|[]()[]')

def _esc_char(match):
	return '\\'+match.group(0)

def my_escape(name):
	return _to_esc.sub(_esc_char, name)
  
############### main routine ################

def main():
    csv_file = r"sample.csv"
    from_folder = r"0/"  #source folder name is 0
    to_folder = r"1/"    #destination folder name is 1
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        filereader = csv.reader(f)
        for row in filereader:
            file_name = row[1]        # check this out, your CSV file may not have files in index 1, so check it to make sure.
            file_name = my_escape(file_name)
            
            from_filename = os.path.join(from_folder, file_name)
            to_filename = os.path.join(to_folder,file_name)
            print("Moving from ",from_filename," to ", to_folder)
            
            try:
            	os.system("mv"+" "+from_filename+" "+to_folder)
            except:
            	print("Can't find the file...\n")
              
main()
