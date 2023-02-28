# Sound rating app

## Install with Virtual Env

Create venv

    python3 -m venv sound_rating_venv 

Activate venv
    
    Windows:
    sound_rating_venv\Scripts\activate.bat

    Unix/MacOS:
    source sound_rating_venv/bin/activate

Deacitvate venv
    
    deactivate

## Install modules
    
    pip install -r requirements.txt


## Start app 

    python3 app.py


## Create res audio folders

To run the experiment three audio folder need to be created as subdirectories in res.

1) folder 1: audio

Here the selection of audio sequences for the participants should be copied. 
The randomization.py script and create_subject-wise_audiolist.py can be used to ensure balancing and automatically sort the audio sequences prior to the experiment by using a dictionary and the subject id. 

2) folder 2: audio_full_list

Here all audio sequences should be copied. This folder is needed to run the create_subject-wise_audiolist.py

3) folder 3: audio_test

Here you can copy a suitable test audio sequences to let participants familiarize with the task. 