# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 20:42:37 2021

@author: hirning
"""
import os 
import numpy as np 
import pandas as pd
import pickle
import random

def randomization(N, file_path):
    for subj_id in range(0,N):
        print('Start', subj_id)
        
        new_lst_pos = []
        new_lst_neg = []
        new_lst_neu = []
        
        if subj_id == 0:
            
            lst_pos = os.listdir(file_path + 'positive_funny/')
            lst_neg = os.listdir(file_path + 'negative/')
            lst_neu = os.listdir(file_path + 'neutral/')
            dict_pos = dict(zip(lst_pos, list(np.repeat(0,len(lst_pos)))))
            dict_neg = dict(zip(lst_neg, list(np.repeat(0,len(lst_neg)))))
            dict_neu = dict(zip(lst_neu, list(np.repeat(0,len(lst_neu)))))
            dict_subj = {}
            count_ratings = {}
        else: 
            
            dict_pos = count_ratings['dict_pos']
            dict_neg = count_ratings['dict_neg']
            dict_neu = count_ratings['dict_neu']
            lst_pos = [item for item in list(dict_pos.keys()) if dict_pos[item] < 12 and dict_pos[item] <= np.array(list(dict_pos.values())).mean()]
            lst_neg = [item for item in list(dict_neg.keys()) if dict_neg[item] < 12 and dict_neg[item] <= np.array(list(dict_neg.values())).mean()]
            lst_neu = [item for item in list(dict_neu.keys()) if dict_neu[item] < 12 and dict_neu[item] <= np.array(list(dict_neu.values())).mean()]
    
        if (subj_id % 2) == 0:
            n_pos = 5 
            n_neg = 6
            n_neu = 8
        else:
            n_pos = 6 
            n_neg = 5
            n_neu = 7
        done = False
        while not done:
            while len(new_lst_pos) < n_pos:
                if len(lst_pos) > 0:    
                    new_item = random.choice(lst_pos)
                    lst_pos.remove(new_item)
                    new_lst_pos.append(new_item)
                elif len(new_lst_pos) < n_pos: 
                    new_item = random.choice([item for item in dict_pos.keys() if item not in new_lst_pos])
                    new_lst_pos.append(new_item)
                else: 
                    break
                
            for item in new_lst_pos:                
                dict_pos[item] = dict_pos[item] + 1
                
            while len(new_lst_neg) < n_neg:
                if len(lst_neg) > 0:    
                    new_item = random.choice(lst_neg)
                    lst_neg.remove(new_item)
                    new_lst_neg.append(new_item)
                elif len(new_lst_neg) < n_neg: 
                    new_item = random.choice([item for item in dict_neg.keys() if item not in new_lst_neg])
                    new_lst_neg.append(new_item)
                else: 
                    break
                
            for item in new_lst_neg:                
                dict_neg[item] = dict_neg[item] + 1
            
            while len(new_lst_neu) < n_neu:
                if len(lst_neu) > 0:    
                    new_item = random.choice(lst_neu)
                    lst_neu.remove(new_item)
                    new_lst_neu.append(new_item)
                elif len(new_lst_neu) < n_neu: 
                    new_item = random.choice([item for item in dict_neu.keys() if item not in new_lst_neu])
                else: 
                    break
                
            for item in new_lst_neu:                
                dict_neu[item] = dict_neu[item] + 1        
            done = True
        
            
        lst_audio_files = new_lst_neu + new_lst_pos + new_lst_neg
        dict_subj[subj_id] = lst_audio_files
        count_ratings['dict_pos'] = dict_pos
        count_ratings['dict_neg'] = dict_neg
        count_ratings['dict_neu'] = dict_neu
           
        print('Finished', subj_id)
        
    return count_ratings, dict_subj

file_path = 'normalized'
save_path = 'GAUDIE_Experiment'
if not os.path.exists(save_path):
    os.makedirs(save_path)
    
count_ratings, dict_subj = randomization(24, file_path)

with open(os.path.join(save_path, 'count_ratings.pickle'), 'wb') as file:
    pickle.dump(count_ratings, file, protocol=pickle.HIGHEST_PROTOCOL)
    
with open(os.path.join(save_path, 'dict_subj.pickle'), 'wb') as file:
    pickle.dump(dict_subj, file, protocol=pickle.HIGHEST_PROTOCOL)
    
