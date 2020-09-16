import numpy as np
import shape_rw
import random

def compute_face_areas(vertices, faces):

    v0 = vertices[faces[:, 0], :]
    v1 = vertices[faces[:, 1], :]
    v2 = vertices[faces[:, 2], :]
    tmp_cross = np.cross(v0 - v2, v1 - v2)

    areas = 0.5 * np.sqrt(np.sum(tmp_cross * tmp_cross, axis=1))
    return areas
    

def sample_on_trianlge(vertices, faces, vertex_normals, face_normals, num_sample):
    
    areas = compute_face_areas(vertices, faces)
    probabilities = areas / areas.sum()
    weighted_random_indices = np.random.choice(range(areas.shape[0]), size=num_sample, p=probabilities)

    u = np.random.rand(num_sample, 1)
    v = np.random.rand(num_sample, 1)
    w = np.random.rand(num_sample, 1)

    sum_uvw = u + v + w
    u = u / sum_uvw
    v = v / sum_uvw
    w = w / sum_uvw
    
    v0 = vertices[faces[:, 0], :]
    v1 = vertices[faces[:, 1], :]
    v2 = vertices[faces[:, 2], :]
    
    v0 = v0[weighted_random_indices]
    v1 = v1[weighted_random_indices]
    v2 = v2[weighted_random_indices]
    
    n0 = vertex_normals[face_normals[:, 0], :]
    n1 = vertex_normals[face_normals[:, 1], :]
    n2 = vertex_normals[face_normals[:, 2], :]
    
    n0 = n0[weighted_random_indices]
    n1 = n1[weighted_random_indices]
    n2 = n2[weighted_random_indices]

    sampled_v = (v0 * u) + (v1 * v) + (v2 * w)
    sampled_v = sampled_v.astype(np.float32)
    
    sampled_n = (n0 * u) + (n1 * v) + (n2 * w)
    sampled_n = sampled_n.astype(np.float32)
    
    sampled_f_id = weighted_random_indices
    
    return sampled_v, sampled_n, sampled_f_id

def normalize(vertices, max_size=1):
    points_max = np.max(vertices, axis=0)
    points_min = np.min(vertices, axis=0)
    vertices_center = (points_max + points_min) / 2
    points = vertices - vertices_center[None, :]
    max_radius = np.max(np.sqrt(np.sum(points * points, axis=1)))
    vertices = points / max_radius * max_size / 2.0
    return vertices

def mesh2point(input_path, output_path, num_sample):
    
    v, f, vn, fn = shape_rw.read_mesh_obj(input_path)
    v, vn, fid = sample_on_trianlge(v, f, vn, fn, num_sample)
    shape_rw.write_point_ply(v, vn, output_path)
