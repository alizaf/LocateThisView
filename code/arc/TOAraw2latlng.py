Xyread.py                                                                                           000644  000765  000024  00000004362 12561163524 013307  0                                                                                                    ustar 00alizaf                          staff                           000000  000000                                                                                                                                                                         from skimage import feature
from skimage import color
from skimage import segmentation

from sklearn.cluster import KMeans
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import skimage
import skimage.io
import matplotlib.pylab as plt
import random
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import pandas as pd
from skimage import data
from skimage import img_as_float
from skimage.morphology import reconstruction
from os.path import isfile, join
import itertools, shutil, os
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def createarray(filepath):
    p = skimage.io.imread(filepath)
    pgray = color.rgb2gray(p)
    X = pgray
    X = feature.canny(pgray,sigma=2)


    return X.flatten()

# read images
def getfeatures(dirpath, filenames):
	features_array = []
	nn=0
	# rands = np.random.random_integers(0,1500,100)
	domain = filenames # [filenames[i] for i in rands]
	print domain
	for i,f in enumerate(domain):
		temp = createarray(dirpath +f)
		print temp
		features_array.append(temp)
		#print len(features_array)
	features_array = np.array(features_array)    
	print('read_images done')
	return features_array

def readsplit(pathname, csv2read):
    df = pd.read_csv(pathname+csv2read)
    testindex = random.sample(df.index, int(df.shape[0])/5)
    testdf = df.loc[testindex]
    df.drop(testindex, inplace = True)

    valindex = random.sample(df.index, int(df.shape[0])/3)
    valdf = df.loc[valindex]
    df.drop(valindex, inplace = True)
    filenames = df['successnames']

    Xtrain = getfeatures(pathname,df.successnames )
    ytrain = np.array(df.reset_index()['label']).astype(np.int32)

    Xval = getfeatures(pathname,valdf.successnames )
    yval = np.array(valdf.reset_index()['label']).astype(np.int32)

    Xtest = getfeatures(pathname,testdf.successnames )
    ytest = np.array(testdf.reset_index()['label']).astype(np.int32)
    train_val_test = [Xtrain, Xtest, ytrain, ytest]#Xval, yval, Xtest, ytest]
    return train_val_test
pathname = './photodb11/'
readsplit(pathname,'imagedata.csv')
	# features_array = features_array*0.99
	# pca = PCA(n_components=5000)
	# feature_pca = pca.fit_transform(features_array)
                                                                                                                                                                                                                                                                              collection.py                                                                                       000644  000765  000024  00000031127 12561541505 014204  0                                                                                                    ustar 00alizaf                          staff                           000000  000000                                                                                                                                                                         import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter
import shutil
from os import listdir
from os.path import isfile, join
from math import radians, cos, sin, asin, sqrt
import numpy as np
import re
import requests
import urllib
from flask import Flask
from flask import request
import time
import random
from random import randint
import pdb
from sklearn.neighbors import NearestNeighbors

