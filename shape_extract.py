import os
import random

def get_filelist(category_folder):
    
    filepath_list=[]
    filename_list = []
    
    for root, dirs, files in os.walk(category_folder):
        for file in files:
            if os.path.splitext(file)[1] == '.obj':
                filepath_list.append(os.path.join(root, file))
                path_code=root.split('\\')
                shape_code=path_code[len(path_code)-2]
                filename_list.append(shape_code)
    
    return filename_list, filepath_list

    
def shuffle_filelist(filelist):
    
    shuffled_shapelist=copy.copy(shapelist)
    random.shuffle(shuffled_shapelist)
    
    return shuffled_shapelist
            
    
