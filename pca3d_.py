#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 20:11:33 2021

@author: Eduardo Gonik
"""
import os
import re
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


plt.style.use('ggplot')


np.random.seed(32)
os.chdir("files")
ffiles={}

data_for_pca=[]
names_for_pca=[]
shapes=set()
for file in os.listdir():
    if file[-4:]==".npz" and "Ensayo" in file:
        
        for name, (xx,yy,zz) in np.load(file).items():
            zz=zz[xx<750].reshape(xx.shape[0],-1)
            yy=yy[xx<750].reshape(xx.shape[0],-1)
            xx=xx[xx<750].reshape(xx.shape[0],-1)
            if "Blanco" in name:
                ffiles[name]=name
            else:
                ffiles[name]=" ".join(name.split()[2:])
            shapes.add((xx.shape, yy.shape ,zz.shape))
            data_for_pca.append(zz.flatten())
            names_for_pca.append(name)
assert len(shapes)==1
shapes=list(shapes)
colori_={value:np.random.random(3) for value in ffiles.values()}
colori={key:colori_[ffiles[key]] for key in ffiles.keys() }
scaler=StandardScaler()
X=scaler.fit_transform(data_for_pca)

pca=PCA(n_components=3)
low_dim=pca.fit_transform(X)
dict_for_coef={}
if pca.n_components<=3:
    fig,ax=plt.subplots(subplot_kw={"projection":"3d"}, figsize=(30,30))
    for i,(name,treat) in enumerate(zip(names_for_pca,low_dim)):
        ax.scatter(*treat, label=ffiles[name], color=colori[name])
        dict_for_coef[name]=treat
    plt.title('Representacion de los datos para {} PC'.format(pca.n_components))
    humberto = plt.gca().get_legend_handles_labels()[1][:len(set(ffiles.values()))]
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    plt.legend(humberto)
    plt.show()
    
else:
    for i,(name,treat) in enumerate(zip(names_for_pca,low_dim)):
        dict_for_coef[name]=treat
    


fig,ax=plt.subplots(ncols=2, nrows= int(np.ceil((pca.n_components + 1)/2, )), figsize=(30,30))
ax=ax.flatten()

ax[0].contourf(xx,yy,pca.mean_.reshape(shapes[0][2]))
ax[0].set_title("Mean")

for i in range(pca.n_components):
    ax[i + 1].contourf(xx,yy, pca.components_[i].reshape(shapes[0][2]))
    ax[i + 1].set_title("PC{}, varianza explicada {:.2f} % ".format(i+1, pca.explained_variance_ratio_[i]*100 ))

plt.suptitle('Representacion gráfica de todos los componentes, {:.2f} % de varianza total explicada'.format(sum(pca.explained_variance_ratio_*100)))
plt.show()



data={value:[] for value in set(ffiles.values())}
listeria=sorted(list(dict_for_coef))
for value in listeria:
    trt=re.findall(r"(?<=Dia\s\d\s).*",value)
    if trt:
        data[trt[0]].append(dict_for_coef[value])
    else:
        data[value].append(dict_for_coef[value])
    



width=.5

fig,ax = plt.subplots(1,1, figsize=(30,15))  
plt.title(r"$\Delta_{coef}$ para cada PC para cada tratamiento")    
labels=["PC{}".format(i + 1) for i in range(pca.n_components)]
x=np.arange(len(labels))
for key,val in data.items():
    if len(val)==1:
        plt.bar(x, val[0], width=width, label=key, color=colori_[key], alpha=.7)
    else:
        plt.bar(x, height=val[-1] - val[0] ,width=width, label=key, color=colori_[key], alpha=.7)
ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.axhline(0, color='black', linewidth=2)
plt.legend()
plt.show()


     

for key, values in data.items():
    fig,ax = plt.subplots(1,1, figsize=(30,15))  
    for i,value in enumerate(values):
        plt.bar(x, value, width, label='dia {}'.format(i), alpha=.7)
        plt.title(key)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    plt.legend()
    plt.show()