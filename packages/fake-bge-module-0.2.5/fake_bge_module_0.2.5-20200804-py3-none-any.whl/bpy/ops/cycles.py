import sys
import typing


def denoise_animation(input_filepath: str = "", output_filepath: str = ""):
    ''' Denoise rendered animation sequence using current scene and view layer settings. Requires denoising data passes and output to OpenEXR multilayer files

    :param input_filepath: Input Filepath, File path for image to denoise. If not specified, uses the render file path and frame range from the scene
    :type input_filepath: str
    :param output_filepath: Output Filepath, If not specified, renders will be denoised in-place
    :type output_filepath: str
    '''

    pass


def merge_images():
    ''' Combine OpenEXR multilayer images rendered with different sampleranges into one image with reduced noise

    '''

    pass


def use_shading_nodes():
    ''' Enable nodes on a material, world or lamp

    '''

    pass
