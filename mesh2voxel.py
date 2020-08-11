import os
import subprocess
import sys


def mesh2voxel(input_path, output_path, voxsize):
    
    cmd = 'utils\\binvox -aw -d {0} -cb -dc {1}'.format(voxsize, input_path)
    basename = os.path.splitext(input_path)[0]
    ret = subprocess.call(cmd)
    
    if ret != 0:
        print("error", i, file)
        return
    
    default_name = basename +'.binvox'    
    
    cp_file_cmd='copy '+ default_name + ' ' + output_path
    print(cp_file_cmd)
    os.system(cp_file_cmd)
    
    rm_file_cmd='del '+ default_name
    os.system(rm_file_cmd)

