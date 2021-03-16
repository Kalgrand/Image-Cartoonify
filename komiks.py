# -*- coding: utf-8 -*-
"""
@author: micha
"""

import cv2 # image processing
import easygui # open the filebox
import numpy as np # store image
import imageio # read image stored at particular path

import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


# Tworzenie okna głównego
top=tk.Tk()
top.geometry('400x400')
top.title('Zamień na komiks !')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):
    # wczytuje obraz
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

    # potwierdź wybór obrazu
    if originalmage is None:
        print("Nie znaleziono obrazka. Wybierz odpowiedni plik")
        sys.exit()

    # zmienia rozmiar obrazu po każdej transformacji, aby wyświetlić wszystkie obrazy w podobnej skali
    ReSized1 = cv2.resize(originalmage, (560, 315))


# cvtColor służy do przekształcania obrazu w przestrzeń kolorów określaną jako „flaga”
# flaga BGR2GRAY zwraca obraz w skali szarości.

    # konwertuje obrazu do skali szarości
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (560, 315))

    # zastosowanie medianBlur w celu wygładzenia obrazu
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (560, 315))

# adaptive thresholding technique
# Wartość progowa to średnia z obszaru wartości pikseli sąsiednich minus stała C
# C to stała, która jest odejmowana od średniej lub ważonej sumy sąsiednich pikseli.
# Thresh_binary to typ zastosowanego progu, a pozostałe parametry określają rozmiar bloku.

    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (560, 315))
    
    # Używamy dwustronnego filtra, który usuwa szumy.
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (560, 315))


    # maskowanie obramowanego obrazu
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (560, 315))
    
    # tworzymy listę wszystkich obrazów
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]


# tworzymy osie, na wykresie i wyświetlamy obrazy jeden-jeden w każdym bloku na osi 

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    
    # przycisk Zapisz
    save1=Button(top,text="Save cartoon image",command=lambda: save(ReSized6, ImagePath),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
    
    
def save(ReSized6, ImagePath):
    # zapisywanie obrazu przy użyciu imwrite()
    
    newName="cartoonified_Image"

    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))

    I= "Obraz zapisany " + newName +" w "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
# przycisk komiks 
upload=Button(top,text="Komiks",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)


#Main function to build the tkinter window
top.mainloop()






