import math
import random
import sys, select
from itertools import product

import mahotas as mt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import linalg
from skimage.feature.texture import greycomatrix
from skimage.util.shape import view_as_windows
from enum import Enum


def svd_dominant_angles(dx, dy, dz, svd_radius):
    """Calculate a new numpy image containing the dominant angles for each voxel.

        :param dx: 3D numpy array of the pixel gradient in the x directions
        :type dx: numpy.ndarray

        :returns: image array with the dominant angle calculated at each voxel
        :rtype: numpy.ndarray
    """

    is_3D = dx.shape[2] > 1

    # create rolling windows
    svd_diameter = svd_radius * 2 + 1
    
    # the first (commented out) version would actually take a patch of one slice above and below,
    # but by convention, the third dimension is simply used for the gradient calculation;
    # the actual collection of nearby gradient values to run through the SVD calculation is
    # still done on a given 2D slice
    #window_shape = (svd_diameter, svd_diameter) + ((3 if is_3D else 1),)
    window_shape = (svd_diameter, svd_diameter, 1)
    print(f'Window patch shape for dominant angle calculation = {window_shape}')
    dx_windows = view_as_windows(dx, window_shape)
    dy_windows = view_as_windows(dy, window_shape)
    dz_windows = view_as_windows(dz, window_shape)

    angles_shape = dx_windows.shape[0:3]
    dominant_angles_array = np.zeros(angles_shape + (2 if is_3D else 1,), np.single)

    # loop through each voxel and use SVD to calculate the dominant angle for that rolling window
    # centered on that x,y,z coordinate
    center_x_range = range(angles_shape[1])
    center_y_range = range(angles_shape[0])
    center_z_range = range(angles_shape[2])
    for current_svd_center_x in center_x_range:
        for current_svd_center_y in center_y_range:
            for current_svd_center_z in center_z_range:
                dominant_angles_array[current_svd_center_y, current_svd_center_x, current_svd_center_z, :] = \
                    svd_dominant_angle(\
                        current_svd_center_x, current_svd_center_y, current_svd_center_z,
                        dx_windows, dy_windows, dz_windows)

    return dominant_angles_array


def svd_dominant_angle(x, y, z, dx_windows, dy_windows, dz_windows):
    """Calculates the dominate angle at the coordinate within the windows.

        :param x: x value of coordinate
        :type x: int
        :param y: y value of coordinate
        :type y: int
        :param z: z value of coordinate
        :type z: int
        :param dx_windows: dx windows of x, y shape to run svd upon (shape = rows, cols, slices, row_radius, col_radius, slice_radius)
        :type dx_windows: numpy.ndarray
        :param dy_windows: dy windows of x, y shape to run svd upon
        :type dy_windows: numpy.ndarray
        :param dz_windows: dy windows of x, y shape to run svd upon
        :type dz_windows: numpy.ndarray

        :returns: dominant angle at x, y
        :rtype: float 
    """

    # extract the patch of pixel gradient values for this specific voxel
    dx_patch = dx_windows[y, x, z]
    dy_patch = dy_windows[y, x, z]
    dz_patch = dz_windows[y, x, z]

    is_3D = dx_windows.shape[2] > 1

    # flatten all N gradient values in this patch into an Nxd matrix to pass into svd
    window_area = dx_patch.size
    flattened_gradients = np.zeros((window_area, (3 if is_3D else 2)))
    matrix_order = 'F' # fortran-style to be consistent with original matlab implementation
    flattened_gradients[:, 0] = np.reshape(dx_patch, window_area, order=matrix_order)
    flattened_gradients[:, 1] = np.reshape(dy_patch, window_area, order=matrix_order)
    if is_3D:
        flattened_gradients[:, 2] = np.reshape(dz_patch, window_area, order=matrix_order)

    # calculate svd
    _, _, v = linalg.svd(flattened_gradients)

    # extract results from the first column (in matlab this would be the first row)
    dominant_y = v[0,0]
    dominant_x = v[1,0]

    # calculate the dominant angle for this voxel
    dominant_angle = math.atan2(dominant_y, dominant_x)

    if is_3D:
        # also include the secondary angle
        dominant_z = v[2,0]
        secondary_angle = math.atan2(dominant_z, math.sqrt(dominant_x ** 2 + dominant_y ** 2))
        return (dominant_angle, secondary_angle)
    else:
        return dominant_angle


