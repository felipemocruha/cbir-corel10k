#coding: utf-8

import numpy as np
import cv2
import sys
import sqlite3
from scipy.spatial.distance import cdist
from scipy.misc import imread
import io
import os


def find_descriptor(img):
    '''
    fourier

    '''
    ret, thres = cv2.threshold(img,127,255,0)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    ms = 20*np.log(np.abs(fshift))
    return ms
            
#from: http://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

#from: http://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database
def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)
            
def chi2_distance(histA, histB, eps = 1e-10):
    # compute the chi-squared distance
    d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                      for (a, b) in zip(histA, histB)])
    
    # return the chi-squared distance
    return d
            
if __name__ == '__main__':
    
    #construindo o banco
    con = sqlite3.connect('cbir.db',detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()

    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, adapt_array)

    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("array", convert_array)

    #cria a tabela com as imagens e seus descritores
    cur.execute("DROP TABLE IF EXISTS IMAGE_INDEX")
    cur.execute("CREATE TABLE IMAGE_INDEX(NOME VARCHAR(10), sift_arr array, fourier_arr array)")

    #lista com os nomes dos arquivos
    #imgs_path = ['images/'+str(i)+'.jpg' for i in xrange(1,100)]

    #deve existir um dir images com todas as imagens dentro dele
    imgs_path = os.listdir('images/')
    
    images = []
    #lista de todas as imagens em grayscale
    print 'Carregando imagens...'
    
    for i in imgs_path[:]:
        im = cv2.imread('images/'+i)
        if im != None:
            images.append(im)

    
    for i in xrange(len(images)):
        try:
            cv2.cvtColor(images[i],cv2.COLOR_BGR2GRAY)
        except:
            pass
    
    #SIFT
    sift = cv2.xfeatures2d.SIFT_create()
    
    #listas com os descritores sift de todas as imagens
    desc_sift = []
    desc_fourier = []

    #fourier
    print 'Criando os descritores Fourier...'
    for i in images:
        fd = find_descriptor(i)
        desc_fourier.append(fd)    
        
    #sift
    print 'Criando os descritores SIFT...'
    for i in images:
        (kps, desc) = sift.detectAndCompute(i, None)
        desc_sift.append(desc)

    print 'Criando o index no banco de dados...'
    #criando o index das imagens e descritores
    for i in xrange(len(images)):
        cur.execute("INSERT INTO IMAGE_INDEX VALUES(?,?,?)", (imgs_path[i], desc_sift[i], desc_fourier[i]))

    
    con.commit()
    con.close()
    
    print 'Index de descritores criado com sucesso!'





    