random.seed(100)
class getview(object):
    """Pool Layer of a convolutional network """
    def __init__(self, rawdatafile, SW, NE, where2store):
        self.dfraw = pd.read_csv(rawdatafile)
        self.SW = SW
        self.NE = NE
        self.where2store = where2store
        if not os.path.exists(self.where2store):
            os.mkdir(self.where2store)
        else:
            print 'Directory exists!'
            ans = raw_input('continue?! [y/n]')
            if ans == 'n' : raise
        # self.dmin = dmin
        # self.meshsize = meshsize
        # self.picsize = picsize
    # def raw2latlng(self):
        df_latlng = self.dfraw['Business_Location'].map(lambda x: str(x).split()[-2:])
        df_lat = df_latlng.map(lambda x: x[0][1:-1])
        df_lng = df_latlng.map(lambda x: x[-1][0:-1])
        df_latlng = pd.concat([df_lat,df_lng],1)
        df_latlng.columns = ['lat', 'lng']
        df = df_latlng.convert_objects(convert_numeric=True)
        
        df=df[(df.lat<NE[0]) & (df.lat>SW[0])]
        df=df[(df.lng<NE[1]) & (df.lng>SW[1])]

        self.df_latlng = df

    def info2name(self, lat, lng, angle, label):
        return 'lat%.6f_lng%.6fang%03dlab%02d.png' %(lat,lng,angle,label)

    def name2info(self, filename):
        filename = re.findall(r"[^\W\d_]+|\d+.\d+",filename)
        nameinfo = dict()
        for i in range (len(filename)-1):
            nameinfo[filename[i]] = filename[i+1]
        return nameinfo

    def slicepics(self, pathname,  SWslice, NEslice, newpath = None):
        onlyfiles = [ f for f in listdir(pathname) if (isfile(join(pathname,f))) & (len(f)>=31) ]
        validfiles = [f for f in onlyfiles if (float(f[3:12])<NEslice[0]) & (float(f[3:12])>SWslice[0])
             & (float(f[16:27])<NEslice[1]) & (float(f[16:27])>SWslice[1])]
        if newpath:
            if not os.path.exists(newpath):
                os.mkdir(newpath)
    #         moved = [os.rename(pathname+f, newpath+f) for f in validfiles]
            copied = [shutil.copy(pathname+f, newpath+f) for f in validfiles]

        self.pics4slice = validfiles

    #function that gets list of file names and return dataframe with lat lng as columns
    def filenameplot(filenames,plot = 0):
        latlist = [float(filenames[i][3:12]) for i in range(len(filenames))]
        lnglist = [float(filenames[i][16:27]) for i in range(len(filenames))]
        namelist = [filenames[i] for i in range(len(filenames))]


        df = pd.DataFrame(np.transpose([latlist, lnglist,namelist]), columns=['lat','lng','filename'])
        if plot == 1:
            df.plot('lng','lat',kind='scatter',s = 0.3, figsize= [5,5])
        return df
    def haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km
    def creatdistinct(self,dmin):
        self.dmin = dmin
        df=self.df_latlng[['lat','lng']]
        
        yy = df['lat'].values
        xx = df['lng'].values
        p = df[['lat', 'lng']].values
        p1 = []
        # nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(p)
        # distances, indices = nbrs.kneighbors(p)
        # nearestd = (np.array(distances[:,1]*100) < dmin)
        # p1 = p[nearestd]
        # safelist=[]
        # for i, ind in enumerate(indices[:,1]):
        #     if nearestd[i] & (indices[i,0] not in safelist):
        #             safelist.append(indices[i,0])
            # else:
            #     safelist.append(indices[i,1])
        # for i in range(len(yy)-1):
        #     for j in range (i+1,len(yy)):
        #         d = self.haversine(xx[i],yy[i],xx[j],yy[j])
        #         # d = np.linalg.norm([xx[i] - xx[j], yy[i] - yy[j]])*100.
        #         # print d1 - d
        #         if d < self.dmin:
        #             p1.append(p[i])
        #             break
        dx = self.haversine(self.SW[1],self.SW[0],self.NE[1],self.SW[0])
        dy = self.haversine(self.SW[1],self.SW[0],self.SW[1],self.NE[0])
        meshsiz = [int(dx/dmin),int(dy/dmin)]
        latlinspace = np.linspace(self.SW[0],self.NE[0],meshsiz[0]+1)
        lnglinspace = np.linspace(self.SW[1],self.NE[1],meshsiz[1]+1)
        self.df_filt = pd.DataFrame(df.iloc[0,:], columns=[df.columns])
        self.df_alter = pd.DataFrame(df.iloc[0,:], columns=[df.columns])
        # self.df_filt.columns = [['lat','lng']]
        mesh = np.array(np.meshgrid(latlinspace, lnglinspace))
        # self.df_filt['label'] = 0
        for i in range(meshsiz[1]):
            if i>0 :print i*meshsiz[0]+j,'out of', meshsiz[0]*meshsiz[1]
            for j in range(meshsiz[0]):
                y_ne = mesh[:,i+1,j+1][0]
                y_sw = mesh[:,i,j][0]
                x_ne = mesh[:,i+1,j+1][1]
                x_sw = mesh[:,i,j][1]
                # pdb.set_trace()
                self.df_alter.loc[i*(meshsiz[0]-1)+j] = [np.mean([y_ne,y_sw]), np.mean([x_ne,x_sw])]
                mask = (df.lat<mesh[:,i+1,j+1][0]) & (df.lat>mesh[:,i,j][0]) \
                & (df.lng<mesh[:,i+1,j+1][1]) & (df.lng>mesh[:,i,j][1])
                ixlist = df[mask]
                # pdb.set_trace()
                # for ii in ixlist.index:
                if ixlist.shape[0] > 0:
                    self.df_filt.loc[i*(meshsiz[0]-1)+j] = df.loc[ixlist.index[0]]



        # if p1 != []:
        #     dfp1 = pd.DataFrame(p1)
        #     dfp1.columns = df.columns
        #     df_filtered = pd.concat([df, dfp1])
        #     df_filtered = df_filtered.reset_index(drop=True)
        #     df_filtered_gpby = df_filtered.groupby(list(df_filtered.columns))
        #     #get index of unique records
        #     idx = [x[0] for x in df_filtered_gpby.groups.values() if len(x) == 1]
        #     #filter
        #     df_filtered = df_filtered.reindex(idx)
        self.df_filt.plot('lng','lat',kind='scatter',figsize=[15,10],s=0.5)

            # self.df_filt = df_filtered
           # pdb.set_trace()
        # else:
            # self.df_filt = df
        # print self.df_labeled
    def single_query(self, lat, lng, angle, label, ii):
        #getfile = urllib.URLopener()
        # print lat,longit
        link='https://maps.googleapis.com/maps/api/streetview?size=%dx%d&location=%.6f,%.6f&\
        fov=90&heading=%d&pitch=10&key=AIzaSyCsHPCM6nVYgvItOGnmXq17FhvKtjOp44k'%(self.picsize[0],\
         self.picsize[1], lat,lng,angle)
        print self.info2name(lat, lng, angle, label)

        pathname = self.where2store + self.filename
        urllib.urlretrieve(link, pathname)
        if os.stat(pathname).st_size in self.errsize:
            os.remove(pathname)
            print 'attempt:', self.attempts
            # ntries += 1
            # return nsucs, ntries
        else:
            try:
                print '%d success!:%d %d Cum Success = %.3f' %(ii, self.nsucs, self.ntries, float(self.nsucs)/self.ntries)
            except ZeroDivisionError:
                print '%d success! Cum Success = %.3f' %(ii, 0)
            self.success = True
            # return nsucs, ntries
    def relabel(self,dfl):
        latlinspace = np.linspace(self.SW[0],self.NE[0],self.meshsize[0]+1)
        lnglinspace = np.linspace(self.SW[1],self.NE[1],self.meshsize[1]+1)
        mesh = np.array(np.meshgrid(latlinspace, lnglinspace))
        # print mesh
        self.df_goal['label'] = 0
        for i in range(self.meshsize[0]):
            for j in range(self.meshsize[1]):
                # pdb.set_trace()

                mask = (self.df_goal.lat<mesh[:,i+1,j+1][0]) & (self.df_goal.lat>mesh[:,i,j][0]) \
                & (self.df_goal.lng<mesh[:,i+1,j+1][1]) & (self.df_goal.lng>mesh[:,i,j][1])
                ixlist = self.df_goal[mask]
                # if ixlist.shape[0] > 0:
                self.current_label += 1
                for ii in ixlist.index:
                    # pdb.set_trace()
                    # print self.current_label# (i*(self.meshsize[0]-1))+j + 1
                    self.df_goal.loc[ii,'label'] = self.current_label#(i*(self.meshsize[0]-1))+j + 1
    
    def query(self, meshsize, picsize,angles,errsize,nattempts, full = False):
        # df = pd.read_csv('processed.csv')
        # df = df.drop(0,axis=0)
        self.errsize = errsize
        self.meshsize = meshsize
        self.picsize = picsize
        self.current_label = 0
        # latlinspace = np.linspace(self.SW[0],self.NE[0],self.meshsize[0]+1)
        # lnglinspace = np.linspace(self.SW[1],self.NE[1],self.meshsize[1]+1)
        if full:
            self.df_goal = self.df_alter
        else:
            self.df_goal = self.df_filt
        self.relabel(self.df_goal)
        # mesh = np.array(np.meshgrid(latlinspace, lnglinspace))
        # self.df_goal['label'] = 0
        # for i in range(self.meshsize[0]):
        #     for j in range(self.meshsize[1]):
        #         # pdb.set_trace()
        #         mask = (self.df_goal.lat<mesh[:,i+1,j+1][0]) & (self.df_goal.lat>mesh[:,i,j][0]) \
        #         & (self.df_goal.lng<mesh[:,i+1,j+1][1]) & (self.df_goal.lng>mesh[:,i,j][1])
        #         ixlist = self.df_goal[mask]
        #         for ii in ixlist.index:
        #             self.df_goal.loc[ii,'label'] = (i*(self.meshsize[0]-1))+j + 1
        # for i in range(len(sortedfiles)-1):
        #     dflabeled = pd.concat([dflabeled,sortedfiles[i+1]],axis=0)
        self.df_labeled = self.df_goal
        # self.df_labeled .to_csv(where2store)
        self.df_labeled = self.df_labeled.reset_index()

        self.nsucs = 0
        self.ntries = 0
        # self.df_success = pd.DataFrame()
        # angles = [45, 90, 135, 180, 225, 180, 315, 360]#, 45, 120, 135, 210, 225, 300, 315]

        nfiles = os.stat(self.where2store).st_nlink
        successnames = []
        for i in range(self.df_labeled.shape[0]):#nfiles+1,42867)nfiles+10001):#range(df.shape[0]):
            [ang] = random.sample(angles, 1)
            self.attempts = 0
            # for ang in angle:
            # if isinthebox(df.iloc[i,1],df.iloc[i,2], SW, NE):
            self.df_success = pd.DataFrame()
            self.filename = self.info2name(self.df_labeled.lat[i],self.df_labeled.lng[i], ang, self.df_labeled['label'][i])
            # pdb.set_trace()
            if os.path.exists(self.where2store+self.filename):
                successnames.append(self.filename)
                self.ntries +=1
                self.nsucs +=1
                print self.nsucs, 'already exists:', self.filename
                # pdb.set_trace()
            else:
                eps = self.dmin/100
                self.success = False
                # self.single_query(filename, self.df_labeled.lat[i],self.df_labeled.lng[i]\
                #         ,ang, self.df_labeled.label[i], i)
                for self.attempts in range(nattempts):
                    self.single_query(self.df_labeled.lat[i]+eps*(np.random.rand()-1)\
                        ,self.df_labeled.lng[i]+eps*(np.random.rand()-1),ang, self.df_labeled.label[i], i )
                    if self.success:
                        self.nsucs +=1
                        self.ntries +=1
                        successnames.append(self.filename)
                        break
                    elif(self.attempts == (nattempts-1)):
                        successnames.append('')
                        self.ntries +=1
                        print 'could not retrive:  %s' %self.filename
                time.sleep(0.0)
            # print len(successnames)
        # pdb.set_trace()
        self.df_labeled['successnames'] = successnames
        nexisting = 0
        self.df_folder= pd.DataFrame()
        if os.path.exists(self.where2store+'folderdata.csv'):
            self.df_folder = self.df_labeled.append(pd.read_csv(self.where2store+'folderdata.csv')[self.df_labeled.columns]\
                ,ignore_index=True)       
            self.df_folder.drop_duplicates('successnames', inplace=True)
        else:
            self.df_folder = self.df_labeled
        self.df_folder.to_csv(self.where2store+'folderdata.csv')




                                                                                                                                                                                                                                                                                                                                                                                                                                         get_pics.py                                                                                         000644  000765  000024  00000003106 12556344756 013657  0                                                                                                    ustar 00alizaf                          staff                           000000  000000                                                                                                                                                                         import requests
