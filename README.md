AWS S3 Automatic File Upload, buckets create and delete, and AWS Transcribe (Text only response) 

There are two folders,
1. audios
2. text

In audios, you keep all the audios you want to transcribe through Amazon Transcribe.
In text, all the transcribed text would appear automatically.

Things to consider before running the script:
1. Please make sure that you are keeping 'audios' folder updated because the script will upload everything in this folder to Amazon S3. For testing, there is an audio file inside the folder. 
2. Please make sure that text folder is empty so that you receive transcripts for exactly what was kept in 'audios' folder. There is one sample transcription text file for your reference.
3. Please put your credentials in the keys.py file
4. The sleep timer is set to 5 seconds, you can change it to 1 to n seconds.
5. Make sure you make the region name same in create_buckets.py and app.py, if you want to make your code more flexible, you can always change the keys.py file to add general configurations for your app.
6. The delete_buckets.py does not delete empty buckets. You can upload a test file and then delete the entire bucket.


To run the app,

`python3 app.py` 

WARNING : If you files are not in wav format, please change your audio files to wav using ffmpeg OR you can change the app.py code like below,if your files are in mp3 format, 
Replace
```
transcribe.start_transcription_job(TranscriptionJobName = job_name, Media = {'MediaFileUri': S3_URL }, MediaFormat = 'wav', LanguageCode='en-US')

```
by

```
transcribe.start_transcription_job(TranscriptionJobName = job_name, Media = {'MediaFileUri': S3_URL }, MediaFormat = 'mp3', LanguageCode='en-US')

```
and things will work. 

If you want this source code to run 'as it is', then before you run the app.py file, follow the following steps to convert all audios in audio folder to wav format using ffmpeg by following the codes below
```
sudo apt install ffmpeg
```
after installing ffmpeg, change the files to wav format, mono channel format,
```
ffmpeg -i file_in_your_uploading_folder.mp3 -y -ar 44100 -ac 1 audios/target_file_name.wav
```
(to be updated soon)






___________________________________________________________________________________________________________

Dependencies installation ( Please run the following commands in your shell to install dependencies)

```
sudo apt-get update

sudo apt install python3-pip

pip3 install boto3
```

If you do not have any buckets set up,
run `create_buckets.py` by 

`python3 create_buckets.py`

You can choose any bucket name as long as it is lowercase characters.

Similarly, if you want to get rid of some buckets you have run delete_buckets.py by,

`python3 delete_buckets.py`

This will list all the available buckets and you just need to enter the name of the bucket to delete. 
