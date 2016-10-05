#coding: utf-8

import numpy as np
import cv2
import sys
import sqlite3
from scipy.spatial.distance import cdist,euclidean
import io
from cbir import *
import operator

if __name__ == "__main__":
    #carregando as imagens
    img = cv2.imread(sys.argv[1])
    cinza = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kn = int(sys.argv[2])
    metodo = sys.argv[3]


    if metodo == 'fourier':
        sqlite3.register_adapter(np.ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)

        con = sqlite3.connect('cbir.db',detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute("SELECT fourier_arr FROM IMAGE_INDEX")
        index = cur.fetchall()
        
        #fourier descriptor
        fd = find_descriptor(cinza)
        #computando as distancias entre a imagem de entrada e o index
        dists = []
        
        for i in index:
            faux = fd.flatten()
            iaux = i[0].flatten()[:len(faux)]
            for j in xrange(len(faux)):
                if faux[j] == np.inf or faux[j] == np.NaN:
                    faux[j] = 1
                if iaux[j] == np.inf or iaux[j] == np.NaN:
                    iaux[j] = 1     
            dists.append(euclidean(faux,iaux))
        
        for i in xrange(len(dists)):
            dists[i] = np.linalg.norm(dists[i])

        dic = {i: dists[i] for i in xrange(len(dists))}
        knarray = []

        sort_dic = sorted(dic.items(), key=operator.itemgetter(1))

        for i in xrange(kn):
            print sort_dic[i][0]
       
    if metodo == 'sift':
        
        sqlite3.register_adapter(np.ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)

        con = sqlite3.connect('cbir.db',detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute("SELECT sift_arr FROM IMAGE_INDEX")
        index = cur.fetchall()

        #SIFT
        sift = cv2.xfeatures2d.SIFT_create()
        (kps, desc) = sift.detectAndCompute(cinza, None)

        #computando as distancias entre a imagem de entrada e o index
        dists = []
        
        for i in index:
            dists.append(chi2_distance(desc,i))
            
        dic = {i: dists[i] for i in xrange(len(dists))}
        knarray = []

        sort_dic = sorted(dic.items(), key=operator.itemgetter(1))

        for i in xrange(kn):
            print sort_dic[i][0]
       
