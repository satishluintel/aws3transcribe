AWS S3 Automatic File Upload, buckets create and delete, and AWS Transcribe (Text only response) 


____________________________________________________________________________________________________________________________________________________

There are two folders,

1. audios  ( Here you keep all the audios in WAV format you want to transcribe. If you do not have audio files in WAV format, there are further steps described below how to fix them.)

2. text  ( In this folder, all the transcribed text would appear automatically. Please do not stop the script unless all files are transcribed. )

____________________________________________________________________________________________________________________________________________________

Dependencies installation ( Please run the following commands in your LINUX shell to install dependencies)

```
sudo apt-get update

sudo apt install python3-pip

pip3 install boto3
```
____________________________________________________________________________________________________________________________________________________


If you do not have any buckets set up,
run `create_buckets.py` by 

`python3 create_buckets.py`

You can choose any bucket name as long as it is lowercase characters.

Similarly, if you want to get rid of some buckets you have run delete_buckets.py by,

`python3 delete_buckets.py`

This will list all the available buckets and you just need to enter the name of the bucket to delete. 

______________________________________________________________________________________________________

Before you run the app using the following command, consider to review the points from 1 to 7.

```
`python3 app.py` 

```

1. Please make sure that the 'audios' folder only contains the audios you want to upload to S3 because the script will upload everything in this folder to Amazon S3, although it will ask if you are sure to upload. If you press any other keys than 'y' then the script will transcribe whatever is in the S3 bucket you have selected. For testing, there is an audio file inside the folder. 

2. Please make sure that text folder is empty to avoid confusions from future transcriptions. There is one sample transcription text file for your reference.

3. Please put your credentials in the keys.py file. This is IMPORTANT, else the script won't run at all.

4. The sleep timer is set to 5 seconds, you can change it to 1 to n seconds in app.py.

5. Make sure you make the region name same in create_buckets.py and app.py, if you want to make your code more flexible, you can always change the keys.py file to add general configurations for your app.

6. The delete_buckets.py does not delete empty buckets. You can upload a test file and then delete the entire bucket.

7. If you have audios to process follow the steps in the next section to change them to wav format.


Sometimes transcript breaks in the middle and keeps you waiting. To debug this, go to your S3 bucket and select all files that have been already transcribed, and DELETE them at once. Also, comment the upload code in app.py so that you do not double upload audios you already uploaded.

_________________________________________________________________________________________________________________________
CHANGING FILES TO WAV FORMAT
_________________________________________________________________________________________________________________________

Case 1. You have files in mp3 format only. 

You can change the app.py code like below,if your files are in mp3 format, 
Replace
```
transcribe.start_transcription_job(TranscriptionJobName = job_name, Media = {'MediaFileUri': S3_URL }, MediaFormat = 'wav', LanguageCode='en-US')

```
by

```
transcribe.start_transcription_job(TranscriptionJobName = job_name, Media = {'MediaFileUri': S3_URL }, MediaFormat = 'mp3', LanguageCode='en-US')

```
and run the app.py now.


Case 2. Case.1 is not general. So, if you want this source code to run 'as it is', then before you run the app.py file, follow the following steps to convert audios in audio folder to wav format using ffmpeg by following the codes below,

```
sudo apt install ffmpeg
```
after installing ffmpeg, change the files to wav format, mono channel format,
```
ffmpeg -i file_in_your_uploading_folder.mp3 -y -ar 44100 -ac 1 audios/target_file_name.wav
```

NOTICE: This is a very painstaking task as you could have files in thousands. 
To automate this, I have added another script here,  
python3 convert_to_wav.py

This script will take in any file name, even with spaces or brackets like ( ), or solid brackets. Before using this script make sure you add all your "to be converted files" in 'processing' folder, and then run the command below,

```
 python3 convert_to_wav.py

```
This single command will convert all your audios in ANY format to wav format and put them in audios folder. After this you can runt the main script app.py.

___________________________________________________________________________________________________________

FOR CUSTOM SERVICE CONTACT : company@learngaroo.com
Please put Subject: AWS
___________________________________________________________________________________________________________