import urllib
from flask import Flask
from flask import request
#import ipdb
import numpy as np
import pandas as pd
import time
import os

df = pd.read_csv('test1.csv')
def single_query(lat, longit, angle,ii):
    #getfile = urllib.URLopener()
    # print lat,longit
    link='https://maps.googleapis.com/maps/api/streetview?size=200x200&location=%.6f,%.6f&fov=90&heading=%d&pitch=-0.76\
    &key=AIzaSyCsHPCM6nVYgvItOGnmXq17FhvKtjOp44k'%(lat,longit,angle)
    print link
    #     https://maps.googleapis.com/maps/api/streetview?size=400x400&location=40.720032,-73.988354&fov=90&heading=235&pitch=10
    filename = './photodb/lat%f_lng%f%d.png' %(lat,longit,ii)
    urllib.urlretrieve(link, filename)
    if os.stat(filename).st_size < 3500 or os.stat(filename).st_size==7850:
        os.remove(filename) 
    #response = requests.get(link)#, params=payload)
    #return response

SW=[37.70339999999999,-122.527]
NE=[37.812,-122.3482]


SN1=np.linspace(SW[0],NE[0],4)
WE1=np.linspace(SW[1],NE[1],4)
latlong=[]

meshy = np.linspace(SN1[-2],SN1[-1],60)
meshx = np.linspace(WE1[-2],WE1[-1],60)

