'''
utils.py

Utility functions used by simpledots.py

by Lincoln Ombelets, 2019-2020
Distributed under the MIT license

'''
import numpy as np
import pandas as pd
import os
import os.path as osp
import skimage
import scipy
import re
import skimage.io

# needed for imshow()
import bokeh.models
import bokeh.palettes
import bokeh.plotting


def fetch_image(data_dir, cycle, position, hyb_pattern='HybCycle_(\d+)$', im_prefix=''):
    '''
    fetch_image(data_dir, cycle, position, prefix, postfix, reshape):
    Fetches an image file from a specified hyb cycle and position, as produced by an automation experiment in MicroManager.
    Assumes images are located in files named 'HybCycle_#postfix' where # is the cycle and postfix is an optional string.
    Within these folders are one or more TIF stacks corresponding to each position, which are generally named as prefix_Pos#.ome.tif,
    where # is the position index. Raw MicroManager output uses 'MMStack' as the prefix, but after swapping channels and slices I change the name,
    so `prefix` allows specifying which specific set of images in the hyb cycle folder to fetch.
    
    If `reshape` is true, which it is by default, then the image will be returned in channel-first indexing shape.
    
    Returns:
    raw: Scikit image MultiImage (equivalent to a Numpy ndarray) containing the raw image data.
    '''
    
    im_pattern = '^' + im_prefix + 'MMStack_Pos(\d+)(.*)'
    
    image = None
    found_dir = False
    
    for f in os.scandir(data_dir):
        cycle_search = re.search(hyb_pattern, f.name)
        
        if not cycle_search:
            continue
            
        if int(cycle_search[1]) == cycle:
            
            if not osp.isdir(f.path):
                print('error: that isnt a directory!')

                return None
            
            found_dir = True
            break # break out of the folder/cycle loop
        
        else:
            
            continue # jump to the next folder if this one doesn't match
    
    if not found_dir:
        return None
    
    for g in os.scandir(f.path):
        pos_search = re.search(im_pattern, g.name)
            
        if not pos_search:
            continue
                
        if int(pos_search[1]) == position:

            image = g.path

            break # we have found the image, exit position loop
        
    if not image:
        print('Could not find image for cycle {}, position {}'.format(cycle, position))
        return None
    
    raw = skimage.io.imread(image)
        
    return raw


def subtract_background_fft(input_im, radius=50):
    image_fft = np.fft.rfft2(input_im)
    bg_fft = scipy.ndimage.fourier.fourier_gaussian(image_fft, radius, n=input_im.shape[0])
    return np.maximum(0, np.fft.irfft2(image_fft - bg_fft)), np.maximum(0, np.fft.irfft2(bg_fft))

    
def local_max_image_2(image,
                    bg_std,
                    thresh_coeff=3,
                    thresh_abs=0,
                    min_distance=1, 
                    exclude_border=2,
                    intensity_image=None,
                    mask=None,
                    verbose=False):
    '''
    local_max_image_2: Performs the same thing as local_max_image, but uses scikit-image 0.16.0's `label` and `regionprops_table` to more elegantly create a DataFrame
    while keeping the intensity image associated. Does NOT perform max filtering; returns
    single-pixel maxima image, from which 'expanded' images can be generated.
    
    Returns:
    local_maxes: binary image of same shape as `image` where 1/True indicates local maximum and 0/False everything else
    props_df: DataFrame containing numerical label, area, coordinates and intensity for each dot. Note coordinates are arrays in a single column and intensity is a 2D array with a single value for the one-pixel local maxima.
    '''
    # we use the absolute threshold if it is specified.
    if thresh_abs > 0:
        thresh = thresh_abs
    else:
        thresh = thresh_coeff * bg_std
        
    if verbose:
        print('local_max_image: finding local maxes above threshold of {}'.format(int(thresh)))
    
    # Take a function that receives the 2D image as its argument and returns a binary mask
    if mask:
        masked = mask(image)
    else:
        masked = None
    
    local_maxes = skimage.feature.peak_local_max(image, 
                                                 min_distance=min_distance, 
                                                 threshold_abs=thresh, 
                                                 exclude_border=exclude_border,
                                                 footprint=masked,
                                                 indices=False)
    
    labeled  = skimage.measure.label(local_maxes)
    
    if type(intensity_image) == type(None):
        intensity_image = image
    
    try:
        props_df = pd.DataFrame(skimage.measure.regionprops_table(labeled, intensity_image, 
                                                 properties=('coords', 'max_intensity')))
    except:
        props_df = pd.DataFrame(columns=['coords', 'max_intensity']) # empty DF if no regions are found
    
    if verbose:
        print('local_max_image: found {} local max pixels'.format(len(props_df)))
    
    return local_maxes.astype(bool), props_df


