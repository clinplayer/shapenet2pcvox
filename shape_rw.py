import numpy as np
import os
from utils import binvox_rw

def read_mesh_obj(path):
    
    vertices = []
    faces = []
    vertex_normals = []
    face_normals = []
    try:
        f = open(path)

        for line in f:
            if line[:2] == "v ":
                strs = line.split()
                v0 = float(strs[1])
                v1 = float(strs[2])
                v2 = float(strs[3])
                vertex = np.array([v0, v1, v2])
                vertices.append(vertex)

            elif line[0] == "f":
                strs = line.split()
                f0 = int(strs[1].split('/')[0])-1
                f1 = int(strs[2].split('/')[0])-1
                f2 = int(strs[3].split('/')[0])-1
                face = np.array([f0, f1, f2])
                faces.append(face)
                
                fn0 = int(strs[1].split('/')[2])-1
                fn1 = int(strs[2].split('/')[2])-1
                fn2 = int(strs[3].split('/')[2])-1
                fn = np.array([fn0, fn1, fn2])
                face_normals.append(fn)
                
            elif line[:2] == "vn":
                strs = line.split()
                n0 = float(strs[1])
                n1 = float(strs[2])
                n2 = float(strs[3])
                normal = np.array([n0, n1, n2])
                vertex_normals.append(normal)

        f.close()
    
    except IOError:
        print(".obj file not found.")

    vertices = np.array(vertices)
    faces = np.array(faces)
    vertex_normals = np.array(vertex_normals)
    face_normals=np.array(face_normals)
    
    return vertices, faces, vertex_normals, face_normals

    
def read_mesh_off(path):
    fopen = open(path, 'r', encoding='utf-8')
    lines = fopen.readlines()
    linecount = 0
    pts = np.zeros((1,3), np.float64)
    faces = np.zeros((1,4), np.int)
    
    p_num=0
    f_num=0
    for line in lines:
        linecount = linecount + 1
        word = line.split()

        if linecount == 1:
            continue

        if linecount == 2:
            p_num = int(word[0])
            f_num = int(word[1])
            pts = np.zeros((p_num,3), np.float)
            faces = np.zeros((f_num, 4), np.int)

        if linecount >= 3 and linecount< 3+p_num:
            pts[linecount-3, :] = np.float64(word[0:3])
        if linecount >=3+p_num:
            faces[linecount-3-p_num] = np.int32(word[1:5])

    fopen.close()
    return pts, faces

    
def load_PC_ply(pc_filepath, expected_point=2000):
    
    fopen = open(pc_filepath, 'r', encoding='utf-8')
    lines = fopen.readlines()
    linecount=0
    
    pts=np.zeros((expected_point,3),np.float64)

    total_point=0
    sample_interval=0
    feed_point_count=0

    start_number = False
    for line in lines:
        linecount=linecount+1
        word=line.split()

        if word[0] == 'element' and word[1] == 'vertex':
            total_point=int(word[2])
            continue

        if start_number == True:
            pts[feed_point_count, :] = np.float64(word[0:3])
            feed_point_count+=1

        if word[0] == 'end_header':
            start_number = True

        if feed_point_count >= expected_point:
            break

    fopen.close()
    return pts


def write_point_off(points, path, colors=None, use_color=False):
    with open(path, "w") as file:
        if use_color:
            file.write("COFF\n")
        else:
            file.write("OFF\n")
        
        file.write(str(int(points.shape[0])) + " 0" + " 0\n")
        for i in range(points.shape[0]):
            file.write(str(float(points[i][0])) + " " + str(float(points[i][1])) + " " + str(float(points[i][2])) + " ")
            if use_color:
                file.write(str(colors[0]) + " " + str(colors[1]) + " " + str(colors[2]))


def write_point_ply(v, n, path):

    with open(path, "w") as file:
        file.write("ply\n")
        file.write("format ascii 1.0\n")
        file.write("comment VCGLIB generated\n")
        file.write("element vertex "+ str(v.shape[0])+"\n")
        file.write("property float x\n")
        file.write("property float y\n")
        file.write("property float z\n")
        file.write("property float nx\n")
        file.write("property float ny\n")
        file.write("property float nz\n")
        file.write("element face 0\n")
        file.write("property list uchar int vertex_indices\n")
        file.write("end_header\n")
        
        for i in range(v.shape[0]):
            file.write(str(float(v[i][0])) + " " + str(float(v[i][1])) + " " + str(float(v[i][2]))+ " " + str(float(n[i][0])) + " " + str(float(n[i][1])) + " " + str(float(n[i][2])) + " \n")

                
def write_mesh_obj(vertexlist, facelist, path):
    with open(path, "w") as file:

        for i in range(vertexlist.shape[0]):
            file.write("v "+str(vertexlist[i][0]) + " " + str(vertexlist[i][1]) + " " + str(vertexlist[i][2]) + "\n")
            
        for i in range(facelist.shape[0]):
            file.write("f " + str(int(facelist[i][0])) + " " + str(int(facelist[i][1])) + " " + \
            str(int(facelist[i][2]))+ " "+ str(int(facelist[i][3])) + " \n")    
    
    
def read_voxel_data(path):
    with open(path, 'rb') as f:
        model = binvox_rw.read_as_3d_array(f)
        return model.data


def check_and_create_dirs(dir_list):
    for dir in dir_list:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(dir+' does not exist. Created.')

            
def read_by_line(path):
    fopen = open(path, 'r', encoding='utf-8')
    lines = fopen.readlines()
    
    data_num=len(lines)
    list=[]
    
    linecount=0
    for line in lines:
        list.append(line.strip('\n'))
        linecount = linecount + 1
        
    fopen.close()
    
    return list

    
def write_by_line(list_data, path):

    with open(path, "w") as file:
        for data in list_data:
            file.write(str(data)+"\n")
        
