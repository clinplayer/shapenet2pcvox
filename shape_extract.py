import os
import random

def get_filelist(category_folder):
    
    filepath_list=[]
    filename_list = []
    
    for root, dirs, files in os.walk(category_folder):
        for file in files:
            if os.path.splitext(file)[1] == '.obj':
                filepath_list.append(os.path.join(root, file))
                shape_name=os.path.basename(file).split('.')[0]
                filename_list.append(shape_name)
    
    return filename_list, filepath_list

    
def shuffle_filelist(filelist):
    
    shuffled_shapelist=copy.copy(shapelist)
    random.shuffle(shuffled_shapelist)
    
    return shuffled_shapelist
            
    
