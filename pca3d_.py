#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 20:11:33 2021

@author: victoria
"""
import os
import numpy as np
from sklearn.decomposition import PCA
#from sklearn.linear_model import l
import matplotlib.pyplot as plt

np.random.seed(66)
os.chdir("files")
ffiles={}

data_for_pca=[]
names_for_pca=[]
shapes=set()
for file in os.listdir():
    if file[-4:]==".npz" and "Ensayo" in file:
        
        for name, (xx,yy,zz) in np.load(file).items():
            print(name)
            if "Blanco" in name:
                ffiles[name]="Blanco"
            else:
                ffiles[name]=" ".join(name.split()[2:])
            shapes.add((xx.shape, yy.shape ,zz.shape))
            data_for_pca.append(zz.flatten())
            names_for_pca.append(name)
assert len(shapes)==1
shapes=list(shapes)
colori_={value:np.random.random(3) for value in ffiles.values()}
colori={key:colori_[ffiles[key]] for key in ffiles.keys() }
fig,ax=plt.subplots(subplot_kw={"projection":"3d"})
X=np.array(data_for_pca)
pca=PCA(n_components=3)
low_dim=pca.fit_transform(X)
for i,(name,treat) in enumerate(zip(names_for_pca,low_dim)):
    ax.scatter(*treat, label=ffiles[name], color=colori[name])
plt.legend()
plt.show()


fig,ax=plt.subplots(ncols=2, nrows= int((pca.n_components + 1)/2), figsize=(30,30))
ax=ax.flatten()

ax[0].contourf(xx,yy,pca.mean_.reshape(shapes[0][2]))
ax[0].set_title("Mean")

for i in range(pca.n_components):
    ax[i + 1].contourf(xx,yy, pca.components_[i].reshape(shapes[0][2]))
    ax[i + 1].set_title("PC{}".format(i+1))
plt.show()



