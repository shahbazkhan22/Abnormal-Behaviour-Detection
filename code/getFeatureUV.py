# coding:utf8
import cv2
from poscal import poscal
from poscalflow import poscalflow
import scipy.io
import numpy as np
from weight_matrix import *
from split import *
font=cv2.FONT_HERSHEY_COMPLEX
data = scipy.io.loadmat('../ref_data/u_seq_abnormal.mat')
u_seq_abnormal = data['u_seq_abnormal']
data = scipy.io.loadmat('../ref_data/v_seq_abnormal.mat')
v_seq_abnormal = data['v_seq_abnormal']

def getFeaturesUV(realPos,u,v):
    n = realPos.shape[0]
    if realPos.max()==0:
        data = np.zeros((1,2))
    else:
        data = np.zeros((n,2))
        for i in range(n):
            data[i][0]=u[int(realPos[i][1]):int(realPos[i][0]),int(realPos[i][3]):int(realPos[i][2])].mean()
            data[i][1]=v[int(realPos[i][1]):int(realPos[i][0]),int(realPos[i][3]):int(realPos[i][2])].mean()
    return data

def main():
    weight = Weight_matrix().get_weight_matrix()
    cv2.imshow('img105',u_seq_abnormal[:,:,105]*weight)

if __name__ == "__main__":
    main()
