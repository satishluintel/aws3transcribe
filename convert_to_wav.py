import csv
import os
import shutil
import re
import glob

_to_esc = re.compile(r'\s|[]()[]')

def _esc_char(match):
	return '\\'+match.group(0)

def my_escape(name):
	return _to_esc.sub(_esc_char, name)


_to_esc = re.compile(r'\s|[]()[]')

os.chdir("processing")
for file in os.listdir(os.getcwd()):
	file=my_escape(file)
	print(file)
	filename,file_extension = os.path.splitext(file)
	print(filename)
	filename=filename+".wav"
	print(filename)
	dest_file=os.path.join("../audios/",filename)
	print(dest_file)
	os.system("ffmpeg -i "+file+" -y -ar 44100 -ac 1 "+dest_file)
