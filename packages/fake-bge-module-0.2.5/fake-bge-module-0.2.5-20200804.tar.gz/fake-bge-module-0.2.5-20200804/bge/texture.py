import sys
import typing
import bpy.context


class DeckLink:
    ''' Certain DeckLink devices can be used to playback video: the host sends video frames regularly for immediate or scheduled playback. The video feed is outputted on HDMI or SDI interfaces. This class supports the immediate playback mode: it has a source attribute that is assigned one of the source object in the bge.texture module. Refreshing the DeckLink object causes the image source to be computed and sent to the DeckLink device for immediate transmission on the output interfaces. Keying is supported: it allows to composite the frame with an input video feed that transits through the DeckLink card. :arg cardIdx: Number of the card to be used for output (0=first card). It should be noted that DeckLink devices are usually half duplex: they can either be used for capture or playback but not both at the same time. :type cardIdx: int :arg format: String representing the display mode of the output feed. :type format: str The default value of the format argument is reserved for auto detection but it is currently not supported (it will generate a runtime error) and thus the video format must be explicitly specified. If keying is the goal (see keying attributes), the format must match exactly the input video feed, otherwise it can be any format supported by the device (there will be a runtime error if not). The format of the string is <displayMode>[/3D] . Refer to VideoDeckLink to get the list of acceptable <displayMode> . The optional /3D suffix is used to create a stereo 3D feed. In that case the 'right' attribute must also be set to specify the image source for the right eye. Note: The pixel format is not specified here because it is always BGRA. The alpha channel is used in keying to mix the source with the input video feed, otherwise it is not used. If a conversion is needed to match the native video format, it is done inside the DeckLink driver or device.
    '''

    source: typing.Union['VideoFFmpeg', 'ImageMirror', 'ImageViewport',
                         'VideoDeckLink', 'ImageBuff', 'ImageMix',
                         'ImageRender', 'ImageFFmpeg'] = None
    ''' This attribute must be set to one of the image sources. If the image size does not fit exactly the frame size, the extend attribute determines what to do. For best performance, the source image should match exactly the size of the output frame. A further optimization is achieved if the image source object is ImageViewport or ImageRender set for whole viewport, flip disabled and no filter: the GL frame buffer is copied directly to the image buffer and directly from there to the DeckLink card (hence no buffer to buffer copy inside VideoTexture).

    :type: typing.Union['VideoFFmpeg', 'ImageMirror', 'ImageViewport', 'VideoDeckLink', 'ImageBuff', 'ImageMix', 'ImageRender', 'ImageFFmpeg']
    '''

    right: typing.Union['VideoFFmpeg', 'ImageMirror', 'ImageViewport',
                        'VideoDeckLink', 'ImageBuff', 'ImageMix',
                        'ImageRender', 'ImageFFmpeg'] = None
    ''' If the video format is stereo 3D, this attribute should be set to an image source object that will produce the right eye images. If the goal is to render the BGE scene in 3D, it can be achieved with 2 cameras, one for each eye, used by 2 ImageRender with an offscreen render buffer that is just the size of the video frame.

    :type: typing.Union['VideoFFmpeg', 'ImageMirror', 'ImageViewport', 'VideoDeckLink', 'ImageBuff', 'ImageMix', 'ImageRender', 'ImageFFmpeg']
    '''

    keying: bool = None
    ''' Specify if keying is enabled. False (default): the output frame is sent unmodified on the output interface (in that case no input video is required). True: the output frame is mixed with the input video, using the alpha channel to blend the two images and the combination is sent on the output interface.

    :type: bool
    '''

    level: int = None
    ''' If keying is enabled, sets the keying level from 0 to 255. This value is a global alpha value that multiplies the alpha channel of the image source. Use 255 (the default) to keep the alpha channel unmodified, 0 to make the output frame totally transparent.

    :type: int
    '''

    extend: bool = None
    ''' Determines how the image source should be mapped if the size does not fit the video frame size. * False (the default): map the image pixel by pixel. If the image size is smaller than the frame size, extra space around the image is filled with 0-alpha black. If it is larger, the image is cropped to fit the frame size. * True: the image is scaled by the nearest neighbor algorithm to fit the frame size. The scaling is fast but poor quality. For best results, always adjust the image source to match the size of the output video.

    :type: bool
    '''

    def close(self):
        ''' Close the DeckLink device and release all resources. After calling this method, the object cannot be reactivated, it must be destroyed and a new DeckLink object created from fresh to restart the output.

        '''
        pass

    def refresh(self, refresh_source: bool, ts: float):
        ''' This method must be called frequently to update the output frame in the DeckLink device.

        :param refresh_source: True if the source objects image buffer should be invalidated after being used to compute the output frame. This triggers the recomputing of the source image on next refresh, which is normally the desired effect. False if the image source buffer should stay valid and reused on next refresh. Note that the DeckLink device stores the output frame and replays until a new frame is sent from the host. Thus, it is not necessary to refresh the DeckLink object if it is known that the image source has not changed.
        :type refresh_source: bool
        :param ts: The timestamp value passed to the image source object to compute the image. If unspecified, the BGE clock is used.
        :type ts: float
        '''
        pass


