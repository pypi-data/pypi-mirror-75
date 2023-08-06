# Simpledots image analysis

Dot detection and file management for seqFISH-type experiments.

By Lincoln Ombelets, 2019-2020

Distributed under the MIT license.

# Classes

## WBImage
This is a simple container class for gracefully dealing with multidimensional images in a standardized way. 

In our research, we commonly encounter 2, 3, or 4 dimensional images. The first 2 dimensions are just the horizontal and vertical dimensions, and each 2D image is a single snap from the microscope camera. But many snaps are often bundled together with changes in either Z (depth) position or fluorescent channel. Finally, rarely you may have multiple time points or "frames", representing a fifth dimension. 

`WBImage` facilitates dealing with any dimensionality image in roughly the same way, by expanding any image to 5D, adding length 1 dimensions that are missing. 

The only thing you have to specify is the order of the dimensions of the raw image. You can ascertain this by loading in the image (for example, with `skimage.io.imread()`) and checking the `shape`:

```python
im = skimage.io.imread('C:\path\to\image.tif')
print(im.shape)
```

Generally, this will print out something like (depending on the type of experiment and the software that produced the image) `(10, 2048, 2048, 4)`. You know your own experiments best, so from this information you can usually determine the way Python is naively reading the image. In this case, the order would be Z slices - X - Y - Fluorescent channels. We would specify this with the single-letter shorthand `zxyc`, which is supplied to the constructor:

```python
wb_im = WBImage(im, order='zxyc')
print(wb_im.shape)
> (4, 10, 1, 2048, 2048)
```

The WBImage constructor reordered the axes and inserted a length-1 `frames` axis to bring the image to the final standard shape `czfxy`.
Note that if you do not specify an order, WBImage assumes the image is already in the final standard shape.

`WBImage` instances can be indexed for reading similarly to `ndarray`s:

```python    
wb_im[1, 4].shape # this is the same as wb_im[1, 4, 0]
> (2048, 2048)
```
    
This would give the second channel, fifth Z slice image.

The image itself is stored as a reshaped `ndarray` in `wb_im.image`.

They can also be iterated as if they were flat arrays of `c*z*f` 2D images, but supply a `dict` with channel, slice and frame information:
```python
for a in wb_im:
    print(a.keys())
```

The keys of the iterator are `channel`, `slice`, `frame`, and `image` containing the 2D `x*y` image.

Finally, the `apply` method loops through the stack in this manner and applies a given function (with optional keyword arguments) to each 2D image, either returning a new `WBImage` instance or modifying the current one in place.

```python
def filter_wbimage(im, sigmas):
    return skimage.filters.gaussian(im['image'], sigma=sigmas[im['channel']])

wb_im_filtered = wb_im.apply(filter_wbimage, inplace=False, sigmas=[4, 2, 1, 1])
```

The above code would apply a different width Gaussian filter to each channel. The applied function receives the same `dict` as any iterator, so you can use the channel, slice and frame information in your function.


## DotImage

This is the main class for dealing with smFISH-like images. Its main functions at present are to perform background subtraction, registration to a reference image, and find and quantify dots. All stages of the image processing are stored as `WBImage`s.

### Constructor

Similar to `WBImage`, the only required arguments to the constructor are an image (filename or preloaded `ndarray`) and a string indicating the axes order of the raw image. However, the full constructor looks like this:

```python
    def __init__(self, 
                 source,
                 order,
                 desc='',
                 exclude_channels=None, 
                 hybcycle=0,
                 position=0,
                 ref_image=None,
                 z_use=[0],
                 ):
```

`source` and `order` are the required arguments. `desc`, `hybcycle`, `position` are metadata that you can add optionally.
`exclude_channels` lets you indicate which channels *not* to process with background subtraction, dot finding etc. Typically the final channel in our images is DAPI, a nuclear stain. You can supply a single integer or a list of integers to exclude them from the analysis.
To exclude DAPI, assuming it's the final channel, you would supply `exclude_channels=-1`.

`z_use` allows you to change how Z slices are handled.

`z_use = 0` or `z_use = [1, 5, 7]` only keeps the specified Z slices in the analysis.

`z_use = 'max'` takes a maximum projection along the Z slices, collapsing the image to a single slice. This can greatly speed up the analysis by reducing the number of 2D images to process, so long as 3D information is not needed.

Leaving `z_use` empty includes all Z slices in the analysis.

