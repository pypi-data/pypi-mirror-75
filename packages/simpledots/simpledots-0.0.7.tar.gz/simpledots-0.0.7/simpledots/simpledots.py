'''
simpledots.py

by Lincoln Ombelets, 2019-2020

Distributed under the MIT license
'''
import numpy as np
import pandas as pd
import re
import xarray as xr
import scipy as sp
import scipy.stats

import bokeh
import skimage
import skimage.feature
import skimage.io
import skimage.filters
import skimage.morphology
__skimage_version__ = skimage.__version__.split('.')


import scipy.ndimage
import os
import os.path as osp
import copy
import itertools

from concurrent.futures import ThreadPoolExecutor
from .utils import *


class WBImage:
    '''
    WBImage: a variable dimensional image that you can iterate through and index intuitively.
    
    * Last two dimensions should be two largest (very good assumption, very rare to be working with an image that's smaller in xy than in z or channels)
    * If image is 3D, first/short dimension is more likely channels than slices (okay assumption for me at least, generally do single slice several channels rather than single channel several slices)
    * If image is 4D, first two/short dimensions are most likely channels and slices - good assumption since multiframes is pretty rare, though single slice or channel with multiframes could be used
    * Channels could be minimum dimension (only okay assumption, can have short Z stack or frames)
    ** Better assumption is that channels is less than or equal to 6
    * Default order from automation is (frames, slices, channels, x, y) or (frames, channels, x, y, slices)
    * Default order from micromanager manual is (frames, channels, slices, x, y) or (frames, channels, x, y, slices)
    ** Frames is always first when it is present;  if image is 5D, good assumption that first dim is frames
    * Final image will always be 5D, i.e. use np.expand() to add singleton dimensions where needed. This keeps iteration and indexing consistent, which is important
    
    '''

    # default order: channel, slice, frame, x, y
    
    def __init__(self, 
                 data, 
                 order=None,
                 ):
        orig_shape = data.shape
        orig_dim   = len(orig_shape)
        
        final_order = 'czfxy' # enforced
        if order == None:
            order = final_order
            
        order = order.lower()
        
        
        if orig_dim > 5:
            raise np.AxisError('Only images with <= 5 dimensions are supported.')
        elif orig_dim != len(order):
            raise np.AxisError('Data has {} dimensions, but {} are implied by the order \'{}\''.format(orig_dim, len(order), order))
        elif orig_dim > len(final_order):
            raise np.AxisError('Data has {} dimensions, but only {} are implied by the desired final order \'{}\''.format(orig_dim, len(final_order), final_order))
        
        self.image = data
        
        # locate the dimensions we are missing
        reorder = [ order.find(a) for a in final_order ]
        missing_dims = np.flatnonzero(np.array(reorder)<0)
        
        # add a new length-1 dimension at the front for each missing dimension
        for a in missing_dims:
            self.image = np.expand_dims(self.image, axis=0)
        
        # add these dimensions to the front of the order string
        new_order = ''.join([ final_order[a] for a in missing_dims ]) + order
        
        # find the reorder that gives the final order
        new_reorder = [ new_order.find(a) for a in final_order ]
        
        # transpose the image to the correct order
        self.image = np.transpose(self.image, new_reorder)
        
        self.shape = self.image.shape
        self.dim   = len(self.shape)
        
        self.channels = self.shape[0]
        self.slices = self.shape[1]
        self.frames = self.shape[2]
        
        self.n_images = self.channels * self.slices * self.frames
        
        self.x = self.shape[3]
        self.y = self.shape[4]
        
        if self.channels > 6:
            raise ValueError('Error: channels appear to be {} but maximum is 6 - did you specify the right order?'.format(self.channels))
            
        self.order = final_order
        
        
    
    def __iter__(self):
        self._cur_frame = 0
        self._cur_slice = 0
        self._cur_channel = 0
        self._index = 0
        return self
        
    
    def __next__(self):
        
        # if our 'current channel' is at the # of channels, we have surpassed the end of the array, and should stop.
        if self._cur_channel == self.channels:
            raise StopIteration
        
        cur_data = dict(image=self.image[self._cur_channel, self._cur_slice, self._cur_frame],
                        channel=self._cur_channel,
                        slice=self._cur_slice,
                        frame=self._cur_frame
                       )
        
        # update frame
        self._cur_frame += 1
        
        # if frame is at limit, update slice
        if self._cur_frame == self.frames:
            self._cur_frame = 0
            self._cur_slice += 1
            
        # if slice is at limit, update channel
        # channel will be checked at beginning of next iteration, stopping if it has reached the limit
        if self._cur_slice == self.slices:
            self._cur_slice = 0
            self._cur_channel += 1
            
        return cur_data
        
        
    def __getitem__(self, key):
        
        if type(key) == int:
            key = (key, 0, 0)
            
        if len(key) == 2:
            key = key + (0,)

        return self.image.__getitem__(key)
    
    def __setitem__(self, *args):
        pass
    
    
    def apply(self, func, inplace=False, **kwargs):
        
        result = [ func(a, **kwargs) for a in self ]
        
        result = np.reshape(result, self.shape)
        
        if inplace:
            self.image = result
        else:
            return self.__init__(result)
        
    
    
    