class FilterBGR24:
    ''' Source filter BGR24.
    '''

    pass


class FilterBlueScreen:
    ''' Filter for Blue Screen. The RGB channels of the color are left unchanged, while the output alpha is obtained as follows: - if the square of the euclidian distance between the RGB color and the filter's reference color is smaller than the filter's lower limit, the output alpha is set to 0; - if that square is bigger than the filter's upper limit, the output alpha is set to 255; - otherwise the output alpha is linarly extrapoled between 0 and 255 in the interval of the limits.
    '''

    color: list = None
    ''' Reference color. :default: (0, 0, 255)

    :type: list
    '''

    limits: list = None
    ''' Reference color limits. :default: (64, 64)

    :type: list
    '''

    previous = None
    ''' Previous pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''


class FilterColor:
    ''' Filter for color calculations. The output color is obtained by multiplying the reduced 4x4 matrix with the input color and adding the remaining column to the result.
    '''

    matrix: list = None
    ''' Matrix [4][5] for color calculation. :default: ((256, 0, 0, 0, 0), (0, 256, 0, 0, 0), (0, 0, 256, 0, 0), (0, 0, 0, 256, 0))

    :type: list
    '''

    previous = None
    ''' Previous pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''


class FilterGray:
    ''' Filter for grayscale effect. Proportions of R, G and B contributions in the output grayscale are 28:151:77.
    '''

    previous = None
    ''' Previous pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''


class FilterLevel:
    ''' Filter for levels calculations. Each output color component is obtained as follows: * if it is smaller than its corresponding min value, it is set to 0; * if it is bigger than its corresponding max value, it is set to 255; * Otherwise it is linearly extrapoled between 0 and 255 in the (min, max) interval.
    '''

    levels: list = None
    ''' Levels matrix [4] (min, max). :default: ((0, 255), (0, 255), (0, 255), (0, 255))

    :type: list
    '''

    previous = None
    ''' Previous pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''


class FilterNormal:
    ''' Normal map filter.
    '''

    colorIdx: int = None
    ''' Index of color used to calculate normal (0 - red, 1 - green, 2 - blue, 3 - alpha). :default: 0

    :type: int
    '''

    depth: float = None
    ''' Depth of relief. :default: 4.0

    :type: float
    '''

    previous = None
    ''' Previous pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''


class FilterRGB24:
    ''' Returns a new input filter object to be used with ImageBuff object when the image passed to the :meth: ImageBuff.load function has the 3-bytes pixel format BGR.
    '''

    pass


class FilterRGBA32:
    ''' Source filter RGBA32.
    '''

    pass


class ImageBuff:
    ''' Image from application memory. For computer generated images, drawing applications. :arg width: Width of the image. :type width: int :arg height: Height of the image. :type height: int :arg color: Value to initialize RGB channels with. The initialized buffer will have all pixels set to (color, color, color, 255). (optional) :type color: int in [0, 255] :arg scale: Image uses scaling. (optional) :type scale: bool
    '''

    filter = None
    ''' Pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''

    flip: bool = None
    ''' Flip image vertically.

    :type: bool
    '''

    image = None
    ''' Image data. (readonly)'''

    scale: bool = None
    ''' Fast scale of image (near neighbour).

    :type: bool
    '''

    size: tuple = None
    ''' Image size. (readonly)

    :type: tuple
    '''

    valid: bool = None
    ''' Tells if an image is available. (readonly)

    :type: bool
    '''

    def load(self, imageBuffer: typing.Union[bytes, 'bpy.context.object'],
             width: int, height: int):
        ''' Load image from buffer.

        :param imageBuffer: Buffer to load the image from.
        :type imageBuffer: typing.Union[bytes, 'bpy.context.object']
        :param width: Width of the image to load.
        :type width: int
        :param height: Height of the image to load.
        :type height: int
        '''
        pass

    def plot(self,
             imageBuffer: typing.
             Union[bytes, 'bpy.context.object', 'ImageBuff'],
             width: int,
             height: int,
             positionX: int,
             positionY: int,
             mode: int = 'IMB_BLEND_COPY'):
        ''' Update image buffer.

        :param imageBuffer: Buffer to load the new data from.
        :type imageBuffer: typing.Union[bytes, 'bpy.context.object', 'ImageBuff']
        :param width: Width of the data to load.
        :type width: int
        :param height: Height of the data to load.
        :type height: int
        :param positionX: Left boundary of the region to be drawn on.
        :type positionX: int
        :param positionY: Upper boundary of the region to be drawn on.
        :type positionY: int
        :param mode: Drawing mode, see Image Blending Modes _.
        :type mode: int
        '''
        pass


