"""
Módulo com ferramentas para processamento de imagens
"""
from henpixy.tools.power import power_transform
from henpixy.tools.contrast_stretching import contrast_stretching
from henpixy.tools.bit_plane_slicing import extract_bit_plane, reconstruct_from_bit_planes, get_bit_plane_contribution 