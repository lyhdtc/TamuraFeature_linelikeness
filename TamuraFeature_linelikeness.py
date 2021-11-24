import cv2
import numpy as np
import math

# original paper
# https://ieeexplore.ieee.org/document/4309999
def __tamura_linelikeness(gray_img, theta, dist):
    n = 16
    h = gray_img.shape[0]
    w = gray_img.shape[1]
    pi = 3.1415926
    dcm = np.zeros((8,n,n))
    # 8 direction
    dir = np.float32([   [[1,0,-dist],   [0,1,-dist]],
                    [[1,0,-dist],   [0,1,0]],
                    [[1,0,dist],    [0,1,0]],
                    [[1,0,0],       [0,1,-dist]],
                    [[1,0,0],       [0,1,dist]],
                    [[1,0,dist],    [0,1,-dist]],
                    [[1,0,dist],    [0,1,0]],
                    [[1,0,dist],    [0,1,dist]]
                 ])
    cooccurrence_matrixes = []
    for i in range(8):
        # move matrix_theta along direction above
        cooccurrence_matrixes.append(cv2.warpAffine(theta, dir[i], (w,h)))
        
    for m1 in range(1,n):
        for m2 in range(1,n):
            for d in range(8):
                # judgement, if 2 pixel(original, moved pic) in the same range, return true
                # sorry for split judge function, because I don't know how to write them together(I'm new in python)
                m_theta_bottom = ( theta>=((2*(m1-1)*pi)/(2*n)) )
                m_theta_top = (theta<(((2*(m1-1)+1)*pi)/(2*n)) )  
                m_theta = np.logical_and(m_theta_bottom, m_theta_top)
                
                m_ccoccurrence_matrixes_bottom = ( cooccurrence_matrixes[d]>=((2*(m2-1)*pi)/(2*n)))
                m_ccoccurrence_matrixes_top = ( cooccurrence_matrixes[d]<(((2*(m2-1)+1)*pi)/(2*n)))
                m_ccoccurrence_matrixes = np.logical_and(m_ccoccurrence_matrixes_bottom, m_ccoccurrence_matrixes_top)
                
                dcm_matrix = np.logical_and(m_theta, m_ccoccurrence_matrixes)
                dcm_matrix = dcm_matrix.astype(int)
                dcm[d][m1][m2] = np.sum(dcm_matrix)                
    matrix_f = np.zeros((1,8))
    matrix_g = np.zeros((1,8))
    
    # calculate the angle of 8 direction, and sum them up
    for i in range(n):
        for j in range(n):
            for d in range(8):
                matrix_f[0][d] += dcm[d][i][j]*(math.cos((i-j)*2*pi/n))
                matrix_g[0][d] += dcm[d][i][j]   
    # set in range (0,1)       
    matrix_res = matrix_f/matrix_g
    # return the max one ,can describe how this picture texture's "direction" move
    res = np.max(matrix_res)
    return res	