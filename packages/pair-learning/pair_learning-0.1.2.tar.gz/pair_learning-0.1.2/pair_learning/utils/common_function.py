import numpy as np
import torch


def angle_to_coord(angle):
    x = angle_to_cos(angle)
    y = angle_to_sin(angle)
    return x, y


def angle_to_cos(angle):
    return np.cos(np.radians(angle))


def angle_to_sin(angle):
    return np.sin(np.radians(angle))


def pairwise_distance(x, y=None):
    '''
    Input: x is a Nxd matrix
           y is an optional Mxd matirx
    Output: dist is a NxM matrix where dist[i, j] is the square norm between x[i, :] and y[j, :]
            if y is not given then use 'y = x'.
    i.e. dist[i,j] = ||x[i,:] - y[j,:]|| ^ 2
    '''
    x_norm = (x**2).sum(1).view(-1, 1)
    if y is not None:
        y_norm = (y**2).sum(1).view(1, -1)
    else:
        y = x
        y_norm = x_norm.view(1, -1)
    dist = x_norm + y_norm - 2.0 * torch.mm(x, y.T)
    dist[dist != dist] = np.inf # to deal with "nan" values
    return torch.clamp(dist, 0.0, np.inf)