angle = 45

# for i in range(df.shape[0]):
#     single_query(df.iloc[i,1],df.iloc[i,2],angle,i)
#     time.sleep(0.0)
for i in range(len(meshx)): 
    for j in range(len(meshy)):
        single_query(meshy[j],meshx[i],angle,i*59+j)
        time.sleep(0.2)

        # latlong.append([c['geometry']['location'] for c in json1['results']])
#if response.status_code != 200:
#    print 'WARNING', response.status_code
#else:

# if __name__ == '__main__':
#     app.run(host='', port=8080, debug=True)
                                                                                                                                                                                                                                                                                                                                                                                                                                                          get_pics_business.py                                                                                000644  000765  000024  00000005216 12560570500 015555  0                                                                                                    ustar 00alizaf                          staff                           000000  000000                                                                                                                                                                         import requests
import urllib
from flask import Flask
from flask import request
#import ipdb
import numpy as np
import pandas as pd
import time
import os
from random import randint

def single_query(lat, longit, angle,ii,nsucs,ntries):
    #getfile = urllib.URLopener()
    # print lat,longit
    link='https://maps.googleapis.com/maps/api/streetview?size=300x400&location=%.6f,%.6f&fov=90&heading=%d&pitch=10&key=AIzaSyCsHPCM6nVYgvItOGnmXq17FhvKtjOp44k'%(lat,longit,angle)
    print link
    #     https://maps.googleapis.com/maps/api/streetview?size=400x400&location=40.720032,-73.988354&fov=90&heading=235&pitch=10
    filename = './photodb6/lat%.6f_lng%.6fang%03d_%d.png' %(lat,longit,angle,ii)
    urllib.urlretrieve(link, filename)
    if os.stat(filename).st_size == 3762 or os.stat(filename).st_size==7850:
        os.remove(filename)
        ntries += 1
        return nsucs, ntries
    else:
        try:
            print '%d success!:%d %d Cum Success = %.3f' %(ii, nsucs, ntries, float(nsucs)/ntries)
        except ZeroDivisionError:
            print '%d success! Cum Success = %.3f' %(ii, 0)
        nsucs += 1
        ntries += 1
        return nsucs, ntries
    #response = requests.get(link)#, params=payload)
    #return response

