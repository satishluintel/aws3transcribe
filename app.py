########################################################################
#
# CODE TO CREATE/DELETE BUCKETS
# UPLOAD FILES IN S3 BUCKET, AMAZON WEB SERVICES
# AND TRANSCRIBE...
#
# CODE BY SATISH LUINTEL, 2020. 
# MIT LICENSE
#
########################################################################
from keys import access_key, secret_access_key
import boto3
import os
import json
import time
import urllib
import random
import string
#####################################################################################
# CONFIG REGION NAME
rname= 'ap-southeast-1'
#####################################################################################

# SETTING A S3 CLIENT, IF YOU WANT TO SPECITY REGION, DO UNDER region_name
client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
response=client.list_buckets()
print("Found "+ str(len(response["Buckets"])) + " bucket(s) \n" )

# FETCH ALL AVAILABLE BUCKETS UNDER YOUR S3 INSTANCE
for x in range(len(response["Buckets"])):
	print(x," ",response["Buckets"][x]["Name"] )  #print bucket names 

# SELECT A BUCKET TO UPLOAD ALL THE AUDIO FILES YOU HAVE IN AUDIOS FOLDER.
y = input("\nSelect a bucket to upload ( in case you do not have a bucket, use create_buckets.py file to create one )....\n")
selected = response["Buckets"][int(y)]["Name"] #selecting a particular bucket
print("Selected ", str(selected) )
list = boto3.resource('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key, region_name = rname)
bucket = list.Bucket(str(selected))

# UPLOADING FROM LOCAL FOLDER audios TO REMOTE BUCKET OF YOUR CHOICE
os.chdir('audios')

asking = input("\n Are you sure to upload all the contents of AUDIOS folder to S3 Bucket? [y/n] ")

if asking == 'y':
	for file in os.listdir(os.getcwd()):
		upload_file_bucket = selected
		upload_file_key = str(file)
		print("Uploading File "+ upload_file_key)
		client.upload_file(file, upload_file_bucket, upload_file_key)
else: 
	print("You have rejected the upload. Transcribing whatever left in the bucket....")

#################################################################################
# EVERY JOB SHOULD BE UNIQUE, HENCE WE GENERATE RANDOM STRINGS OF 12 CHARACTERS

def randomString(stringLength=12):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

################################################################################

# PRINTING ALL FILES IN THE FOLDER 
print("There are following files in the your Bucket : " + str(selected) )
for file in bucket.objects.all():
	list = file.key
	print(list)  #printing all files in the selected bucket

print("#\n#\n#\n#\n#\n#\n#\n")

##################################################################################
#
#
#                             TRANSCRIPTION STARTS HERE 
#                          Results are saved in text folder.
#                      
#
os.chdir('../')  
#get back one directory, until now we were in 'audios', now we need to get into text to write files 



for file in bucket.objects.all():
	list = file.key
	file_name = str(list).replace('.wav', '') 
	
	create_file = open('text/'+ str(file_name+".txt"), 'w+')
	create_jsonfile = open('jsonresponse/'+ str(file_name+".json"), 'w+')
	transcribe = boto3.client('transcribe', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key, region_name = 'ap-southeast-1')
	job_name = randomString()
	S3_URL = 's3://'+str(selected)+'/'+str(list)
	print("Fetching file from...",S3_URL)
	transcribe.start_transcription_job(TranscriptionJobName = job_name, Media = {'MediaFileUri': S3_URL }, MediaFormat = 'wav', LanguageCode='en-US')
	print("on job ", job_name)

	counter = 10

	while True:

		status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
		if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
			response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
			data = json.loads(response.read())
			
			#print(data)
			text = data['results']['transcripts'][0]['transcript']
			create_file.write(text)
			create_file.close()

			#writing a json file for further processing
			create_jsonfile.write(str(data))
			create_jsonfile.close()

			print("----------------------------------------------------------------------")
			print("-\n")
			print("Job "+ job_name + " finished. Written to text File ", create_file)
			print("-\n")
			print("----------------------------------------------------------------------")

			#delete the transcription job from AWS transcribe logs.
			response = transcribe.delete_transcription_job(TranscriptionJobName=job_name)

			break

		if status['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
			print("WARNING ! FAILED !", job_name)

		counter = counter + 10.0
		print('In Progress, you waited '+ str(counter) +" seconds, pausing for 10 more seconds...")
		time.sleep(10)

####################################################################################

