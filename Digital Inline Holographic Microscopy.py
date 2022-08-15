################################################################################
####                    Copyright (C) 2022 Joseph McKeown                  #####
####                                                                       #####
#### This program is free software: you can redistribute it and/or modify  #####
#### it under the terms of the GNU General Public License as published by  #####
#### the Free Software Foundation, either version 3 of the License, or     #####
#### (at your option) any later version.                                   #####
####                                                                       #####
#### This program is distributed in the hope that it will be useful,       #####
#### but WITHOUT ANY WARRANTY; without even the implied warranty of        #####
#### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #####
#### GNU General Public License for more details.                          #####
####                                                                       #####
#### You should have received a copy of the GNU General Public License     #####
#### along with this program.  If not, see <http://www.gnu.org/licenses/>. #####
################################################################################

print("                   Copyright (C) 2022 Joseph McKeown               ")
print("")
print("This program is free software: you can redistribute it and/or modify")
print("it under the terms of the GNU General Public License as published by")
print("the Free Software Foundation, either version 3 of the License, or")
print("(at your option) any later version.")
print("")
print("This program is distributed in the hope that it will be useful,")
print("but WITHOUT ANY WARRANTY; without even the implied warranty of")
print("MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
print("GNU General Public License for more details.")
print("")
print("You should have received a copy of the GNU General Public License")
print("along with this program.  If not, see <http://www.gnu.org/licenses/>.")
print("")
print("---------------------------------------------------------------------")
print("")

################################################################################
#### This program requires the following libraries: PIL                    #####
####                                                Numpy                  #####
####                                                Scipy                  #####
####                                                Open CV 2              #####
####                                                                       #####
################################################################################

print("Please ensure that you have PIL, Numpy, Scipy and Open CV2 installed.")
print("")
print("This program was designed to run in Python version 2.7.9 and")
print("has been adapted for use in Python version 3.10.4 but has ")
print("not been confirmed to operate correctly in any other versions.")
print("")
print("---------------------------------------------------------------------")
print("")
print("                   Please input your values below.                 ")
print("")

################################################################################
################################################################################
#### This program is capable of producing holograms from a pair of images. #####
####         A foreground image and background image are required.         #####
####       Holograms can be created as videos or as a series of images.    #####
####       Please run the program and follow the printed instructions.     #####
################################################################################
################################################################################

from PIL import Image
import numpy as np
import scipy.signal as ss
import os
import cv2

################################################################################
############################## REFOCUS STACK ###################################
################################################################################

#Get original image names and open files.
#The variables 'name' and 'bgname' are filepaths as strings.
ValidInput = False
while ValidInput == False:
    try:
        name = input("Foreground image filepath? ")
        #Import foreground.
        fg = Image.open('%s'%name)
        
        bgname = input("Background image filepath? ")
        #Import background.
        bg = Image.open('%s'%bgname)
        ValidInput = True
    
    except IOError:
        print("Something went wrong with your filepath(s).")
        print("Remember to include the file extension (e.g. image.png).")

#Options for output.
ValidInput = False
while ValidInput == False:
    Decision = input("Press 'V' for hologram video, 'I' for hologram images or 'B' for both. ")
    if Decision.lower() == 'v':
        ValidInput = True
    elif Decision.lower() == 'i':
        ValidInput = True
    elif Decision.lower() == 'b':
        ValidInput = True
    else:
        print("Please answer 'V' for videos, 'I' for images or 'B' for both.")

#Convert to monochrome.
fg = fg.convert('L')
bg = bg.convert('L')

#Turn into arrays.
fg = np.array(fg)
bg = np.array(bg)

#Correct background (all zeros to ones).
for row in bg:
    for pixel in row:
        if pixel == 0:
            pixel = 1
            
#Convert arrays from int to float for division etc.
fg = fg.astype(np.float32)
bg = bg.astype(np.float32)

#Calculate filter array, if the user wants to use a bandpass filter.
ValidInput = False
while ValidInput == False:
        Bpass = input("Band pass filter (Y/N)? ")
        if Bpass.lower() == 'y':
            ValidInput = True
        elif Bpass.lower() == 'n':
            ValidInput = True
        else:
            print("Please answer Y or N.")

if Bpass.lower() == ('y' or 'yes'):
    ValidInput = False
    while ValidInput == False:
        try:
            smax = int(input("Max pixels? (Suggested 40) "))
            smin = int(input("Min pixels? (Suggested 2) "))
            if smin >= 0 and smax > 0:
                ValidInput = True
            else:
                print("Please ensure you use positive integers only.")
        except ValueError:
            print("Please use whole numbers only.")
            
    lmax = max([len(bg),len(bg[0])])
    q1 = lmax/2.0
    q2 = -(((smax*2.0)/lmax)**2)
    q3 = -(((smin*2.0)/lmax)**2)
    filtar1 = np.zeros((len(bg),len(bg[0])))
    filtar2 = np.zeros((len(bg),len(bg[0])))
    for i in range(len(bg)):
        o = (i-q1)**2
        for j in range(len(bg[0])):
            o2 = o+(j-q1)**2
            filtar1[i][j] = np.exp(o2*q2)
            filtar2[i][j] = np.exp(o2*q3)
    filtar=np.subtract(filtar2,filtar1)
    #Filtar will later be multiplied into the stack to create bandpass effect.

#Fourier transform of (FG/BG)-1.
divar = np.divide(fg,bg)
out1 = np.subtract(divar,1)
ft = np.fft.fft2(out1)
ft = np.fft.fftshift(ft)

#Set useful variables from user input.
ValidInput = False
while ValidInput == False:
    try:
        nosteps = int(input("Number of steps? (Suggested 150) "))
        wvl = float(input("Wavelength? (Suggested 0.66) "))
        mri = float(input("Median Refractive Index? (Suggested 1.3326) "))
        ppm = float(input("Pixels per Micron? (Suggested 4.29) "))
        ssz = float(input("Step Size? (Suggested 0.233) "))
        defdist = float(input("Offset distance? (Suggested 0) "))-ssz
        fps = float(input("Frames per Second for output video? (Suggested 24.0) "))
        ValidInput = True
    except ValueError:
        print("There was an error in your inputs. Please use numbers only.")

#If all variables were entered successfully...
#A folder should be created in order to store the outputs.
ValidInput = False
while ValidInput == False:
    Directory = input("In which directory should the hologram be saved? ")
    if os.path.isdir(Directory) and Directory.endswith("\\"):
        ValidInput = True
    else:
        print("There was an error with your input. Please enter in the form: C:\\users\\JohnSmith\\Desktop\\ ")

name=name.split('\\')
name=name[len(name)-1].split('.')
if os.path.isdir("%s%s"%(Directory, name[0]))==False:
    os.mkdir("%s%s"%(Directory, name[0]))

#Parabola loop.
N=len(fg)
in1=ppm*wvl/mri 
outar=np.zeros((len(fg),len(fg[0])))
for i in range(N):
    outi=((i-(N/2.0))*(in1/N))**2
    for j in range(N):
        outj=((j-(N/2.0))*(in1/N))**2
        outar[i][j]=outi+outj

#Q factor.
outar=np.subtract(1,outar)
outar=np.real(outar)
Qfac=np.lib.scimath.sqrt(outar)
array1=np.subtract(Qfac,1)

print("Writing refocus stack...")

#Create a stack array to store holograph frames (2D arrays).
stackar = []

#Take complex conjugate for all images except input.
for j in range(nosteps):
    defdist += ssz
    if defdist*ppm > 0:
        outar = np.conj(array1)
    else:
        outar = array1

#More operations.
    rpp = ((mri/wvl)*-2*np.pi*(0+1j)*(1/ppm))#radians per pixel
    outar = np.multiply(outar,rpp*defdist*ppm)
    outar = np.exp(outar)

#Apply bandpass filter if appropriate.    
    if Bpass.lower() == ('y' or 'yes'):
        outar = np.multiply(filtar,np.multiply(ft,outar))
    else:
        outar = np.multiply(ft,outar)

#Inverse Fourier.
    outar = np.fft.ifftshift(outar)
    outar = np.fft.ifft2(outar)
    outar = np.add(outar,1)
    outar = np.real(outar)

#Make intensity range from 0-255.
    maxo = outar.max()
    mino = outar.min()
    outar = np.subtract(outar,mino)
    outar = np.multiply(outar,(255/(maxo-mino)))

#Produce stack.
    outar = outar.astype(np.uint8) #converting to uint8 for VideoWriter
    stackar.append(outar)

#Use stack to write hologram video.
if Decision.lower() == 'v' or Decision.lower() == 'b':
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    size = len(stackar[0][0]), len(stackar[0])
    vid = cv2.VideoWriter('%s%s'%(Directory,name[0])+'\HOLO.%s'%name[0]+'vid.mp4',fourcc,fps,size, False)
    for img in stackar:
        vid.write(img)
    vid.release()

#Save each image in the stack.
if Decision.lower() == 'i' or Decision.lower() == 'b':
    i=0
    for img in stackar:
        img = Image.fromarray(img).convert('L').save('%s%s'%(Directory,name[0])+'\%s'%name[0]+'.%d.png'%i)
        i+=1
        
################################################################################
############################### GRADIENT STACK #################################
################################################################################

print("Writing gradient stack...")

#Start a list of image filepaths for video construction later.
gradimglist=[]

#Create modified Sobel filter.
Sobel = np.array([[0,0,0],[-1,0,1],[0,0,0]])
Sobel = np.transpose(Sobel)

#Pad the image stack to avoid edge effects.
tempar = np.zeros((len(stackar)+4,len(stackar[0]),len(stackar[0][0])))
for i in range(2):
    tempar[i]=stackar[0]
for i in range(len(stackar)):
    tempar[i+2]=stackar[i]
tempar[len(stackar)+2]=stackar[len(stackar)-1]
tempar[len(stackar)+3]=stackar[len(stackar)-1]
stackar=tempar

#Convolve the stack with the modified Sobel filter.
stackar = np.transpose(stackar)
newar = np.zeros((len(stackar),len(stackar[0][0]),len(stackar[0])))
for i in range(len(stackar)):
    newar[i] = np.transpose(stackar[i])
convar = np.zeros((len(newar),len(newar[0])+2,len(newar[0][0])+2))
for i in range(len(convar)):
    convar[i]=ss.convolve2d(newar[i],Sobel,mode='full')

#Resize array.
tempar = np.zeros((len(convar[0][0])-2,len(convar[0]),len(convar)))
convar = np.transpose(convar)
for i in range(len(convar)-2):
    tempar[i] = convar[i+1]
convar = tempar
tempar = np.zeros((len(convar),len(convar[0][0]),len(convar[0])))
for i in range(len(tempar)):
    tempar[i] = np.transpose(convar[i])
convar = np.transpose(tempar)
tempar = np.zeros((len(convar)-6,len(convar[0]),len(convar[0][0])))
for i in range(len(convar)-6):
    tempar[i] = convar[i+3]
convar = tempar
tempar = np.zeros((len(convar),len(convar[0][0]),len(convar[0])))
for i in range(len(tempar)):
    tempar[i] = np.transpose(convar[i])

#Make intensity range from 0-255.
stackar = np.clip(tempar, 0, None)
stackar = np.multiply(stackar, 255/(stackar.max()))
stackar = stackar.astype(np.uint8)

#Use stack to write gradient video.
if Decision.lower() == 'v' or Decision.lower() == 'b':
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    size = len(stackar[0][0]), len(stackar[0])
    vid = cv2.VideoWriter('%s%s'%(Directory,name[0])+'\HOLOGRAD.%s'%name[0]+'vid.mp4',fourcc,fps,size, False)
    for img in stackar:
        vid.write(img)
    vid.release()

#Save each image in the stack.
if Decision.lower() == 'i' or Decision.lower() == 'b':
    i=0
    for img in stackar:
        img = Image.fromarray(img).convert('L').save('%s%s'%(Directory,name[0])+'\GRAD.%s'%name[0]+'.%d.png'%i)
        i+=1

#Tell the user the program has finished running.
print(f"The program has finished running. Please go to {Directory+name[0]} to find your files.")