class ImageFFmpeg:
    ''' FFmpeg image source, used for image files and web based images. :arg file: Path to the image to load. :type file: str
    '''

    status: int = None
    ''' Image status. (readonly) :value: see FFmpeg Video and Image Status _.

    :type: int
    '''

    valid: bool = None
    ''' Tells if an image is available. (readonly)

    :type: bool
    '''

    image = None
    ''' Image data. (readonly)'''

    size: tuple = None
    ''' Image size. (readonly)

    :type: tuple
    '''

    scale: bool = None
    ''' Fast scale of image (near neighbour).

    :type: bool
    '''

    flip: bool = None
    ''' Flip image vertically.

    :type: bool
    '''

    filter = None
    ''' Pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''

    def refresh(self, buffer=None, format: str = "RGBA") -> int:
        ''' Refresh image, get its status and optionally copy the frame to an external buffer.

        :param buffer: An optional object that implements the buffer protocol. If specified, the image is copied to the buffer, which must be big enough or an exception is thrown.
        :type buffer: 
        :param format: An optional image format specifier for the image that will be copied to the buffer. Only valid values are "RGBA" or "BGRA"
        :type format: str
        :rtype: int
        :return: see FFmpeg Video and Image Status _.
        '''
        pass

    def reload(self, newname: str = None):
        ''' Reload image, i.e. reopen it.

        :param newname: Path to a new image. (optional)
        :type newname: str
        '''
        pass


class ImageMirror:
    ''' Image source from mirror. :arg scene: Scene in which the image has to be taken. :type scene: ~bge.types.KX_Scene :arg observer: Reference object for the mirror (the object from which the mirror has to be looked at, for example a camera). :type observer: ~bge.types.KX_GameObject :arg mirror: Object holding the mirror. :type mirror: ~bge.types.KX_GameObject :arg material: ID of the mirror's material to be used for mirroring. (optional) :type material: int :arg width: Off-screen render buffer width (optional). :type width: integer :arg height: Off-screen render buffer height (optional). :type height: integer :arg samples: Off-screen render buffer samples (optional). :type samples: integer :arg hdr: Off-screen image format (optional). :type hdr: One of :ref: these constants<render-hdr>
    '''

    alpha: bool = None
    ''' Use alpha in texture.

    :type: bool
    '''

    horizon: typing.List[float] = None
    ''' Horizon color.

    :type: typing.List[float]
    '''

    zenith: typing.List[float] = None
    ''' Zenith color.

    :type: typing.List[float]
    '''

    background: typing.List[float] = None
    ''' Deprecated use :py:meth: bge.texture.ImageMirror.horizon or :py:meth: bge.texture.ImageMirror.zenith instead.

    :type: typing.List[float]
    '''

    updateShadow: bool = None
    ''' Choose to force shadow buffer update if there is a gap beetween image rendered and shadows.

    :type: bool
    '''

    colorBindCode = None
    ''' Off-screen color texture bind code.'''

    capsize: list = None
    ''' Size of render area.

    :type: list
    '''

    clip: float = None
    ''' Clipping distance.

    :type: float
    '''

    filter = None
    ''' Pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''

    flip: bool = None
    ''' Flip image vertically.

    :type: bool
    '''

    image = None
    ''' Image data. (readonly)'''

    scale: bool = None
    ''' Fast scale of image (near neighbour).

    :type: bool
    '''

    size: tuple = None
    ''' Image size (readonly).

    :type: tuple
    '''

    valid: bool = None
    ''' Tells if an image is available. (readonly)

    :type: bool
    '''

    whole: bool = None
    ''' Use whole viewport to render.

    :type: bool
    '''

    def refresh(self, buffer=None, format: str = "RGBA"):
        ''' Refresh image - render and copy the image to an external buffer (optional) then invalidate its current content.

        :param buffer: An optional object that implements the buffer protocol. If specified, the image is rendered and copied to the buffer, which must be big enough or an exception is thrown.
        :type buffer: 
        :param format: An optional image format specifier for the image that will be copied to the buffer. Only valid values are "RGBA" or "BGRA"
        :type format: str
        '''
        pass