def collectpics(csvfilename, sw,ne, meshgrid)
    df = pd.read_csv('latlong_distinct.csv')
    df = df.drop(0,axis=0)

    nsucs = 0
    ntries = 0

    SWsf=[37.70339999999999,-122.527]
    NEsf=[37.812,-122.3482]
    SW1 = [37.785087, -122.423623]
    NE1 = [37.811130, -122.382081]
    latlinspace = np.linspace(SW1[0],NE1[0],6)
    lnglinspace = np.linspace(SW1[1],NE1[1],6)
    #latlong=[]
    mesh = np.array(np.meshgrid(latlinspace, lnglinspace))
    SW = SW1#mesh[:,5,5]
    NE = NE1#mesh[:,10,10]
    def isinthebox(lat, longit, SW, NE):
        if (lat < NE[0]) & (lat > SW[0]) & (longit < NE[1]) & (longit > SW[1]):
            return True
        else:
            return
    angles = [45,135,225,315]#, 45, 120, 135, 210, 225, 300, 315]
    nfiles = os.stat('photodb6/').st_nlink
    for i in range(df.shape[0]):#nfiles+1,42867)nfiles+10001):#range(df.shape[0]):
        if isinthebox(df.iloc[i,1],df.iloc[i,2], SW, NE):
            nsucs, ntries = single_query(df.iloc[i,1],df.iloc[i,2],angles[randint(0,3)],i, nsucs, ntries)
            time.sleep(0.0)

