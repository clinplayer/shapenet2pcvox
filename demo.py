from mesh2voxel import mesh2voxel
from point2voxel import point2voxel
from mesh2point import mesh2point
import shape_rw
from shape_extract import get_filelist
import argparse


def parse_args():

    """parse input arguments"""
    parser = argparse.ArgumentParser(description='demo to convert shapenet')
    
    parser.add_argument('--shapenet_root', type=str, default='shapenet', help='the root directory of shapenet dataset')
    parser.add_argument('--category_name', type=str, default='03001627', help='the name of category')
    parser.add_argument('--output_root', type=str, default='shapenet_convert', help='directory to save the results')

    args = parser.parse_args()
    
    return args

if __name__ == "__main__":


    args = parse_args()
    
    category_folder=args.shapenet_root+'\\'+args.category_name+'\\'
    output_root=args.output_root
    
    filename_list, filepath_list = get_filelist(category_folder)
    
    
    #convert to point
    pc_output_folder=output_root+'\\'+args.category_name+'\\pc\\'
    shape_rw.check_and_create_dirs([pc_output_folder])
    
    for i in range(len(filename_list)):
        input_path=filepath_list[i]
        output_path=pc_output_folder+filename_list[i]+'.ply'
        mesh2point(input_path, output_path, 2000)
        
        
    #convert the sampled point to voxel
    pcvox_output_folder=output_root+'\\'+args.category_name+'\\pc_vox\\'
    shape_rw.check_and_create_dirs([pcvox_output_folder])
    
    for i in range(len(filename_list)):
        input_path=pc_output_folder+filename_list[i]+'.ply'
        output_path=pcvox_output_folder+filename_list[i]+'.binvox'
        point2voxel(input_path, output_path, 32, 32, 32)
        
    
    #convert to voxel
    vox_output_folder=output_root+'\\'+args.category_name+'\\vox\\'
    shape_rw.check_and_create_dirs([vox_output_folder])
    
    for i in range(len(filename_list)):
        input_path=filepath_list[i]
        output_path=vox_output_folder+filename_list[i]+'.binvox'
        mesh2voxel(input_path, output_path, 64)