def show_colored_image(figure, axis, image_data, colormap=plt.cm.jet):
    """Helper method to show a colored image in matplotlib.


        :param figure: figure upon which to display
        :type figure: matplotlib.figure.Figure
        :param axis: axis upon which to display
        :type axis: matplotlib.axes.Axes
        :param image_data: image to display
        :type image_data: numpy.ndarray
        :param colormap: color map to convert for display. Defaults to plt.cm.jet.
        :type colormap: matplotlib.colors.Colormap, optional
    """

    if image_data.ndim == 3:
        image_data = image_data[:,:,0]
    image = axis.imshow(image_data, cmap=colormap)
    divider = make_axes_locatable(axis)
    colorbar_axis = divider.append_axes("right", size="5%", pad=0.05)
    figure.colorbar(image, cax=colorbar_axis)


def create_highlighted_rectangle(x, y, w, h):
    """Creates a matplotlib Rectangle object for a highlight effect


        :param x: x location to start rectangle
        :type x: int
        :param y: y location to start rectangle
        :type y: int
        :param w: width of rectangle
        :type w: int
        :param h: height of rectangle
        :type h: int

        :returns: Rectangle used to highlight within a plot
        :rtype: matplotlib.patches.Rectangle
    """
    return Rectangle((x, y), w, h, linewidth=3, edgecolor='cyan', facecolor='none')


def highlight_rectangle_on_image(image_data, min_x, min_y, w, h, colormap=plt.cm.gray):
    """Highlights a rectangle on an image at the passed in coordinate.


        :param image_data: image to highlight
        :type image_data: numpy.ndarray
        :param min_x: x location to start highlight
        :type min_x: int
        :param min_y: y location to start highlight
        :type min_y: int
        :param w: width of highlight rectangle
        :type w: int
        :param h: height of highlight rectangle
        :type h: int
        :param colormap: color map to convert for display. Defaults to plt.cm.jet.
        :type colormap: matplotlib.colors.Colormap, optional

        :returns: image array with highlighted rectangle
        :rtype: numpy.ndarray
    """
    figure, axes = plt.subplots(1, 2, figsize=(15, 15))

    # Highlight window within image.
    show_colored_image(figure, axes[0], image_data, colormap)
    axes[0].add_patch(create_highlighted_rectangle(min_x, min_y, w, h))

    # Crop window.
    cropped_array = image_data[min_y:min_y + h, min_x:min_x + w]
    axes[1].set_title(f'Cropped Region ({w}x{h})')
    show_colored_image(figure, axes[1], cropped_array, colormap)

    plt.show()

    return cropped_array


def scale_array_for_image(array_to_scale):
    """Scales an array to have 0-255 values as the output

        :param array_to_scale: array to scale
        :type array_to_scale: numpy.ndarray

        :returns: array scaled from 0-255
        :rtype: numpy.ndarray
    """
    minimum = float(array_to_scale.min())
    maximum = float(array_to_scale.max())
    array_range = maximum - minimum
    array_to_scale = array_to_scale - minimum
    array_to_scale /= array_range
    array_to_scale *= 255
    return array_to_scale


class HaralickFeature(Enum):
    """Enumeration Helper For Haralick Features


        :param Enum: Enumeration Helper For Haralick Features
        :type Enum: HaralickFeature
    """
    AngularSecondMoment = 0
    Contrast = 1
    Correlation = 2
    SumOfSquareVariance = 3
    SumAverage = 4
    SumVariance = 5
    SumEntropy = 6
    Entropy = 7
    DifferenceVariance = 8
    DifferenceEntropy = 9
    InformationMeasureOfCorrelation1 = 10
    InformationMeasureOfCorrelation2 = 11
    MaximalCorrelationCoefficient = 12
    All = 13


