# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:51:20 2021

@author: hirning
"""
# importing required packages
from pathlib import Path
import shutil
import os
import pickle
import re

with open('dict_subj.pickle', 'rb') as file:
    dict_subj = pickle.load(file)

# =============================================================================
# =============================================================================
# # ENTER SUBJECT ID between 0 and 23 

subj_ID = '25'


# =============================================================================
# =============================================================================

lst_subject_wise_audio = dict_subj[subj_ID]

# path to source directory
src_dir = 'res/audio_full_list/'
  
# path to destination directory
dest_dir = 'res/audio'

# getting all the files in the source directory
files = [item for item in os.listdir(src_dir) if item in lst_subject_wise_audio]
#delete all files in dest_dir
shutil.rmtree(dest_dir)
os.makedirs(dest_dir)
# iterating over all the files in 
# the source directory
for fname in files:
    # copying the files to the 
    # destination directory
    shutil.copy2(os.path.join(src_dir,fname), dest_dir)