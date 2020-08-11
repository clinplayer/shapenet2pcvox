import numpy as np
from pyntcloud import PyntCloud
from utils import binvox_rw


def point2voxel(intput_path, output_path, grid_x, grid_y, grid_z):
    
    '''
    input_path: the file path to the point cloud (*.ply)
    input_path: the file path to save the voxel file (*.binvox)
    grid_x, grid_y, grid_z: the size of the voxel grid
    '''

    cloud = PyntCloud.from_file(intput_path)

    voxelgrid_id = cloud.add_structure("voxelgrid", n_x=grid_x, n_y=grid_y, n_z=grid_z)
    voxelgrid = cloud.structures[voxelgrid_id]

    x_cords = voxelgrid.voxel_x
    y_cords = voxelgrid.voxel_y
    z_cords = voxelgrid.voxel_z

    voxel = np.zeros((grid_x, grid_y, grid_z)).astype(np.bool)

    for x, y, z in zip(x_cords, y_cords, z_cords):
        voxel[x][y][z] = True

    with open(output_path, 'wb') as f:
        v = binvox_rw.Voxels(voxel, (grid_x, grid_y, grid_z), (0, 0, 0), 1, 'xyz')
        v.write(f)