class DifferenceVarianceInterpretation(Enum):
    """ Feature 10 has two interpretations, as the variance of |x-y|
        or as the variance of P(|x-y|).
        See: https://ieeexplore.ieee.org/document/4309314

        :param Enum: Enumeration Helper For Haralick Features
        :type Enum: DifferenceVarianceInterpretation
    """
    XMinusYVariance = 0
    ProbabilityXMinusYVariance = 1


class Collage:
    """This is the main object in the Collage calculation system. Usage: create a Collage object and then call the :py:meth:`execute` function.

        :param image_array: image to run collage upon
        :type image_array: numpy.ndarray
        :param mask_array: mask that correlates with the image
        :type mask_array: numpy.ndarray
        :param svd_radius: radius of svd. Defaults to 5.
        :type svd_radius: int, optional
        :param verbose_logging: turning this on will log intermediate results]. Defaults to False.
        :type verbose_logging: bool, optional
        :param cooccurence_angles: list of angles to use in the cooccurence matrix. Defaults to [x*numpy.pi/4 for x in range(8)]
        :type cooccurence_angles: list, optional
        :param difference_variance_interpretation: Feature 10 has two interpretations, as the variance of |x-y| or as the variance of P(|x-y|).].Defaults to DifferenceVarianceInterpretation.XMinusYVariance.
        :type difference_variance_interpretation: DifferenceVarianceInterpretation, optional
        :param haralick_window_size: size of rolling window for texture calculations. Defaults to -1.
        :type haralick_window_size: int, optional
        :param num_unique_angles: number of bins to use for the texture calculation. Defaults to 64.
        :type num_unique_angles: int, optional
    """


    @property
    def img_array(self):
        """
        The original image.

        :getter: Returns the original image array.
        :setter: Sets the original image array.
        :type: np.ndarray
        """
        return self._img_array

    @property
    def mask_array(self):
        """
        Array passed into Collage.

        :getter: Returns the original mask array.
        :setter: Sets the original mask array.
        :type: np.ndarray
        """        
        return self._mask_array

    @property
    def is_3D(self):
        """
        Whether we are using 3D collage calculations (True) or 2D (False)
        """
        return self._is_3D

    @property
    def svd_radius(self):
        """
        SVD radius is used to calculate the pixel radius
        for the dominant angle calculation.

        :getter: Returns the SVD radius.
        :setter: Sets the SVD radius.
        :type: int
        """   
        return self._svd_radius

    @property
    def verbose_logging(self):
        """
        Turning this on will result in more
        detailed logging.

        :getter: Returns True if on.
        :setter: Turns verbose logging off or on.
        :type: bool
        """
        return self._verbose_logging

    @property
    def cooccurence_angles(self):
        """
        Iterable of angles that will be used in the cooccurence matrix.

        :getter: Returns the Iterable of cooccurence angles.
        :setter: Sets the angles to be used in the cooccurence matrix.
        :type: int
        """
        return self._cooccurence_angles

    @property
    def difference_variance_interpretation(self):
        """
        Feature 10 has two interpretations, as the variance of |x-y| or as the variance of P(|x-y|).].
        Defaults to DifferenceVarianceInterpretation.XMinusYVariance.

        :getter: Returns requested variance interpretation.
        :setter: Sets requested variance interpretation.
        :type: DifferenceVarianceInterpretation
        """
        return self._difference_variance_interpretation

    @property
    def haralick_window_size(self):
        """
        Number of pixels around each pixel to calculate a haralick texture.

        :getter: Returns requested number of pixels.
        :setter: Sets requested number of pixels.
        :type: int
        """
        return self._haralick_window_size

    @property
    def num_unique_angles(self):
        """
        Number of bins to use for texture calculations. Defaults to 64.

        :getter: Returns requested number of unique angles to bin into.
        :type: int
        """
        return self._num_unique_angles

    @property
    def collage_output(self):
        """
        Array representing collage upon the mask within the full images.
        If the input was 2D, the output will be height×width×13 where "13" is the number of haralick textures.
        If the input was 3D, the output will be height×width×depth×13x2 where "2" is the primary angle (element 0) or the secondary angle (element 1)

        The output will have numpy.nan values everywhere outside the masked region.

        :getter: Returns array the same shape as the original image with collage in the mask region.
        :type: numpy.ndarray
        """
        return self._collage_output

    @collage_output.setter
    def collage_output(self, value):
        self._collage_output = value


    def __init__(self,
                 img_array,
                 mask_array,
                 svd_radius=5,
                 verbose_logging=False,
                 cooccurence_angles=[x * np.pi/4 for x in range(8)],
                 difference_variance_interpretation=DifferenceVarianceInterpretation.XMinusYVariance,
                 haralick_window_size=-1,
                 num_unique_angles=64,
                 ):
        """Designated initializer for Collage

            :param image_array: image to run collage upon
            :type image_array: numpy.ndarray
            :param mask_array: mask that correlates with the image
            :type mask_array: numpy.ndarray
            :param svd_radius: radius of svd. Defaults to 5.
            :type svd_radius: int, optional
            :param verbose_logging: turning this on will log intermediate results. Defaults to False.
            :type verbose_logging: bool, optional
            :param cooccurence_angles: list of angles to use in the cooccurence matrix. Defaults to [x * np.pi/4 for x in range(8)]
            :type cooccurence_angles: list, optional
            :param difference_variance_interpretation: Feature 10 has two interpretations, as the variance of |x-y| or as the variance of P(|x-y|).].Defaults to DifferenceVarianceInterpretation.XMinusYVariance.
            :type difference_variance_interpretation: DifferenceVarianceInterpretation, optional
            :param haralick_window_size: size of rolling window for texture calculations. Defaults to -1.
            :type haralick_window_size: int, optional
            :param num_unique_angles: number of bins to use for the texture calculation. Defaults to 64.
            :type num_unique_angles: int, optional
        """

        if verbose_logging:
            print('Collage Module Initialized')

        # error checking
        if haralick_window_size == -1:
            self._haralick_window_size = svd_radius * 2 + 1
        else:
            self._haralick_window_size = haralick_window_size

        if self._haralick_window_size < 1:
            raise Exception('Haralick windows size must be at least 1 pixel.')

        if svd_radius < 1:
            raise Exception('SVD radius must be at least 1 pixel')

        if num_unique_angles < 1:
            raise Exception('num_unique_angles must contain at least 1 bin')

        if img_array.ndim < 2 or img_array.ndim > 3:
            raise Exception('Expected a 2D or 3D image.')

        if mask_array.shape != img_array.shape:
            raise Exception('Mask must be the same shape as image.')

        self._is_3D = img_array.ndim == 3
        if verbose_logging:
            print(f'Running 3D Collage = {self.is_3D}')

        self._img_array = img_array
        if not self.is_3D:
            # in the case of a single 2D slice, give it a third dimension of unit length
            self._img_array = self._img_array.reshape(self._img_array.shape + (1,))

        min_3D_slices = 3;
        if self._img_array.shape[0] <  self._haralick_window_size or self._img_array.shape[1] < self._haralick_window_size or (self._is_3D and self._img_array.shape[2] < min_3D_slices):
            raise Exception(
                f'Image is too small for a window size of {self._haralick_window_size} pixels.')

        # threshold mask
        uniqueValues = np.unique(mask_array)
        numberOfValues = len(uniqueValues)
        if numberOfValues > 2:
            print(f'Warning: Mask is not binary. Considering all {numberOfValues} nonzero values in the mask as a value of True.')
        thresholded_mask_array = (mask_array != 0)

        # make correct shape
        thresholded_mask_array = thresholded_mask_array.reshape(self.img_array.shape)

        # extract rectangular area of mask
        non_zero_indices = np.argwhere(thresholded_mask_array)
        min_mask_coordinates = non_zero_indices.min(0)
        max_mask_coordinates = non_zero_indices.max(0)+1
        self.mask_min_x = min_mask_coordinates[1]
        self.mask_min_y = min_mask_coordinates[0]
        self.mask_min_z = min_mask_coordinates[2]
        self.mask_max_x = max_mask_coordinates[1]
        self.mask_max_y = max_mask_coordinates[0]
        self.mask_max_z = max_mask_coordinates[2]

        cropped_mask_array = thresholded_mask_array[self.mask_min_y:self.mask_max_y,
                                                    self.mask_min_x:self.mask_max_x,
                                                    self.mask_min_z:self.mask_max_z]

        # store variables internally
        self._mask_array = cropped_mask_array

        self._svd_radius = svd_radius
        self._verbose_logging = verbose_logging

        self._cooccurence_angles = cooccurence_angles
        self._difference_variance_interpretation = difference_variance_interpretation

        self._num_unique_angles = num_unique_angles


    def calculate_haralick_feature_values(self, img_array, center_x, center_y):

        """Gets the haralick texture feature values at the x, y, z coordinate.
, pos[1]
            :param image_array: image to calculate texture
            :type image_array: numpy.ndarray
            :param center_x: x center of coordinate
            :type center_x: int
            :param center_y: y center of coordinate
            :type center_y: int
            :param window_size: size of window to pull for calculation
            :type window_size: int
            :param num_unique_angles: number of bins
            :type num_unique_angles: int
            :param haralick_feature: desired haralick feature
            :type haralick_feature: HaralickFeature

            :returns: A 13x1 vector of haralick texture at the coordinate.
            :rtype: numpy.ndarray
        """
        # extract subpart of image (todo: pass in result from view_as_windows)
        window_size = self.haralick_window_size
        min_x = int(max(0, center_x - window_size / 2 - 1))
        min_y = int(max(0, center_y - window_size / 2 - 1))
        max_x = int(min(img_array.shape[1] - 1, center_x + window_size / 2 + 1))
        max_y = int(min(img_array.shape[0] - 1, center_y + window_size / 2 + 1))
        cropped_img_array = img_array[min_y:max_y, min_x:max_x]

        # co-occurence matrix of all 8 directions and sum them
        cooccurence_matrix = greycomatrix(cropped_img_array, [1], self.cooccurence_angles, levels=self.num_unique_angles)
        cooccurence_matrix = np.sum(cooccurence_matrix, axis=3)
        cooccurence_matrix = cooccurence_matrix[:, :, 0]

        # extract haralick using mahotas library
        return mt.features.texture.haralick_features([cooccurence_matrix], return_mean=True)


    def calculate_haralick_textures(self, dominant_angles):
        """Gets haralick texture values 

            :param dominant_angles_array: An image of the dominant angles at each voxel
            :type dominant_angles_[:,:,:,feature_index]array: numpy.ndarray
            :param desired_haralick_feature: which feature to calculate
            :type desired_haralick_feature: Haralick Feature
            :param num_unique_angles: number of bins
            :type num_unique_angles: int
            :param haralick_window_size: size of window around pixels to calculate haralick value

            :returns: An hxwxdx13 set of haralick texture.
            :rtype: numpy.ndarray
        """

        # rescale from 0 to (num_unique_angles-1)
        num_unique_angles = self.num_unique_angles
        if self.verbose_logging:
            print(f'Rescaling dominant angles to {num_unique_angles} unique values.')
        dominant_angles_max = dominant_angles.max()
        dominant_angles_min = dominant_angles.min()
        dominant_angles_binned = (dominant_angles - dominant_angles_min) / (dominant_angles_max - dominant_angles_min) * (num_unique_angles - 1)
        dominant_angles_binned = np.round(dominant_angles_binned).astype(int)
        if self.verbose_logging:
            print(f'Rescaling dominant angles done.')

        # prepare output
        shape = dominant_angles_binned.shape
        haralick_image = np.empty(shape + (13,))
        haralick_image[:] = np.nan

        # the haralick is calculated for each slice separately
        height, width, depth = shape
        for z in range(depth):
            for y,x in product(range(height), range(width)):
                if self.mask_array[y,x,z]:
                    haralick_image[y,x,z,:] = self.calculate_haralick_feature_values(dominant_angles_binned[:,:,z], x, y)

        return haralick_image


    def execute(self):
        """Begins haralick calculation.

            :returns: An image at original size that only has the masked section filled in with collage calculations.
            :rtype: numpy.ndarray
        """

        svd_radius = self.svd_radius

        # mask location
        mask_min_x = int(self.mask_min_x)
        mask_min_y = int(self.mask_min_y)
        mask_min_z = int(self.mask_min_z)
        mask_max_x = int(self.mask_max_x)
        mask_max_y = int(self.mask_max_y)
        mask_max_z = int(self.mask_max_z)

        mask_width  = mask_max_x - mask_min_x
        mask_height = mask_max_y - mask_min_y
        mask_depth  = mask_max_z - mask_min_z

        img_array = self.img_array

        # extend the mask outwards a bit (up to the edge of the image) to handle the svd radius
        cropped_min_x = max(mask_min_x - svd_radius, 0)
        cropped_min_y = max(mask_min_y - svd_radius, 0)
        cropped_min_z = max(mask_min_z - 1         , 0) # for 3D, we just extend 1 slice in both directions
        cropped_max_x = min(mask_max_x + svd_radius, img_array.shape[1])
        cropped_max_y = min(mask_max_y + svd_radius, img_array.shape[0])
        cropped_max_z = min(mask_max_z + 1         , img_array.shape[2])

        cropped_image = img_array[cropped_min_y:cropped_max_y,
                                  cropped_min_x:cropped_max_x,
                                  cropped_min_z:cropped_max_z]

        if self.verbose_logging:
            print(f'Image shape = {img_array.shape}')
            print(f'Mask size = {mask_height}x{mask_width}x{mask_depth}')
            print(f'Image shape (cropped and padded) = {cropped_image.shape}')

        # ensure the image values range from 0-1
        if cropped_image.max() > 1:
            if self.verbose_logging:
                print('Note: Dividing image values by 255 to convert to 0-1 range')
            cropped_image = cropped_image / 255.

        # calculate x,y,z gradients
        if self.verbose_logging:
            print('Calculating pixel gradients:')
        dx = np.gradient(cropped_image, axis=1)
        dy = np.gradient(cropped_image, axis=0)
        dz = np.gradient(cropped_image, axis=2) if self.is_3D else np.zeros(dx.shape)
        self.dx = dx
        self.dy = dy
        self.dz = dz
        if self.verbose_logging:
            print('Calculating pixel gradients done.')

        # calculate dominant angles of each patch
        if self.verbose_logging:
            print(f'Calculating dominant gradient angles using SVD for each image patch of size {svd_radius}x{svd_radius}')
        dominant_angles = svd_dominant_angles(dx, dy, dz, svd_radius)
        self.dominant_angles = dominant_angles
        angles_shape = dominant_angles.shape
        if self.verbose_logging:
            print('Calculating dominant gradient angles done.')
            print(f'Dominant angles shape = {angles_shape}')

        # calculate haralick features of the dominant angles
        if self.verbose_logging:
            print('Calculating haralick features of angles:')
        haralick_features = np.empty(angles_shape[0:3] + (13, 2 if self.is_3D else 1,))
        haralick_features[:] = np.nan
        for angle_index in range(angles_shape[3]):
            print(f'Calculating features for angle {angle_index}:')
            haralick_features[:,:,:,:,angle_index] = self.calculate_haralick_textures(dominant_angles[:,:,:,angle_index])
            print(f'Calculating features for angle {angle_index} done.')
        if self.verbose_logging:
            print('Calculating haralick features of angles done.')

        # prepare an output full of "NaN's"
        collage_output = np.empty(img_array.shape + haralick_features.shape[3:5])
        collage_output[:] = np.nan
        print(collage_output.shape)

        # insert the haralick output into the correct spot
        collage_output[mask_min_y:mask_max_y,
                       mask_min_x:mask_max_x,
                       mask_min_z:mask_max_z,
                       :, :] = haralick_features

        # remove the singleton third dimension from the output
        if not self.is_3D:
            collage_output = np.squeeze(collage_output, 4)
            collage_output = np.squeeze(collage_output, 2)

        # output
        self.collage_output = collage_output
        if self.verbose_logging:
            print(f'Output shape = {collage_output.shape}')
        return collage_output