# for i in range(len(meshx)): 
#     for j in range(len(meshy)):
#         single_query(meshy[j],meshx[i],angle,i*59+j)
#         time.sleep(0.2)

        # latlong.append([c['geometry']['location'] for c in json1['results']])
#if response.status_code != 200:
#    print 'WARNING', response.status_code
#else:

if __name__ == '__main__':
    app.run(host='', port=8080, debug=True)
                                                                                                                                                                                                                                                                                                                                                                                  imageread.py                                                                                        000644  000765  000024  00000001131 12560161321 013750  0                                                                                                    ustar 00alizaf                          staff                           000000  000000                                                                                                                                                                         import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

from skimage import data
from skimage import img_as_float
from skimage.morphology import reconstruction
def dialate(image):
    # Convert to float: Important for subtraction later which won't work with uint8
    #image = skimage.io.imread('./photodb3/lat37.758877_lng-122.414508ang045_61137.png', as_grey=True)
    image = gaussian_filter(image, 3)

    seed = np.copy(image)
    seed[1:-1, 1:-1] = image.min()
    mask = image

    dilated = reconstruction(seed, mask, method='dilation')
    return dilated                                                                                                                                                                                                                                                                                                                                                                                                                                       raw2latlong.py                                                                                      000644  000765  000024  00000015204 12560612775 014312  0                                                                                                    ustar 00alizaf                          staff                           000000  000000                                                                                                                                                                         import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import os
from collections import Counter
import shutil
from os import listdir
from os.path import isfile, join
from math import radians, cos, sin, asin, sqrt
import numpy as np
import re
import requests
import urllib
from flask import Flask
from flask import request
import time
from random import randint