###############################################################################
###############################################################################
################### DotImage Class Definition Start ###########################
###############################################################################
###############################################################################

class DotImage:
    '''
    DotImage: a multidimensional, multichannel image with associated dot-like features
    '''
    def __init__(self, 
                 source,
                 order,
                 desc='',
                 exclude_channels=None, 
                 hybcycle=0,
                 position=0,
                 ref_image=None,
                 z_use=None,
                 ):
        
        '''
        DotImage(source,
                 order,
                 desc='',
                 exclude_channels=None, 
                 hybcycle=0,
                 position=0,
                 ref_image=None,
                 z_use=[0],
                 )
                 
        Main class for dot finding in images.
        Most important parameters:
        * order
            Indicates the starting order of axes in the source image. String containing some or all the letters 'c' (channels), 'z' (slices), 'f' (frames), 'x' and 'y' (image dimensions).
            Whichever order you specify, WBImage will reshape it into a standardized 5D image in the order 'czfxy'. 
            
        * exclude_channels
            Indicates which channel(s) NOT to process with background subtraction and dot finding. Can be an integer, tuple or list of channel indices
            Generally, DAPI channel is not processed. This is usually the final channel, so specify -1 to exclude it.
            The resulting object excludes these channel(s) from self.image and subsequent processed images, but they are preserved in self.raw_image.
        
        * z_use
            Indicates how to deal with z stacks. By default, does nothing and uses all slices in the source image.
            Supplying the string 'max' will take a max projection on all slices in the source image.
            Supply a list or tuple of slice indices will keep only those slices. 
        '''
        
        # if source is a string, assume it is a filename. else, assume it is image data.
        if type(source) == str:
            self.filename = source
            
            if osp.isfile(self.filename):
                data = skimage.io.imread(self.filename)
            else:
                raise ValueError('DotImage: {} is not a file'.format(self.filename))
                
        else:
            self.filename = None
            data = source
            
        
        ### Initialize WBImage on our loaded image data
        self.raw_image = WBImage(data, order=order)
        raw_channels = np.arange(self.raw_image.channels)
        
        if exclude_channels:
            if type(exclude_channels) == list:
                exclude_channels = tuple(exclude_channels) # np.delete expects a scalar or tuple
            working_channels = np.delete(raw_channels, exclude_channels)
        else:
            working_channels = raw_channels
            
        working_image  = WBImage(self.raw_image.image[working_channels], order=self.raw_image.order)

        self.desc = desc
        
        
        self.z_method = None
        # handle Z for a 4d image by max projecting, selecting, or striding, or nothing
        # set self.z_use to list of 'z positions' used - which slices from the original image did we keep
        if working_image.slices > 1:
            if type(z_use) == str and z_use.lower() == 'max':
                self.image = WBImage(np.max(working_image.image, axis=1), order='cfxy') # max projecting removes slice axis
                self.z_method = 'max'
                self.z_use = [0]
            elif type(z_use) == list or type(z_use) == tuple:
                self.image = WBImage(working_image.image[:, z_use, :, :, :])
                self.z_method = 'specify {}'.format(z_use)
                self.z_use = z_use
            else:
                self.z_method = 'full'
                self.z_use = np.arange(0, working_image.slices)
                self.image = working_image
        else:
            self.z_method = 'full'
            self.z_use = np.arange(0, working_image.slices)
            self.image = working_image
        
        
        self.shape    = self.image.shape
        self.channels = self.image.channels
        self.slices   = self.image.slices
        self.frames   = self.image.frames
        
        self.hybcycle = hybcycle
        self.position = position
        
        
        self.bg_subtracted = False
        self.bg_radius = None
        self.aligned = False
        self.align_shift = (0, 0)
        self.align_error = 0.
        self.expanded = False
        
                
    def __repr__(self):
        return 'DotImage, cycle {0} position {1} of shape {2}'.format(self.hybcycle, self.position, self.shape)
        
        
    def dapi_align(self, ref_image, channel=-1, z_slice=None, inter=0):
        
        if type(z_slice) == int:
            z_slice = (z_slice, z_slice)
        elif z_slice == None:
            z_slice = (ref_image.slices//2, self.slices//2)
                
        ref_dapi  = ref_image.raw_image[channel, z_slice[0]]
        self_dapi = self.raw_image[channel, z_slice[1]]
        
        if int(__skimage_version__[1]) < 17:
            register = skimage.feature.register_translation
        else:
            register = skimage.registration.phase_cross_correlation
        
        self.align_shift, self.align_error, _ = register(ref_dapi, self_dapi)
        self.align_shift = self.align_shift.astype(int)
        
        def shift_func(im, **kwargs):
            return scipy.ndimage.shift(im['image'], **kwargs)
        
        self.image.apply(shift_func, inplace=True, 
                         shift=self.align_shift, order=inter, mode='nearest')
        
        self.ref_dapi = ref_dapi
        self.aligned = True
        
    def subtract_background(self, radius=3, bg_image=None):
        
        if (self.bg_subtracted) & (self.bg_radius == radius):
            return
        
        self.bg_radius = radius
        
        if bg_image and bg_image.shape == self.shape:
            try:
                bg_image_wb = WBImage(bg_image)
            except:
                bg_image_wb = bg_image
            image_nobg = [ a['image'] - b['image'] for a, b in zip(self.image, bg_image_wb) ]
            
            self.image_nobg = WBImage(np.reshape(image_nobg, self.shape))
            self.image_bg   = bg_image_wb
            
            return
        
        
        bgsub_pack = itertools.product(iter(self.image), [radius])
        
        def bgsub_map(pack):
            return subtract_background_fft(pack[0]['image'], pack[1])
        
        
        with ThreadPoolExecutor() as pool:
            output = np.array( list(pool.map(bgsub_map, bgsub_pack)) )

            
        output = np.transpose(output, (1, 0, 2, 3))
        
        
        self.image_nobg = WBImage(np.reshape(output[0], self.shape))
        self.image_bg   = np.array([ np.std(b) for b in output[1] ])
        del output
        
        
        self.bg_subtracted = True
        

    
    def find_local_maxes(self, 
                         thresh_abs=0,
                         thresh_coeff=3,
                         mask=None,
                         verbose=False):
        if not self.bg_subtracted:
            if verbose:
                print('find_local_maxes: background subtraction not performed, using raw image.')
            
            self.image_nobg = copy.copy(self.image) # needed for zip() iterator below. otherwise throws an error.
            self.image_bg   = [ np.min(a['image']) for a in self.image_nobg ]
            
        #output_df = pd.DataFrame({
        #    'Slice': pd.Series([], dtype=np.dtype('uint8')),
        #    'Channel': pd.Series([], dtype=np.dtype('uint8')),
        #    'Frame': pd.Series([], dtype=np.dtype('uint8')),
        #    'HybCycle': pd.Series([], dtype=np.dtype('uint16')),
        #    'Position': pd.Series([], dtype=np.dtype('uint8')),
        #    'x': pd.Series([], dtype=np.dtype('uint16')),
        #    'y': pd.Series([], dtype=np.dtype('uint16')),
        #    'area': pd.Series([], dtype=np.dtype('uint8')),
        #    'label': pd.Series([], dtype=np.dtype('int')),
        #    'max_intensity': pd.Series([], dtype=np.dtype('uint16'))
        #})
        
        local_max_images = []
        output_df_temp   = []
        
        if type(thresh_abs) == int:
            thresh_abs = np.repeat(thresh_abs, self.channels)
        
        if type(thresh_coeff) == int:
            thresh_coeff = np.repeat(thresh_coeff, self.channels)
        
        if len(thresh_abs) != self.channels or len(thresh_coeff) != self.channels:
            raise ValueError('find_local_maxes: threshold required for each image channels')
        
        tc = [ thresh_coeff[im['channel']] for im in self.image ]
        ta = [ thresh_abs[im['channel']]   for im in self.image ]
        
        localmax_pack = itertools.product(zip(self.image_nobg, self.image_bg, self.image, tc, ta), [mask], [verbose])
        
        def localmax_map(pack):
            im_data = pack[0]
            mask    = pack[1]
            verbose = pack[2]
            local_maxes, dots_df = local_max_image_2(im_data[0]['image'], # self.image_nobg
                                     im_data[1],          # self.image_bg
                                     thresh_coeff=im_data[3],          # tc
                                     thresh_abs=im_data[4],          # ta
                                     intensity_image=im_data[2]['image'],
                                     mask=mask,
                                     verbose=verbose)
            
            dots_df['Slice']   = im_data[0]['slice']
            dots_df['Channel'] = im_data[0]['channel']
            dots_df['Frame']   = im_data[0]['frame']
            
            return local_maxes, dots_df
            
        
        with ThreadPoolExecutor() as pool:
            packed_results = np.array( list(pool.map(localmax_map, localmax_pack)) )
                        
        local_max_images = [ p[0] for p in packed_results ]
        output_df_temp   = [ p[1] for p in packed_results ]
        
        self.local_max_image = WBImage(np.reshape(local_max_images, self.shape))
        output_df            = pd.concat(output_df_temp)
        
        output_df['HybCycle'] = self.hybcycle
        output_df['Position'] = self.position
                
        output_df = output_df.rename(columns={
                                             'coords': 'Coords',
                                             'max_intensity': 'Intensity',
                                             })
        
        try:
            output_df['Coords'] = output_df.apply(lambda df: np.ravel(df['Coords']), axis=1)
            output_df['x'] = [r[0] for r in output_df['Coords']]
            output_df['y'] = [r[1] for r in output_df['Coords']]
            output_df = output_df.drop(columns='Coords')
        except:
            if verbose:
                print('Found 0 dots on channel {}, slice {}'.format(channel))
        
        #output_df['Intensity'] = [ 
        #                            self.image[ d['Channel'], d['Slice'], d['Frame'], d['Coords'][0], d['Coords'][1] ]
        #                            for _, d in output_df.iterrows() 
        #                         ]
            
        
        self.dots_df = output_df

    
    def get_summary(self):
        grouped = self.dots_df.groupby(['Channel', 'Slice'])
        
        def CoV(data):
            try:
                result = np.std(data) / np.mean(data)
            except:
                result = np.nan
                
            return result
        
        self.summary_df = grouped.agg([min, max, len, np.mean, np.std, np.median, CoV])['Intensity'].reset_index()
        
        
    
    def expand_local_maxes(self, radius=2):
        self.expanded_local_maxes = np.empty_like(self.local_max_image)
            
        for i, im in enumerate(self.local_max_image):
            self.expanded_local_maxes[i] = scipy.ndimage.filters.convolve(im, skimage.morphology.disk(radius))
            
        self.expanded_local_maxes = self.expanded_local_maxes.astype(bool)
            
        self.expanded = True
        
   
###############################################################################
###############################################################################
######################## DotImage Class Definition End ########################
###############################################################################
###############################################################################        
 

###############################################################################
###############################################################################
####################### MultiHyb Class Definition Start #######################
###############################################################################
###############################################################################


class MultiImage:
    '''
    MultiHyb: a multi-hybridization, multi-position sequence of images.
    '''
    def __init__(self,
                data_dir,
                file_list,
                dir_format=('HybCycle_', ''),
                file_format=('MMStack_Pos', '.ome.tif'),
                n_cycles=0,
                n_pos=0,
                n_channels=0,
                dapi_channel=0,
                channel_map=None):
        
        pass
    

    

    
###############################################################################
###############################################################################
######################## MultiHyb Class Definition End ########################
###############################################################################
###############################################################################
    
    

def coloc(*images, window=3):
    '''
    coloc(*images, window=3):
    
    Finds the colocalization between an arbitrary number of binary images of single-pixel local maxima. Does not depend 
    on the order of the arguments. Roughly equivalent to the set theoretical operation on sets of coordinates A and B:
    
    | intersection(A, B) | / | union(A, B) | = (|A| + |B| - | union(A, B) |) / | union(A, B) |
    
    or the bitwise image computation:
    
    sum(A & B) / sum(A | B)
    
    but with tolerance for small shifts in the coordinates when calculating the union.
    `window` defines the side length of a square used to calculate union among dots. 
    All images in `images` will be bitwise OR'd together and dots within the window will be 'merged' into one dot. This allows
    tolerance of small pixelwise shifts due to different dichroics, chromatic aberration, etc. 
    Even with a window size of 0 some merging is performed because dots within an 8-neighborhood in the cumulative OR image
    are considered one dot. 
    '''
    if window > 1:
        expanded_images = [ scipy.ndimage.filters.convolve(im, skimage.morphology.square(window))
                              for im in images ]
    else:
        expanded_images = images
    
    or_image = np.zeros_like(images[0])
    
    for exim in expanded_images:
        or_image = np.bitwise_or(or_image, exim)
    
    _, unique_dots = skimage.measure.label(or_image, background=0, connectivity=2, return_num = True)
    
    return np.sum(images) / unique_dots - 1



def show_two_ims(im_1, im_2, titles=[None, None], interpixel_distances=[1, 1], min_intensity=None, max_intensity=None,
                 color_mapper=None, colorbar=True):
    """
    Convenient function for showing two images side by side.
    This function is adapted slightly from Justin Bois' BE/Bi103 code. The license provided by him for the bebi103 module is as follows:
    Copyright (c) 2017, Justin Bois All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

    Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    """
        
    if min_intensity == None:
        min_intensity = [np.min(im_1.astype(float)), np.min(im_2.astype(float))]
        print(min_intensity)
    
    if max_intensity == None:
        max_intensity = [np.max(im_1.astype(float)), np.max(im_2.astype(float))]
        print(max_intensity)
    
    p_1 = imshow(im_1,
                frame_height=400,
                frame_width=400,
                title=titles[0],
                cmap=color_mapper,
                interpixel_distance=interpixel_distances[0],
                length_units='µm',
                colorbar=colorbar,
                min_intensity=min_intensity[0],
                max_intensity=max_intensity[0]
                )
    p_2 = imshow(im_2,
                frame_height=400,
                frame_width=400,
                title=titles[1],
                cmap=color_mapper,
                interpixel_distance=interpixel_distances[0],
                length_units='µm',
                colorbar=colorbar,
                min_intensity=min_intensity[1],
                max_intensity=max_intensity[1]
                )
    
    p_2.x_range = p_1.x_range
    p_2.y_range = p_1.y_range
        
    
    return bokeh.layouts.gridplot([p_1, p_2], ncols=2)