class ImageMix:
    ''' Image mixer used to mix multiple image sources together.
    '''

    filter = None
    ''' Pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''

    flip: bool = None
    ''' Flip image vertically.

    :type: bool
    '''

    image = None
    ''' Image data. (readonly)'''

    scale: bool = None
    ''' Fast scale of image (near neighbour).

    :type: bool
    '''

    size: tuple = None
    ''' Image size. (readonly)

    :type: tuple
    '''

    valid: bool = None
    ''' Tells if an image is available. (readonly)

    :type: bool
    '''

    def getSource(
            self, id: str
    ) -> typing.Union['VideoFFmpeg', 'ImageMirror', 'ImageViewport',
                      'ImageBuff', 'ImageMix', 'ImageRender', 'ImageFFmpeg']:
        ''' Get image source.

        :param id: Identifier of the source to get.
        :type id: str
        :rtype: typing.Union['VideoFFmpeg', 'ImageMirror', 'ImageViewport', 'ImageBuff', 'ImageMix', 'ImageRender', 'ImageFFmpeg']
        :return: Image source.
        '''
        pass

    def getWeight(self, id: str) -> int:
        ''' Get image source weight.

        :param id: Identifier of the source.
        :type id: str
        :rtype: int
        :return: Weight of the source.
        '''
        pass

    def refresh(self, buffer=None, format: str = "RGBA"):
        ''' Refresh image - calculate and copy the image to an external buffer (optional) then invalidate its current content.

        :param buffer: An optional object that implements the buffer protocol. If specified, the image is calculated and copied to the buffer, which must be big enough or an exception is thrown.
        :type buffer: 
        :param format: An optional image format specifier for the image that will be copied to the buffer. Only valid values are "RGBA" or "BGRA"
        :type format: str
        '''
        pass

    def setSource(self, id: str, image):
        ''' Set image source - all sources must have the same size.

        :param id: Identifier of the source to set.
        :type id: str
        :param image: 
        :type image: 
        '''
        pass

    def setWeight(self, id: str, weight: int):
        ''' Set image source weight - the sum of the weights should be 256 to get full color intensity in the output.

        :param id: Identifier of the source.
        :type id: str
        :param weight: Weight of the source.
        :type weight: int
        '''
        pass


class ImageRender:
    ''' Image source from a render of a non active camera. The render is done on a custom framebuffer object if fbo is specified, otherwise on the default framebuffer. :arg scene: Scene in which the image has to be taken. :type scene: ~bge.types.KX_Scene :arg camera: Camera from which the image has to be taken. :type camera: ~bge.types.KX_Camera :arg width: Off-screen render buffer width (optional). :type width: integer :arg height: Off-screen render buffer height (optional). :type height: integer :arg samples: Off-screen render buffer samples (optional). :type samples: integer :arg hdr: Off-screen image format (optional). :type hdr: One of :ref: these constants<render-hdr>
    '''

    alpha: bool = None
    ''' Use alpha in texture.

    :type: bool
    '''

    horizon: typing.List[float] = None
    ''' Horizon color.

    :type: typing.List[float]
    '''

    zenith: typing.List[float] = None
    ''' Zenith color.

    :type: typing.List[float]
    '''

    background: typing.List[float] = None
    ''' Background color. Deprecated use :py:meth: bge.texture.ImageRender.horizon or :py:meth: bge.texture.ImageRender.zenith instead.

    :type: typing.List[float]
    '''

    updateShadow: bool = None
    ''' Choose to force shadow buffer update if there is a gap beetween image rendered and shadows.

    :type: bool
    '''

    colorBindCode = None
    ''' Off-screen color texture bind code.'''

    capsize: list = None
    ''' Size of render area.

    :type: list
    '''

    filter = None
    ''' Pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''

    flip: bool = None
    ''' Flip image vertically.

    :type: bool
    '''

    image = None
    ''' Image data. (readonly)'''

    scale: bool = None
    ''' Fast scale of image (near neighbour).

    :type: bool
    '''

    size: tuple = None
    ''' Image size. (readonly)

    :type: tuple
    '''

    valid: bool = None
    ''' Tells if an image is available. (readonly)

    :type: bool
    '''

    whole: bool = None
    ''' Use whole viewport to render.

    :type: bool
    '''

    depth: bool = None
    ''' Use depth component of render as array of float - not suitable for texture source, should only be used with bge.texture.imageToArray(mode='F').

    :type: bool
    '''

    zbuff: bool = None
    ''' Use depth component of render as grayscale color - suitable for texture source.

    :type: bool
    '''

    def render(self) -> bool:
        ''' Render the scene but do not extract the pixels yet. The function returns as soon as the render commands have been send to the GPU. The render will proceed asynchronously in the GPU while the host can perform other tasks. To complete the render, you can either call :func: refresh directly of refresh the texture of which this object is the source. This method is useful to implement asynchronous render for optimal performance: call render() on frame n and refresh() on frame n+1 to give as much as time as possible to the GPU to render the frame while the game engine can perform other tasks.

        :rtype: bool
        :return: True if the render was initiated, False if the render cannot be performed (e.g. the camera is active)
        '''
        pass

    def refresh(self):
        ''' 

        '''
        pass

    def refresh(self, buffer, format: str = "RGBA") -> bool:
        ''' Refresh video - render and optionally copy the image to an external buffer then invalidate its current content. The render may have been started earlier with the :func: render method, in which case this function simply waits for the render operations to complete. When called without argument, the pixels are not extracted but the render is guaranteed to be completed when the function returns. This only makes sense with offscreen render on texture target (see :func: ~bge.render.offScreenCreate ).

        :param buffer: An object that implements the buffer protocol. If specified, the image is copied to the buffer, which must be big enough or an exception is thrown. The transfer to the buffer is optimal if no processing of the image is needed. This is the case if flip=False, alpha=True, scale=False, whole=True, depth=False, zbuff=False and no filter is set.
        :type buffer: 
        :param format: An optional image format specifier for the image that will be copied to the buffer. Only valid values are "RGBA" or "BGRA"
        :type format: str
        :rtype: bool
        :return: True if the render is complete, False if the render cannot be performed (e.g. the camera is active)
        '''
        pass


