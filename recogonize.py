# -*- coding: utf-8 -*-
from __future__ import division
import cv2
import numpy as np
from matplotlib import pyplot as plt


counti=[]
countj=[]
count=0
countarray=[]
percent=[]
d=['one','two','three','func','four','five','six','clear','seven','eight','nine','cancel','dzero','zero','star','confirm']
#下面的数组是用来算磨损程度的分母，是由手动构造的无损键盘得出的，详见报告
model=[0.10820588235294118, 0.15578539107950873, 0.14508726567550098, 0.17995072374499538, 0.09787610619469027, 0.1294612467178839, 0.14499659632402995, 0.15685956539869342, 0.0902122641509434, 0.11494401824590504, 0.14057640472734811, 0.16605749283809149, 0.1308128078817734, 0.134655984409679, 0.1173334055107454, 0.15286410646583964]
def dealarray(a,len):#处理得到的数组
    tmp=a[0]
    m=[]
    m.append(tmp)
    for i in range(len-2):
        if a[i+1]-tmp>100:
            tmp=a[i+2]
            m.append(a[i+1])
            m.append(tmp)
    m.append(a[-1])
    return m

def jSums(i,j,src):#统计每一行黑像素点数
    trans=0
    count=0
    while trans<j:
        if src[i,trans]==0:
            count=count+1
        trans=trans+1
    return count

def iSums(i,j,src):#统计每一列黑像素点个数
    traa=0
    countt=0
    while traa<i:
        if src[traa,j]==0:
            countt=countt+1
        traa=traa+1
    return countt

img1=cv2.imread('1.png',0)
blur=cv2.medianBlur(img1,5)
th1=cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
th1=cv2.medianBlur(th1,5)
th1=cv2.medianBlur(th1,5)

for i in range(0,th1.shape[0]-1):#hang
    p=jSums(i,th1.shape[1],th1)
    counti.append(p)
for j in range(0,th1.shape[1]-1):#lie
    m=iSums(th1.shape[0],j,th1)
    countj.append(m)

for f in range(10):
    countj[f]=0
    counti[f]=0
row=[]
col=[]
for lengthi in range(len(counti)):
    if counti[lengthi-1]<5 and counti[lengthi]>5:
        row.append(lengthi)
    if counti[lengthi-1]>5 and counti[lengthi]<5:
        row.append(lengthi)
for lengthj in range(len(countj)):
    if countj[lengthj-1]<10 and countj[lengthj]>10:
        col.append(lengthj)
    if countj[lengthj-1]>10 and countj[lengthj]<10:
        col.append(lengthj-1)

#print row
row=dealarray(row,len(row))
col=dealarray(col,len(col))

# print row,col
for i in range(0,7,2):
    for j in range(0,7,2):
        count=0
        tmp=th1[row[i]:row[i+1],col[j]:col[j+1]]
        for m in range(row[i+1]-row[i]):
            for n in range(col[j+1]-col[j]):
                if tmp[m,n]==0:
                    count=count+1
        pe=float(count)/float(tmp.size)
        percent.append(pe)
        # countarray.append(count)

# print countarray
for i in range(len(percent)):
    # pe=np.float32(countarray[i])/np.float32(model[i])
    res=float(abs(model[i]-percent[i]))/float(model[i])
    print d[i],":",('%.2f%%' % (res * 100))

#cv2.imwrite("new2.png",th1)