'''
The following two functions, `imshow` and `im_merge`, are slightly modified versions of those from Justin Bois' BE/Bi103 utility package, hosted at https://github.com/justinbois/bebi103/. The follow license/disclaimer applies to them.


Copyright (c) 2017, Justin Bois All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

def imshow(
    im,
    cmap=None,
    frame_height=400,
    frame_width=None,
    length_units="pixels",
    interpixel_distance=1.0,
    x_range=None,
    y_range=None,
    colorbar=False,
    no_ticks=False,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    flip=True,
    return_im=False,
    saturate_channels=True,
    min_intensity=None,
    max_intensity=None,
    display_clicks=False,
    record_clicks=False,
):
    """
    Display an image in a Bokeh figure.
    Parameters
    ----------
    im : Numpy array
        If 2D, intensity image to be displayed. If 3D, first two
        dimensions are pixel values. Last dimension can be of length
        1, 2, or 3, which specify colors.
    cmap : str or list of hex colors, default None
        If `im` is an intensity image, `cmap` is a mapping of
        intensity to color. If None, default is 256-level Viridis.
        If `im` is a color image, then `cmap` can either be
        'rgb' or 'cmy' (default), for RGB or CMY merge of channels.
    frame_height : int
        Height of the plot in pixels. The width is scaled so that the
        x and y distance between pixels is the same.
    frame_width : int or None (default)
        If None, the width is scaled so that the x and y distance
        between pixels is approximately the same. Otherwise, the width
        of the plot in pixels.
    length_units : str, default 'pixels'
        The units of length in the image.
    interpixel_distance : float, default 1.0
        Interpixel distance in units of `length_units`.
    x_range : bokeh.models.Range1d instance, default None
        Range of x-axis. If None, determined automatically.
    y_range : bokeh.models.Range1d instance, default None
        Range of y-axis. If None, determined automatically.
    colorbar : bool, default False
        If True, include a colorbar.
    no_ticks : bool, default False
        If True, no ticks are displayed. See note below.
    x_axis_label : str, default None
        Label for the x-axis. If None, labeled with `length_units`.
    y_axis_label : str, default None
        Label for the y-axis. If None, labeled with `length_units`.
    title : str, default None
        The title of the plot.
    flip : bool, default True
        If True, flip image so it displays right-side up. This is
        necessary because traditionally images have their 0,0 pixel
        index in the top left corner, and not the bottom left corner.
    return_im : bool, default False
        If True, return the GlyphRenderer instance of the image being
        displayed.
    saturate_channels : bool, default True
        If True, each of the channels have their displayed pixel values
        extended to range from 0 to 255 to show the full dynamic range.
    min_intensity : int or float, default None
        Minimum possible intensity of a pixel in the image. If None,
        the image is scaled based on the dynamic range in the image.
    max_intensity : int or float, default None
        Maximum possible intensity of a pixel in the image. If None,
        the image is scaled based on the dynamic range in the image.
    display_clicks : bool, default False
        If True, display clicks to the right of the plot using
        JavaScript. The clicks are not recorded nor stored, just
        printed. If you want to store the clicks, use the
        `record_clicks()` or `draw_rois()` functions.
    record_clicks : bool, default False
        Deprecated. Use `display_clicks`.
    Returns
    -------
    p : bokeh.plotting.figure instance
        Bokeh plot with image displayed.
    im : bokeh.models.renderers.GlyphRenderer instance (optional)
        The GlyphRenderer instance of the image being displayed. This is
        only returned if `return_im` is True.
    """

    # If a single channel in 3D image, flatten and check shape
    if im.ndim == 3:
        if im.shape[2] == 1:
            im = im[:, :, 0]
        elif im.shape[2] not in [2, 3]:
            raise RuntimeError("Can only display 1, 2, or 3 channels.")

    # If binary image, make sure it's int
    if im.dtype == bool:
        im = im.astype(np.uint8)

    # Get color mapper
    if im.ndim == 2:
        if cmap is None:
            color_mapper = bokeh.models.LinearColorMapper(bokeh.palettes.viridis(256))
        elif type(cmap) == str and cmap.lower() in ["rgb", "cmy"]:
            raise RuntimeError("Cannot use rgb or cmy colormap for intensity image.")
        else:
            color_mapper = bokeh.models.LinearColorMapper(cmap)

        if min_intensity is None:
            color_mapper.low = im.min()
        else:
            color_mapper.low = min_intensity
        if max_intensity is None:
            color_mapper.high = im.max()
        else:
            color_mapper.high = max_intensity
    elif im.ndim == 3:
        if cmap is None or cmap.lower() == "cmy":
            im = im_merge(
                *np.rollaxis(im, 2),
                cmy=True,
                im_0_min=min_intensity,
                im_1_min=min_intensity,
                im_2_min=min_intensity,
                im_0_max=max_intensity,
                im_1_max=max_intensity,
                im_2_max=max_intensity,
            )
        elif cmap.lower() == "rgb":
            im = im_merge(
                *np.rollaxis(im, 2),
                cmy=False,
                im_0_min=min_intensity,
                im_1_min=min_intensity,
                im_2_min=min_intensity,
                im_0_max=max_intensity,
                im_1_max=max_intensity,
                im_2_max=max_intensity,
            )
        else:
            raise RuntimeError("Invalid color mapper for color image.")
    else:
        raise RuntimeError("Input image array must have either 2 or 3 dimensions.")

    # Get shape, dimensions
    n, m = im.shape[:2]
    if x_range is not None and y_range is not None:
        dw = x_range[1] - x_range[0]
        dh = y_range[1] - y_range[0]
    else:
        dw = m * interpixel_distance
        dh = n * interpixel_distance
        x_range = [0, dw]
        y_range = [0, dh]

    # Set up figure with appropriate dimensions
    if frame_width is None:
        frame_width = int(m / n * frame_height)
    if colorbar:
        toolbar_location = "above"
    else:
        toolbar_location = "right"
    p = bokeh.plotting.figure(
        frame_height=frame_height,
        frame_width=frame_width,
        x_range=x_range,
        y_range=y_range,
        title=title,
        toolbar_location=toolbar_location,
        tools="pan,box_zoom,wheel_zoom,save,reset",
    )
    if no_ticks:
        p.xaxis.major_label_text_font_size = "0pt"
        p.yaxis.major_label_text_font_size = "0pt"
        p.xaxis.major_tick_line_color = None
        p.xaxis.minor_tick_line_color = None
        p.yaxis.major_tick_line_color = None
        p.yaxis.minor_tick_line_color = None
    else:
        if x_axis_label is None:
            p.xaxis.axis_label = length_units
        else:
            p.xaxis.axis_label = x_axis_label
        if y_axis_label is None:
            p.yaxis.axis_label = length_units
        else:
            p.yaxis.axis_label = y_axis_label

    # Display the image
    if im.ndim == 2:
        if flip:
            im = im[::-1, :]
        im_bokeh = p.image(
            image=[im],
            x=x_range[0],
            y=y_range[0],
            dw=dw,
            dh=dh,
            color_mapper=color_mapper,
        )
    else:
        im_bokeh = p.image_rgba(
            image=[rgb_to_rgba32(im, flip=flip)],
            x=x_range[0],
            y=y_range[0],
            dw=dw,
            dh=dh,
        )

    # Make a colorbar
    if colorbar:
        if im.ndim == 3:
            warnings.warn("No colorbar display for RGB images.")
        else:
            color_bar = bokeh.models.ColorBar(
                color_mapper=color_mapper,
                label_standoff=12,
                border_line_color=None,
                location=(0, 0),
            )
            p.add_layout(color_bar, "right")

    if return_im:
        return p, im_bokeh
    return p

def im_merge(
    im_0,
    im_1,
    im_2=None,
    im_0_max=None,
    im_1_max=None,
    im_2_max=None,
    im_0_min=None,
    im_1_min=None,
    im_2_min=None,
    cmy=True,
):
    """
    Merge channels to make RGB image.
    Parameters
    ----------
    im_0: array_like
        Image represented in first channel.  Must be same shape
        as `im_1` and `im_2` (if not None).
    im_1: array_like
        Image represented in second channel.  Must be same shape
        as `im_1` and `im_2` (if not None).
    im_2: array_like, default None
        Image represented in third channel.  If not None, must be same
        shape as `im_0` and `im_1`.
    im_0_max : float, default max of inputed first channel
        Maximum value to use when scaling the first channel. If None,
        scaled to span entire range.
    im_1_max : float, default max of inputed second channel
        Maximum value to use when scaling the second channel
    im_2_max : float, default max of inputed third channel
        Maximum value to use when scaling the third channel
    im_0_min : float, default min of inputed first channel
        Maximum value to use when scaling the first channel
    im_1_min : float, default min of inputed second channel
        Minimum value to use when scaling the second channel
    im_2_min : float, default min of inputed third channel
        Minimum value to use when scaling the third channel
    cmy : bool, default True
        If True, first channel is cyan, second is magenta, and third is
        yellow. Otherwise, first channel is red, second is green, and
        third is blue.
    Returns
    -------
    output : array_like, dtype float, shape (*im_0.shape, 3)
        RGB image.
    """

    # Compute max intensities if needed
    if im_0_max is None:
        im_0_max = im_0.max()
    if im_1_max is None:
        im_1_max = im_1.max()
    if im_2 is not None and im_2_max is None:
        im_2_max = im_2.max()

    # Compute min intensities if needed
    if im_0_min is None:
        im_0_min = im_0.min()
    if im_1_min is None:
        im_1_min = im_1.min()
    if im_2 is not None and im_2_min is None:
        im_2_min = im_2.min()

    # Make sure maxes are ok
    if (
        im_0_max < im_0.max()
        or im_1_max < im_1.max()
        or (im_2 is not None and im_2_max < im_2.max())
    ):
        raise RuntimeError("Inputted max of channel < max of inputted channel.")

    # Make sure mins are ok
    if (
        im_0_min > im_0.min()
        or im_1_min > im_1.min()
        or (im_2 is not None and im_2_min > im_2.min())
    ):
        raise RuntimeError("Inputted min of channel > min of inputted channel.")

    # Scale the images
    if im_0_max > im_0_min:
        im_0 = (im_0 - im_0_min) / (im_0_max - im_0_min)
    else:
        im_0 = (im_0 > 0).astype(float)

    if im_1_max > im_1_min:
        im_1 = (im_1 - im_1_min) / (im_1_max - im_1_min)
    else:
        im_0 = (im_0 > 0).astype(float)

    if im_2 is None:
        im_2 = np.zeros_like(im_0)
    elif im_2_max > im_2_min:
        im_2 = (im_2 - im_2_min) / (im_2_max - im_2_min)
    else:
        im_0 = (im_0 > 0).astype(float)

    # Convert images to RGB
    if cmy:
        im_c = np.stack((np.zeros_like(im_0), im_0, im_0), axis=2)
        im_m = np.stack((im_1, np.zeros_like(im_1), im_1), axis=2)
        im_y = np.stack((im_2, im_2, np.zeros_like(im_2)), axis=2)
        im_rgb = im_c + im_m + im_y
        for i in [0, 1, 2]:
            im_rgb[:, :, i] /= im_rgb[:, :, i].max()
    else:
        im_rgb = np.empty((*im_0.shape, 3))
        im_rgb[:, :, 0] = im_0
        im_rgb[:, :, 1] = im_1
        im_rgb[:, :, 2] = im_2

    return im_rgb
