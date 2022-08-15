# Digital Inline Holographic Microscopy

## An iGEM 2017 Project

The "Digital Inline Holographic Microscopy.py" script was originally written to solve a problem with entry into the  
iGEM (International Genetically Engineered Machine) competition in 2017.  
  
The original function (taking images and creating a hologram for microscopy) was achieved in LabVIEW.  
(See Credits section below.)  
  
However, the competition asked that any software contributions be made in open source languages.  
Hence the translation into Python.

## What Does It Do?

As inputs, the script takes two pictures.  
The first picture is of some diffraction pattern created by a microscopic object.  
The second is a background picture: the same environment without the microscopic object.  
  
The background is subtracted from the foreground image, isolating the diffraction pattern.  
Using Fourier transforms, the microscope is virtually refocused many times in the z-direction and an image is produced at each stage.  
This forms a hologram of the microscopic object with spatial information in 3 dimensions.  
  
The outputs are then images of each refocused "step", or videos of them stitched together, or both.

## How Do I Run It?

Firstly, make sure you have all the dependencies installed.  
In this case, they are:  
- Numpy
- Scipy
- PIL (or pillow)
- OpenCV2  
  
Now, download "Digital Inline Holographic Microscopy.py", "Background.png" and at least one of "108.png" or "2005.png". 
The numbered images are of diffraction patterns created by bacteria.
  
Run the python script.  
When it asks for a foreground image, give the filepath for either "108.png" or "2005.png".  
For a background image, give the "Background.png" filepath.  
Enter Y for the bandpass filter.  
For any numerical value, use the suggested value. (You could play around with these numbers but it may have unexpected results!)  
Designate a directory for the script to save your hologram into.  
Wait for the code to finish running and you're good to go!  
  
Congratulations on your new hologram!  

## Credits
Author: Joseph McKeown  
  
Special thanks to Dr. Laurence Wilson, who wrote the original LabVIEW code (available at https://sites.google.com/a/york.ac.uk/bis_lab/downloads).

## Licence

Copyright (C) 2022 Joseph McKeown

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,      
but WITHOUT ANY WARRANTY; without even the implied warranty of       
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        
GNU General Public License for more details.                         
                                                                     
You should have received a copy of the GNU General Public License    
along with this program.  If not, see <http://www.gnu.org/licenses/>.