class ImageViewport:
    ''' Image source from viewport rendered by the active camera. To render from a non active camera see ImageRender .
    '''

    alpha: bool = None
    ''' Use alpha in texture.

    :type: bool
    '''

    capsize: list = None
    ''' Size of viewport area being captured.

    :type: list
    '''

    filter = None
    ''' Pixel filter. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''

    flip: bool = None
    ''' Flip image vertically.

    :type: bool
    '''

    image = None
    ''' Image data. (readonly)'''

    position: list = None
    ''' Upper left corner of the captured area.

    :type: list
    '''

    scale: bool = None
    ''' Fast scale of image (near neighbour).

    :type: bool
    '''

    size: tuple = None
    ''' Image size. (readonly)

    :type: tuple
    '''

    valid: bool = None
    ''' Tells if an image is available. (readonly)

    :type: bool
    '''

    whole: bool = None
    ''' Use whole viewport to capture.

    :type: bool
    '''

    depth: bool = None
    ''' Use depth component of viewport as array of float - not suitable for texture source, should only be used with bge.texture.imageToArray(mode='F') .

    :type: bool
    '''

    zbuff: bool = None
    ''' Use depth component of viewport as grayscale color - suitable for texture source.

    :type: bool
    '''

    def refresh(self, buffer=None, format: str = "RGBA"):
        ''' Refresh video - copy the viewport to an external buffer (optional) then invalidate its current content.

        :param buffer: An optional object that implements the buffer protocol. If specified, the image is copied to the buffer, which must be big enough or an exception is thrown. The transfer to the buffer is optimal if no processing of the image is needed. This is the case if flip=False, alpha=True, scale=False, whole=True, depth=False, zbuff=False and no filter is set.
        :type buffer: 
        :param format: An optional image format specifier for the image that will be copied to the buffer. Only valid values are "RGBA" or "BGRA"
        :type format: str
        '''
        pass


class Texture:
    ''' Class that creates the Texture object that loads the dynamic texture on the GPU. :arg gameObj: Game object to be created a video texture on. :type gameObj: ~bge.types.KX_GameObject :arg materialID: Material ID default, 0 is the first material. (optional) :type materialID: int :arg textureID: Texture index in case of multi-texture channel, 0 = first channel by default. In case of UV texture, this parameter should always be 0. (optional) :type textureID: int :arg textureObj: Reference to another Texture object with shared bindId which he user might want to reuse the texture. If this argument is used, you should not create any source on this texture and there is no need to refresh it either: the other Texture object will provide the texture for both materials/textures.(optional) :type textureObj: Texture
    '''

    bindId: int = None
    ''' OpenGL Bind Name. (readonly)

    :type: int
    '''

    mipmap: bool = None
    ''' Mipmap texture.

    :type: bool
    '''

    source = None
    ''' Source of texture. * VideoFFmpeg * VideoDeckLink * ImageFFmpeg * ImageBuff * ImageMirror * ImageMix * ImageRender * ImageViewport'''

    def close(self):
        ''' Close dynamic texture and restore original.

        '''
        pass

    def refresh(self, refresh_source: bool, timestamp: float = -1.0):
        ''' Refresh texture from source.

        :param refresh_source: Whether to also refresh the image source of the texture.
        :type refresh_source: bool
        :param timestamp: timestamp (in seconds from the start of the movie) of the frame to be loaded; this can be used for video-sound synchonization by passing :attr: ~bge.types.KX_SoundActuator.time to it. (optional)
        :type timestamp: float
        '''
        pass


class VideoDeckLink:
    ''' Image source from an external video stream captured with a DeckLink video card from Black Magic Design. Before this source can be used, a DeckLink hardware device must be installed, it can be a PCIe card or a USB device, and the 'Desktop Video' software package (version 10.4 or above must be installed) on the host as described in the DeckLink documentation. If in addition you have a recent nVideo Quadro card, you can benefit from the 'GPUDirect' technology to push the captured video frame very efficiently to the GPU. For this you need to install the 'DeckLink SDK' version 10.4 or above and copy the 'dvp.dll' runtime library to Blender's installation directory or to any other place where Blender can load a DLL from. :arg format: string describing the video format to be captured. :type format: str :arg capture: Card number from which the input video must be captured. :type capture: int The format argument must be written as <displayMode>/<pixelFormat>[/3D][:<cacheSize>] where <displayMode> describes the frame size and rate and <pixelFormat> the encoding of the pixels. The optional /3D suffix is to be used if the video stream is stereo with a left and right eye feed. The optional :<cacheSize> suffix determines the number of the video frames kept in cache, by default 8. Some DeckLink cards won't work below a certain cache size. The default value 8 should be sufficient for all cards. You may try to reduce the cache size to reduce the memory footprint. For example the The 4K Extreme is known to work with 3 frames only, the Extreme 2 needs 4 frames and the Intensity Shuttle needs 6 frames, etc. Reducing the cache size may be useful when Decklink is used in conjunction with GPUDirect: all frames must be locked in memory in that case and that puts a lot of pressure on memory. If you reduce the cache size too much, you'll get no error but no video feed either. The valid <displayMode> values are copied from the BMDDisplayMode enum in the DeckLink API without the 'bmdMode' prefix. In case a mode that is not in this list is added in a later version of the SDK, it is also possible to specify the 4 letters of the internal code for that mode. You will find the internal code in the DeckLinkAPIModes.h file that is part of the SDK. Here is for reference the full list of supported display modes with their equivalent internal code: Internal Codes - NTSC 'ntsc' - NTSC2398 'nt23' - PAL 'pal ' - NTSCp 'ntsp' - PALp 'palp' HD 1080 Modes - HD1080p2398 '23ps' - HD1080p24 '24ps' - HD1080p25 'Hp25' - HD1080p2997 'Hp29' - HD1080p30 'Hp30' - HD1080i50 'Hi50' - HD1080i5994 'Hi59' - HD1080i6000 'Hi60' - HD1080p50 'Hp50' - HD1080p5994 'Hp59' - HD1080p6000 'Hp60' HD 720 Modes - HD720p50 'hp50' - HD720p5994 'hp59' - HD720p60 'hp60' 2k Modes - 2k2398 '2k23' - 2k24 '2k24' - 2k25 '2k25' 4k Modes - 4K2160p2398 '4k23' - 4K2160p24 '4k24' - 4K2160p25 '4k25' - 4K2160p2997 '4k29' - 4K2160p30 '4k30' - 4K2160p50 '4k50' - 4K2160p5994 '4k59' - 4K2160p60 '4k60' Most of names are self explanatory. If necessary refer to the DeckLink API documentation for more information. Similarly, <pixelFormat> is copied from the BMDPixelFormat enum. Here is for reference the full list of supported pixel format and their equivalent internal code: Pixel Formats - 8BitYUV '2vuy' - 10BitYUV 'v210' - 8BitARGB * no equivalent code * - 8BitBGRA 'BGRA' - 10BitRGB 'r210' - 12BitRGB 'R12B' - 12BitRGBLE 'R12L' - 10BitRGBXLE 'R10l' - 10BitRGBX 'R10b' Refer to the DeckLink SDK documentation for a full description of these pixel format. It is important to understand them as the decoding of the pixels is NOT done in VideoTexture for performance reason. Instead a specific shader must be used to decode the pixel in the GPU. Only the '8BitARGB', '8BitBGRA' and '10BitRGBXLE' pixel formats are mapped directly to OpenGL RGB float textures. The '8BitYUV' and '10BitYUV' pixel formats are mapped to openGL RGB float texture but require a shader to decode. The other pixel formats are sent as a GL_RED_INTEGER texture (i.e. a texture with only the red channel coded as an unsigned 32 bit integer) and are not recommended for use. Example: HD1080p24/10BitYUV/3D:4 is equivalent to 24ps/v210/3D:4 and represents a full HD stereo feed at 24 frame per second and 4 frames cache size. Although video format auto detection is possible with certain DeckLink devices, the corresponding API is NOT implemented in the BGE. Therefore it is important to specify the format string that matches exactly the video feed. If the format is wrong, no frame will be captured. It should be noted that the pixel format that you need to specify is not necessarily the actual format in the video feed. For example, the 4K Extreme card delivers 8bit RGBs pixels in the '10BitRGBXLE' format. Use the 'Media Express' application included in 'Desktop Video' to discover which pixel format works for a particular video stream.
    '''

    status: int = None
    ''' Status of the capture: 1=ready to use, 2=capturing, 3=stopped

    :type: int
    '''

    framerate: float = None
    ''' Capture frame rate as computed from the video format.

    :type: float
    '''

    valid: bool = None
    ''' Tells if the image attribute can be used to retrieve the image. Always False in this implementation (the image is not available at python level)

    :type: bool
    '''

    image = None
    ''' The image data. Always None in this implementation.'''

    size: int = None
    ''' The size of the frame in pixel. Stereo frames have double the height of the video frame, i.e. 3D is delivered to the GPU as a single image in top-bottom order, left eye on top.

    :type: int
    '''

    scale: bool = None
    ''' Not used in this object.

    :type: bool
    '''

    flip: bool = None
    ''' Not used in this object.

    :type: bool
    '''

    filter = None
    ''' Not used in this object.'''

    def play(self) -> bool:
        ''' Kick-off the capture after creation of the object.

        :rtype: bool
        :return: True if the capture could be started, False otherwise.
        '''
        pass

    def pause(self) -> bool:
        ''' Temporary stops the capture. Use play() to restart it.

        :rtype: bool
        :return: True if the capture could be paused, False otherwise.
        '''
        pass

    def stop(self) -> bool:
        ''' Stops the capture.

        :rtype: bool
        :return: True if the capture could be stopped, False otherwise.
        '''
        pass


class VideoFFmpeg:
    ''' FFmpeg video source, used for video files, video captures, or video streams. :arg file: Path to the video to load; if capture >= 0 on Windows, this parameter will not be used. :type file: str :arg capture: Capture device number; if >= 0, the corresponding webcam will be used. (optional) :type capture: int :arg rate: Capture rate. (optional, used only if capture >= 0) :type rate: float :arg width: Capture width. (optional, used only if capture >= 0) :type width: int :arg height: Capture height. (optional, used only if capture >= 0) :type height: int
    '''

    status: int = None
    ''' Video status. (readonly) :value: see FFmpeg Video and Image Status _.

    :type: int
    '''

    range: list = None
    ''' The start and stop time of the video playback, expressed in seconds from beginning. By default the entire video.

    :type: list
    '''

    repeat: int = None
    ''' Number of times to replay the video, -1 for infinite repeat.

    :type: int
    '''

    framerate: float = None
    ''' Relative frame rate, <1.0 for slow, >1.0 for fast.

    :type: float
    '''

    valid: bool = None
    ''' Tells if an image is available. (readonly)

    :type: bool
    '''

    image = None
    ''' Image data. (readonly)'''

    size: tuple = None
    ''' Image size. (readonly)

    :type: tuple
    '''

    scale: bool = None
    ''' Set to True to activate fast nearest neighbor scaling algorithm. Texture width and height must be a power of 2. If the video picture size is not a power of 2, rescaling is required. By default bge.texture uses the precise but slow gluScaleImage() function. Best is to rescale the video offline so that no scaling is necessary at runtime!

    :type: bool
    '''

    flip: bool = None
    ''' If True the imaged will be flipped vertically. FFmpeg always delivers the image upside down, so this attribute is set to True by default.

    :type: bool
    '''

    filter = None
    ''' An additional filter that is applied on the video before sending it to the GPU. * FilterBGR24 * FilterBlueScreen * FilterColor * FilterGray * FilterLevel * FilterNormal * FilterRGB24 * FilterRGBA32'''

    preseek: int = None
    ''' Number of frames of preseek.

    :type: int
    '''

    deinterlace: bool = None
    ''' Deinterlace image.

    :type: bool
    '''

    def play(self) -> bool:
        ''' Play (restart) video.

        :rtype: bool
        :return: Whether the video was ready or stopped.
        '''
        pass

    def pause(self) -> bool:
        ''' Pause video.

        :rtype: bool
        :return: Whether the video was playing.
        '''
        pass

    def stop(self) -> bool:
        ''' Stop video (play will replay it from start).

        :rtype: bool
        :return: Whether the video was playing.
        '''
        pass

    def refresh(self,
                buffer=None,
                format: str = "RGBA",
                timestamp: float = -1.0) -> int:
        ''' Refresh video - get its status and optionally copy the frame to an external buffer.

        :param buffer: An optional object that implements the buffer protocol. If specified, the image is copied to the buffer, which must be big enough or an exception is thrown.
        :type buffer: 
        :param format: An optional image format specifier for the image that will be copied to the buffer. Only valid values are "RGBA" or "BGRA"
        :type format: str
        :param timestamp: An optional timestamp (in seconds from the start of the movie) of the frame to be copied to the buffer.
        :type timestamp: float
        :rtype: int
        :return: see FFmpeg Video and Image Status _.
        '''
        pass


def getLastError() -> str:
    ''' Last error that occurred in a bge.texture function.

    :return: The description of the last error occurred in a bge.texture function.
    '''

    pass


def imageToArray(image, mode: str):
    ''' Returns a ~bgl.Buffer corresponding to the current image stored in a texture source object.

    :param mode: Optional argument representing the pixel format. - You can use the characters R, G, B for the 3 color channels, A for the alpha channel, 0 to force a fixed 0 color channel and 1 to force a fixed 255 color channel. Examples: - "BGR" will return 3 bytes per pixel with the Blue, Green and Red channels in that order. - "RGB1" will return 4 bytes per pixel with the Red, Green, Blue channels in that order and the alpha channel forced to 255. - A special mode "F" allows to return the image as an array of float. This mode should only be used to retrieve the depth buffer of the class: ImageViewport and ImageRender objects. The default mode is "RGBA".
    :type mode: str
    :return: An object representing the image as one dimensional array of bytes of size (pixel_size*width*height), line by line starting from the bottom of the image. The pixel size and format is determined by the mode parameter. For mode 'F', the array is a one dimensional array of float of size (width*height).
    '''

    pass


def materialID(object, name: str) -> int:
    ''' Returns a numeric value that can be used in Texture to create a dynamic texture. The value corresponds to an internal material number that uses the texture identified by name. name is a string representing a texture name with IM prefix if you want to identify the texture directly. This method works for basic tex face and for material, provided the material has a texture channel using that particular texture in first position of the texture stack. name can also have MA prefix if you want to identify the texture by material. In that case the material must have a texture channel in first position. If the object has no material that matches name, it generates a runtime error. Use try/except to catch the exception. Ex: bge.texture.materialID(obj, 'IMvideo.png')

    :param object: The game object that uses the texture you want to make dynamic.
    :param name: Name of the texture/material you want to make dynamic.
    :type name: str
    :return: The internal material number.
    '''

    pass


def setLogFile(filename: str) -> int:
    ''' Sets the name of a text file in which runtime error messages will be written, in addition to the printing of the messages on the Python console. Only the runtime errors specific to the VideoTexture module are written in that file, ordinary runtime time errors are not written.

    :param filename: Name of the error log file.
    :type filename: str
    :return: -1 if the parameter name is invalid (not of type string), else 0.
    '''

    pass


IMB_BLEND_ADD = None

IMB_BLEND_ADD_ALPHA = None

IMB_BLEND_COLOR = None

IMB_BLEND_COLORBURN = None

IMB_BLEND_COLORDODGE = None

IMB_BLEND_COPY = None

IMB_BLEND_COPY_ALPHA = None

IMB_BLEND_COPY_RGB = None

IMB_BLEND_DARKEN = None

IMB_BLEND_DIFFERENCE = None

IMB_BLEND_ERASE_ALPHA = None

IMB_BLEND_EXCLUSION = None

IMB_BLEND_HARDLIGHT = None

IMB_BLEND_HUE = None

IMB_BLEND_LIGHTEN = None

IMB_BLEND_LINEARBURN = None

IMB_BLEND_LINEARLIGHT = None

IMB_BLEND_LUMINOSITY = None

IMB_BLEND_MIX = None

IMB_BLEND_MUL = None

IMB_BLEND_OVERLAY = None

IMB_BLEND_PINLIGHT = None

IMB_BLEND_SATURATION = None

IMB_BLEND_SCREEN = None

IMB_BLEND_SOFTLIGHT = None

IMB_BLEND_SUB = None

IMB_BLEND_VIVIDLIGHT = None

SOURCE_EMPTY = None

SOURCE_ERROR = None

SOURCE_PLAYING = None

SOURCE_READY = None

SOURCE_STOPPED = None