After calling the constructor, the *raw* image - with all channels and slices - is found in `im.raw_image`, and the *working* image, without excluded channels and after Z processing, is in `im.image`. `im.shape`, `im.channels`, `im.slices`, `im.frames` refer to the *working* image's shape.

### Processing methods

#### dapi_align
```python
def dapi_align(self, ref_image, channel=-1, z_slice=None, inter=0):
```

This function performs 2D image alignment between the current object and a given `DotImage`, `ref_image`. The channel to perform cross-correlation on is given as -1 by default, because that is typically the DAPI channel - note that this `channel` argument refers to the `raw_image`, containing channels that were excluded in the constructor.

 `z_slice` allows you to specify which slices to use - it can be a tuple in case they are different between the current image and the reference image, or a single integer. If not supplied, the *middle z slice* of each image is used, by reasoning that this may be most likely to have in focus signal. 

 The `inter` argument allows you to specify the order of interpolation performed in the shift operation. By default it is 0, which is equivalent to pixel-resolution alignment - no subpixel shift is possible without higher order. Higher orders allow finer shifts, but potentially alter the dot intensities.


 After running this method, the `align_shift` attribute contains a tuple of the shifts in each direction, and `ref_dapi` contains the 2D DAPI image used as a reference.

#### subtract_background

```python
def subtract_background(self, radius=3, bg_image=None):
```

This method performs a Gaussian blur on each 2D subimage, then subtracts the blurred image from the original. `radius` specifies the sigma of the Gaussian filter applied - a larger radius retains more lower frequency features while keeping the signal higher, while a smaller radius discards more features at the expense of some real signal intensity. Typically, a radius of a little bigger than the expected size of real dots is used to selectively retain real features.

Alternatively, if an actual background image is available, it can be supplied as a `WBImage` which must have the same shape as the current image. Each 2D image of this will be subtracted from the corresponding image in the current object.


After running this method, the `image_nobg` attribute contains the background-subtracted `WBImage`, and `image_bg` contains an array of *standard deviations* of each background (blurred) image. The standard deviation of the background image is used in `find_local_maxes` as a basis for relative thresholding of dots.

Note that the convolutions (actually forward and inverse Fourier Transforms with multiplications) needed for computing this function are expensive for high-dimensional images (such as those with many Z slices). Typically this method runs much longer than `find_local_maxes`. `find_local_maxes` can run on raw, non-background subtracted images as well if desired; thresholding is somewhat tougher and must be optimized manually. In the future, a faster routine that either averages along Z or only computes the blur periodically could be implemented to reduce the number of convolutions. 

#### find_local_maxes
```python
def find_local_maxes(self, 
                    thresh_abs=0,
                    thresh_coeff=3,
                    mask=None,
                    verbose=False):
```

This method identifies local maxima pixels in each 2D subimage of the current object. The most important parameters to optimize are the thresholds. `thresh_abs`, if supplied, *takes precedence* over `thresh_coeff.`, and specifies the minimum absolute pixel value to call a local maximum. `thresh_coeff`, which is used by default, is the multiplier applied to one of two measures of 'background':

1. If background subtraction has been performed, each subimage is thresholded on `thresh_coeff` times the *standard deviation of its background image*
2. If no background subtraction was performed, each subimage is thresholded on `thresh_coeff` times the *minimum value of the raw image* (though will likely change this to a quantile-based measure).

For both of these, a single number can be supplied, *or a list of numbers*, one for each channel. This is useful for channels that have different typical backgrounds. 

`mask` is a binary 2D image of the same XY dimensions as the current image that can be used to specify where to look or not to look for dots.

If `verbose` is `True`, messages about the thresholds applied and number of dots identified in each subimage are printed.


The outputs of `find_local_maxes` are:

1. A *binary* `WBImage` called `local_max_image` where identified local maxima are `True` and all other pixels are `False`
2. A `DataFrame` called `dots_df` containing the information about every dot identified. This can be quite a long DataFrame. Its columns are:
    1. `Coords`: A length-2 list with the X and Y pixel location
    2. `Label`: An integer label that is unique to each dot
    3. `Area`: Area in pixels of the local maximum, should always be 1
    4. `Intensity`: Pixel intensity of the dot *from the non-background subtracted image*
    5. `Channel`: Channel dot was found in.
    6. `Slice`: Z slice dot was found in
    7. `Frame`: Time frame dot was found in
    8. `HybCycle`: `hybcycle` attribute of current image
    9. `Position`: `position` attribute of current image

Thus, `dots_df` contains all of the information needed to quantify intensity, position (in 3D) and channel of all identified local maxima. 
