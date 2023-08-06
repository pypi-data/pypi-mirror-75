#!/usr/bin/env python
# coding: utf-8

# In[66]:


import strym
from strym import strymread
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
# importing shutil module  
import shutil 


# ## Replacement script

# In[33]:


source_folder = "/home/ivory/CyverseData/JmscslgroupData/safwanelmadani/PandaData/" # Safwan's Folder Path
destination_folder = "/home/ivory/CyverseData/JmscslgroupData/PandaData/" # Rahul's Folder Path
replacement_text_file = []

folderlist = glob.glob(source_folder+"*")
for datafolder in folderlist:
    replacement_text = glob.glob(datafolder+"/*back_in_time.txt")
    for f in replacement_text:
        replacement_text_file.append(f)


# In[ ]:


original_file_list = []
new_file_src_list = []
for txt_file in replacement_text_file:
    handler = open(txt_file, "r")
    
    # Name value-pair splot
    first_line = handler.readline()
    original = first_line.split(':')
    
    # Get the file name
    original_file_name  = original[1].strip()
    
    # Path of the file to be deleted from `rahulbhadani` folder
    original_file_path = destination_folder + '_'.join(original_file_name.split("-")[0:3]) + "/" + original_file_name
    original_file_list.append(original_file_path)
    
    second_line = handler.readline()
    new = second_line.split(':')
    new_file_name  = new[1].strip()
    new_src_file_path = source_folder + '_'.join(original_file_name.split("-")[0:3]) + "/" + new_file_name
    new_file_src_list.append(new_src_file_path)
    
    new_dst_file_path = destination_folder + '_'.join(new_file_name.split("-")[0:3]) + "/" 
    
    print(first_line)
    print(second_line)
    
    try:
        P = os.remove(original_file_path)
    except FileNotFoundError:
        print("{} not found".format(original_file_path))
                         
    print("File deleted: {}".format(original_file_path))
    print("File to be copied from: {}".format(new_src_file_path))
    print("File to be copied to: {}\n------------------".format(new_dst_file_path))
    dest = shutil.copy(new_src_file_path, new_dst_file_path) 
    
    


# ## Test if everything is alright

# In[77]:


parentfolder = "/home/ivory/CyverseData/JmscslgroupData/PandaData/" # Put the parent folder from your system.
dbcfile = '/home/ivory/VersionControl/Jmscslgroup/strym/examples/newToyotacode.dbc'
csvlist = []
folderlist = glob.glob(parentfolder+"*")
for datafolder in folderlist:
    csvlisttmp = glob.glob(datafolder+"/*.csv")
    for f in csvlisttmp:
        csvlist.append(f)


# In[ ]:


problem_file = []
for csv in csvlist:
    print("\nReading the CSV file {}".format(csv))
    r = strymread(csvfile=csv, dbcfile=dbcfile)
    if r.success is True:
        continue
    else:
        if hasattr(r, 'dataframe'):
            if 'Time' in r.dataframe.columns:
                if np.any(np.diff(r.dataframe['Time'].values) < 0.0):
                    print("Warning: Timestamps are not monotonically increasing. Further analysis is not recommended.")
                    problem_file.append(csv)


# In[80]:


if(len(problem_file)) == 0:
    print("Success")
else:
    print("Failure")


# In[ ]:




