"""
======================================================
Measure fluorescence intensity at the nuclear envelope
======================================================

This example reproduces a well-established workflow in bioimage data analysis
for measuring the fluorescence intensity localized to the nuclear envelope, in
a time sequence of cell images (each with two channels and two spatial
dimensions) which shows a process of protein re-localization from the
cytoplasmic area to the nuclear envelope. This biological application was
first presented by Andrea Boni and collaborators in [1]_; it was used in a
textbook by Kota Miura [2]_ as well as in other works ([3]_, [4]_).
In other words, we port this workflow from ImageJ Macro to Python with
scikit-image.

.. [1] Boni A, Politi AZ, Strnad P, Xiang W, Hossain MJ, Ellenberg J (2015)
       "Live imaging and modeling of inner nuclear membrane targeting reveals
       its molecular requirements in mammalian cells" J Cell Biol
       209(5):705–720. ISSN: 0021-9525.
       :DOI:`10.1083/jcb.201409133`
.. [2] Miura K (2020) "Measurements of Intensity Dynamics at the Periphery of
       the Nucleus" in: Miura K, Sladoje N (eds) Bioimage Data Analysis
       Workflows. Learning Materials in Biosciences. Springer, Cham.
       :DOI:`10.1007/978-3-030-22386-1_2`
.. [3] Klemm A (2020) "ImageJ/Fiji Macro Language" NEUBIAS Academy Online
       Course: https://www.youtube.com/watch?v=o8tfkdcd3DA
.. [4] Vorkel D and Haase R (2020) "GPU-accelerating ImageJ Macro image
       processing workflows using CLIJ" https://arxiv.org/abs/2008.11799

"""

import matplotlib.pyplot as plt
import numpy as np
import plotly.io
import plotly.express as px
from scipy import ndimage as ndi

from skimage import filters, measure, morphology, segmentation
from skimage.data import protein_transport




def NE_mask(img,sigma=1.5,nb_px=1):

    smooth = filters.gaussian(img, sigma)

    thresh_value = filters.threshold_otsu(smooth)
    thresh = smooth > thresh_value + np.std(smooth)
    
    
    


    fill = ndi.binary_fill_holes(thresh)
    
   
    #####################################################################
    # Following the original workflow, let us remove objects which touch the image
    # border (step ``c-2)``). Here, we can see that part of another nucleus was
    # touching the bottom right-hand corner.

    clear = segmentation.clear_border(fill)
    clear.dtype
    
    
#####################################################################
    # We compute both the morphological dilation of this binary image
    # (step ``d)``) and its morphological erosion (step ``e)``).

    dilate = morphology.binary_dilation(clear)

    n=0
    while n < nb_px:
        n=n+1
        erode = morphology.binary_erosion(clear)
        clear = erode
        

    #####################################################################
    # Finally, we subtract the eroded from the dilated to get the nucleus rim
    # (step ``f)``). This is equivalent to selecting the pixels which are in
    # ``dilate``, but not in ``erode``:

    mask = np.logical_and(dilate, ~erode)


    return mask