class getview(object):
    """Pool Layer of a convolutional network """
    def __init__(self, rawdatafile, SW, NE, where2store,dmin, meshsize):
        self.dfraw = pd.read_csv(rawdatafile)
        self.SW = SW
        self.NE = NE
        self.where2store = where2store
        self.dmin = dmin
        self.meshsize = meshsize
    # def raw2latlng(self):
        df_latlng = self.dfraw['Business_Location'].map(lambda x: str(x).split()[-2:])
        df_lat = df_latlng.map(lambda x: x[0][1:-1])
        df_lng = df_latlng.map(lambda x: x[-1][0:-1])
        df_latlng = pd.concat([df_lat,df_lng],1)
        df_latlng.columns = ['lat', 'lng']
        df = df_latlng.convert_objects(convert_numeric=True)
        
        df=df[(df.lat<NE[0]) & (df.lat>SW[0])]
        df=df[(df.lng<NE[1]) & (df.lng>SW[1])]

        self.df_latlng = df

    def info2name(self, lat, lng, angle, label):
        return 'lat%.6f_lng%.6fang%03d_%dlab%d.png' %(lat,lng,angle,label)

    def name2info(self, filename):
        filename = re.findall(r"[^\W\d_]+|\d+.\d+",filename)
        nameinfo = dict()
        for i in range (len(filename)-1):
            nameinfo[filename[i]] = filename[i+1]
        return nameinfo

    def slicepics(self, pathname,  SW, NE, newpath = None):
        onlyfiles = [ f for f in listdir(pathname) if (isfile(join(pathname,f))) & (len(f)>=31) ]
        validfiles = [f for f in onlyfiles if (float(f[3:12])<NE[0]) & (float(f[3:12])>SW[0])
             & (float(f[16:27])<NE[1]) & (float(f[16:27])>SW[1])]
        if newpath:
            if not os.path.exists(newpath):
                os.mkdir(newpath)
    #         moved = [os.rename(pathname+f, newpath+f) for f in validfiles]
            copied = [shutil.copy(pathname+f, newpath+f) for f in validfiles]

        self.pics4slice = validfiles

    #function that gets list of file names and return dataframe with lat lng as columns
    def filenameplot(filenames,plot = 0):
        latlist = [float(filenames[i][3:12]) for i in range(len(filenames))]
        lnglist = [float(filenames[i][16:27]) for i in range(len(filenames))]
        namelist = [filenames[i] for i in range(len(filenames))]


        df = pd.DataFrame(np.transpose([latlist, lnglist,namelist]), columns=['lat','lng','filename'])
        if plot == 1:
            df.plot('lng','lat',kind='scatter',s = 0.3, figsize= [5,5])
        return df
    def haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km
    def creatdistinct(self):
        df=self.df_latlng[['lat','lng']]
        
        yy = df['lat'].values
        xx = df['lng'].values
        p = df[['lng', 'lat']].values
        p1 = []
        for i in range(len(yy)-1):
            for j in range (i+1,len(yy)):
                d = haversine(xx[i],yy[i],xx[j],yy[j])
                if d < self.dmin:
                    p1.append(p[i])
                    break
        dfp1 = pd.DataFrame(p1)
        dfp1.columns = df.columns
        df_filtered = pd.concat([df, dfp1])
        df_filtered = df_filtered.reset_index(drop=True)
        df_filtered_gpby = df_filtered.groupby(list(df_filtered.columns))
        #get index of unique records
        idx = [x[0] for x in df_filtered_gpby.groups.values() if len(x) == 1]
        #filter
        df_filtered = df_filtered.reindex(idx)
        df_filtered.plot('lng','lat',kind='scatter',figsize=[15,10],s=0.5)

        self.df_filt = df_filtered

        latlinspace = np.linspace(self.SW[0],self.NE[0],self.meshsize[0])
        lnglinspace = np.linspace(self.SW[1],self.NE[1],self.meshsize[1])

        mesh = np.array(np.meshgrid(latlinspace, lnglinspace))

        self.df_filt['label'] = 0
        sortedfiles = []
        for i in range(meshsize[0]):
            for j in range(meshsize[1]):
                inarea = [f for f in onlyfiles if (float(f[3:12])<mesh[:,i+1,j+1[0] & (float(f[3:12])>mesh[:,i,j][0])
             & (float(f[16:27])<mesh[:,i+1,j+1][1]) & (float(f[16:27])>mesh[:,i,j][1])]
                sortedfiles.append(filenameplot(inarea,plot = 0))

        for i in range(len(sortedfiles)-1):
            sortedfiles[i]['label']=i

        dflabeled=sortedfiles[0]

        for i in range(len(sortedfiles)-1):
            dflabeled = pd.concat([dflabeled,sortedfiles[i+1]],axis=0)
        self.df_labeled = dflabeled
        self.df_labeled .to_csv(where2store)


def single_query(self, filename, ii, nsucs, ntries):
    #getfile = urllib.URLopener()
    # print lat,longit
    link='https://maps.googleapis.com/maps/api/streetview?size=300x400&location=%.6f,%.6f&fov=90&heading=%d&pitch=10&key=AIzaSyCsHPCM6nVYgvItOGnmXq17FhvKtjOp44k'%(lat,longit,angle)
    print link
    pathname = self.where2save + infor2name(lat, longit, angle, label)
    urllib.urlretrieve(link, pathname)
    if os.stat(pathname).st_size == 3762 or os.stat(pathname).st_size==7850:
        os.remove(pathname)
        ntries += 1
        return nsucs, ntries
    else:
        try:
            print '%d success!:%d %d Cum Success = %.3f' %(ii, nsucs, ntries, float(nsucs)/ntries)
        except ZeroDivisionError:
            print '%d success! Cum Success = %.3f' %(ii, 0)
        nsucs += 1
        ntries += 1
        return nsucs, ntries

def query(self):
    # df = pd.read_csv('processed.csv')
    # df = df.drop(0,axis=0)
    nsucs = 0
    ntries = 0
    self.df_success = pd.DataFrame()
    angles = [45,135,225,315]#, 45, 120, 135, 210, 225, 300, 315]
    nfiles = os.stat(where2store).st_nlink
    for i in range(df.shape[0]):#nfiles+1,42867)nfiles+10001):#range(df.shape[0]):
        # if isinthebox(df.iloc[i,1],df.iloc[i,2], SW, NE):
        filename = infor2name(self.df_labeled.iloc[i,1],self.df_labeled.iloc[i,2],angles[randint(0,3)], df_labeled['label'][i]
        nsucs_new, ntries = single_query(filename, i , nsucs, ntries)
        if nsucs_new > nsucs:
            nsucs = nsucs_new
            self.df_success.iloc[nsucs] = self.df_labeled[i,:]
            time.sleep(0.0)

                                                                                                                                                                                                                                                                                                                                                                                            run_all.py                                                                                          000644  000765  000024  00000002044 12561731240 013476  0                                                                                                    ustar 00alizaf                          staff                           000000  000000                                                                                                                                                                         import collection
reload(collection)
import shutil,os
from collection import getview

# SW = [37.785087, -122.423623]
# NE = [37.811130, -122.382081]
rawdatafile = 'Registered_Business_Map.csv'
where2store = './photodb21/'

dmin = 0.05
#smal area including few blocks around galvanize
# NE = [37.789679, -122.395617]
# SW = [37.781750, -122.398989]


	# NE = [37.800,-122.400]
	# SW = [37.775,-122.425]
#larger area including part of park
# NE = [37.796259, -122.395532]
# # NE = [37.761259, -122.459532]

# SW = [37.756640, -122.461450]

SW = [37.78, -122.41]
NE = [37.79, -122.40]


g = getview(rawdatafile, SW, NE, where2store)
g.creatdistinct(dmin)


meshsize = [5,5]
picsize = [300,300]

angles = [40, 130, 220, 310]#45, 90, 135, 180]
# angles2 = [130]#225, 180, 315, 360]

# errsize = [(200x200),(300x300)]
errsize = [2966, 3367]
for angle in angles:
	g.query(meshsize,picsize,[angle],errsize,2,full =True)



targetpath = '../codeDL/'+where2store[2:]

if os.path.exists(targetpath):
	shutil.rmtree(targetpath)

shutil.copytree(where2store, targetpath)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            