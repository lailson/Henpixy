"""
Módulo com ferramentas para processamento de imagens
"""
from henpixy.tools.power import power_transform
from henpixy.tools.contrast_stretching import contrast_stretching
from henpixy.tools.bit_plane_slicing import extract_bit_plane, get_bit_plane_contribution, get_image_bit_depth
from henpixy.tools.histogram import calculate_histogram, equalize_histogram, create_histogram_figure
from henpixy.tools.pseudocolor import intensity_slicing, create_color_gradient, create_predefined_maps, apply_custom_transformation, create_custom_transformation_functions
from henpixy.tools.spatial_filtering import mean_filter 