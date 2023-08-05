# -*- coding: utf-8 -*-

from .pypack.folk.controlserver import Controlserver, EquipmentType, EquipmentTypeError

class UserApi:

    def __init__(self):
        self._control_server = Controlserver()
        if self._control_server == None:
            exit(0)

#=============================================System Config======================================================================#

    def equipment_create(self, equipment_type):
        '''
        创建无人机设备
        
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :return:
                  | 飞机id号:创建成功
                  | -1:创建失败
        ---------------------------------
        Create an equipment

        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane or EquipmentType.LedPlane
        :return:
                  | plane_id: success
                  | -1: Failed
        '''
        return self._control_server.equipment_create(equipment_type)

    def equipment_remove(self, equipment_type, id = 0):
        '''
        删除无人机设备

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Remove an equipment

        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane or EquipmentType.LedPlane
        :param id: plane id, default is 0 
        '''
        return self._control_server.equipment_remove(equipment_type, id)

    def equipment_show(self):
        '''
        打印输出所有无人机设备的类型和id
        ---------------------------------
        Show every equipment's type and id
        '''
        return self._control_server.equipment_show()

#=============================================Plane Config=======================================================================#

    def plane_connect(self, equipment_type, id = 0):
        '''
        连接到无人机设备

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Connect to equipment
        
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane or EquipmentType.LedPlane
        :param id: plane id, 0 as default if no input
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.plane_connect(equipment_type, id)
    
    def plane_disconnect(self, equipment_type, id = 0):
        '''
        断开与无人机设备的连接
        
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Disconnect from the equipment
        
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane or EquipmentType.LedPlane
        :param id: plane id, 0 as default if no input
        '''
        return self._control_server.plane_disconnect(equipment_type, id)
    
    def plane_get_connect_state(self, equipment_type, id = 0):
        '''
        获取飞机连接状态

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:已连接
                  | False:未连接
        ---------------------------------
        Get equipment's connection status
        
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane or EquipmentType.LedPlane
        :param id: plane id, 0 as default if no input
        :return:
                  | True:connected
                  | False:disconnected
        '''
        return self._control_server.plane_get_connect_state(equipment_type, id)

    def plane_sys_reset_wifi(self, ssid, password, equipment_type, id = 0):
        '''
        重置wifi名称与wifi密码

        :param ssid: wifi名称
        :param password: wifi密码
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Reset equipment wifi's ssid and password
        
        :param ssid: wifi's name
        :param password: wifi's password
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane or EquipmentType.LedPlane
        :param id: plane id, 0 as default if no input
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.plane_sys_reset_wifi(ssid, password, equipment_type, id)

    def plane_sys_update_firmware(self, firmware_path, equipment_type, id = 0):
        '''
        更新飞机固件

        :param firmware_path: 固件路径
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败

        .. note::
          升级飞机固件时，最好连接飞机wifi，不要连接摄像头wifi，以保证升级成功率。
        ---------------------------------
        Update equipment's firmware
        
        :param firmware_path: path to firmware
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane or EquipmentType.LedPlane
        :param id: plane id, 0 as default if no input
        :return:
                  | True:success
                  | False:failed
                  
        .. note::
          It's better to use plane's wifi rather than camera's for firmware update.
        '''
        return self._control_server.plane_sys_update_firmware(firmware_path, equipment_type, id)

    def plane_sys_get_firmware_update_rate(self, equipment_type, id = 0):
        '''
        获取固件上传进度

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return: 飞机固件上传进度百分比:正常传输

        .. warning::
          用户接口都是串行处理，固件上传传输过程中，如果需要获取进度，则需要在线程中调用该函数进行获取
        ---------------------------------
        Get firmware uploading progress

        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane or EquipmentType.LedPlane
        :param id: plane id, 0 as default if no input
        :return: uploading progress percent: normal uploading
        
        .. warning::
          Only can be called in other threads while uploading
        '''
        return self._control_server.plane_sys_get_firmware_update_rate(equipment_type,id)
        
#==============================================Camera Control====================================================================#

    def camera_take_photo(self):
        '''
        拍照，照片存储在摄像头的sd卡上
        
        :return:
                  | True:成功 
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型设置为EquipmentType.CameraPlane
        ---------------------------------
        Take photo, and the photo will be saved in camera's sd card
        
        :return:
                  | True:success
                  | False:failed
             
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.camera_take_photo()

    def camera_take_video_on(self):
        '''
        开始录像，视频存储在摄像头的sd卡上
        
        :return:
                  | True:成功 
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Start to record a video, and the video will be saved in camera's sd card

        :return:
                  | True:success
                  | False:failed

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.camera_take_video(1)

    def camera_take_video_off(self):
        '''
        停止录像，视频存储在摄像头的sd卡上
        
        :return:
                  | True:成功
                  | False:失败

        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Stop recording and the video will be saved in camera's sd card
        
        :return:
                  | True:success
                  | False:failed

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.camera_take_video(0)
        
    def camera_get_take_video_status(self):
        '''
        获取SD卡录像状态
        
        :return:
                  | 0:未开始录像
                  | 1:录像中
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Get video recording status
        
        :return:
                  | 0:the video is not recorded
                  | 1:the video is recording
        
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.camera_get_take_video_status()

#=============================================Stream Control=====================================================================#

    def stream_on(self):
        '''
        开始获取视频流
        
        :return:
                  | True:成功
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Turn on video streaming
        
        :return:
                  | True:success
                  | False:failed

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_on()
            
    def stream_off(self):
        '''
        停止获取视频流
        
        :return:
                  | True:成功
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Turn off video streaming
        
        :return:
                  | True:success
                  | False:failed
        
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_off()
        
    def stream_show(self):
        '''
        实时显示视频流
        
        :return:
                  | True:成功
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Show video streaming
        
        :return:
                  | True:success
                  | False:failed

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_show()

    def stream_stop_show(self):
        '''
        停止显示视频流
        
        :return:
                  | True:成功 
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Stop showing video streaming
        
        :return:
                  | True:success
                  | False:failed
        
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_stop_show()

    def stream_flip(self, flip):
        '''
        水平反转视频流

        :param flip: 是否反转(True或False)
        :return:
                  | True:成功
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Horizontal flip the video streaming
        
        :param flip: whether flip the video streaming(True or False)
        :return:
                  | True:success
                  | False:failed
        
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_flip(flip)
        
    def stream_set_path(self, path):
        '''
        设置照片和视频的存储路径
        
        :return:
                  | True:成功 
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Set a path to save photo and video
        
        :return:
                  | True:success
                  | False:failed
        
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_set_path(path)
        
    def stream_take_photo(self):
        '''
        拍一张照片，存储在stream_set_path设置的路径上
        
        :return:
                  | True:成功 
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        take a photo and save it in the path set by stream_set_path
        
        :return:
                  | True:success
                  | False:failed
                  
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_take_photo()
        
    def stream_take_video_on(self):
        '''
        开始录像，视频存储在stream_set_path设置的路径上
        
        :return:
                  | True:成功 
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Start recording a video and save it in the path set by stream_set_path
        
        :return:
                  | True:success
                  | False:failed
                  
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_take_video_on()
        
    def stream_take_video_off(self):
        '''
        停止录像，视频存储在stream_set_path设置的路径上
        
        :return:
                  | True:成功 
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Stop recording video and save it in the path set by stream_set_path
        
        :return:
                  | True:success
                  | False:failed
                  
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_take_video_off()
        
    def stream_get_status(self):
        '''
        获取视频流运行状态

        :return:
                  | 0:未开启
                  | 1:已开启

        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Get video streaming status

        :return:
                  | 0:off
                  | 1:on

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_get_status()
        
    def stream_get_stream_show_status(self):
        '''
        获取视频流显示状态
        
        :return:
                  | 0:未显示
                  | 1:显示中
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Get video streaming showing status
        
        :return:
                  | 0:off
                  | 1:on
                  
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_get_stream_show_status()
        
    def stream_get_take_video_status(self):
        '''
        获取录像状态
        
        :return:
                  | 0:未开始录像
                  | 1:录像中
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Get video recording status
        
        :return:
                  | 0:off
                  | 1:on

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment               
        '''
        return self._control_server.stream_get_take_video_status()
        
    def stream_get_frame(self):
        '''
        返回一帧图像
        
        :return:
                  | 一帧图像:获取成功
                  | None:获取失败
        
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Get the current frame
        
        :return: 
                  | the current frame:success
                  | None:failed

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_get_frame()
        
    def stream_get_height(self):
        '''
        获取视频分辨率的高度信息
        
        :return: 
                  | 视频高度（像素）:获取成功
                  | -1:获取失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Get video resolution's height
        
        :return:
                  | height(pixel):success
                  | -1:failed
                  
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_get_height()
        
    def stream_get_width(self):
        '''
        获取视频分辨率的宽度信息
        
        :return: 
                  | 视频宽度（像素）:获取成功
                  | -1:获取失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Get the video resolution's width
        
        :return:
                  | width(pixel):success
                  | -1:failed
                  
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_get_width()

    def stream_get_fps(self):
        '''
        获取视频帧率
        
        :return: 
                  | 视频帧率（帧/秒）:获取成功
                  | -1:获取失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        get the video frame rate
        
        :return:
                  | fps:success
                  | -1:failed
                  
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_get_fps()
        
    def stream_draw_rectangle(self, rectangle_id, start_x, start_y, end_x, end_y, r, g, b, thickness):
        '''
        在视频流上画框
        
        :param rectangle_id: 边框的编号
        :param start_x: 画框的左上角x坐标
        :param start_y: 画框的左上角y坐标
        :param end_x: 画框右下角x坐标
        :param end_y: 画框的右下角y坐标
        :param r: 设置画框红色色值(0-255)
        :param g: 设置画框绿色色值(0-255)
        :param b: 设置画框蓝色色值(0-255)
        :param thickness: 画框厚度(0-20)
        :return:
                  | True:成功 
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Draw a box on every frame of video streaming

        :param rectangle_id: box's id
        :param start_x: the x-coordinate of the box's top left corner
        :param start_y: the y-coordinate of the box's top left corner
        :param end_x: the x-coordinate of the box's lower right corner
        :param end_y: the y-coordinate of the box's lower right corner
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :param thickness: box line's thickness(0-20)
        :return:
                  | True:success
                  | False:failed
                 
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_draw_rectangle(rectangle_id, start_x, start_y, end_x, end_y, r, g, b, thickness)

    def stream_draw_rectangle_by_mouse(self, rectangle_id, r, g, b, thickness, ret = 0):
        '''
        在视频流上使用鼠标画框
        
        :param rectangle_id: 画框的编号
        :param r: 设置画框红色色值(0-255)
        :param g: 设置画框绿色色值(0-255)
        :param b: 设置画框蓝色色值(0-255)
        :param thickness: 画框厚度(0-20)
        :param ret: 是否返回坐标，1为返回，0为不返回。当需要返回坐标时该函数会阻塞。
        :return:
                  | [左上角x坐标, 左上角y坐标, 右下角x坐标, 右下角y坐标]:ret为1时返回画框的坐标
                  | []:ret为0或者参数错误时返回[]

        .. warning::
          | 1.需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
          | 2.当ret为0时，连续调用该函数只会以最后一次调用填入的参数为准。
        ---------------------------------
        Draw a box by mouse on every frame of video streaming
        
        :param rectangle_id: box's id
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :param thickness: box line's thickness(0-20)
        :param ret: whether to return the box's coordinate: 1 for yes and 0 for no. If ret is 1, the box's coordinate will be returned and this function will block
        :return:
                  | [x-coordinate of top left, y-coordinate of top left, x-coordinate of lower right, y-coordinate of lower right]:if ret is set as 1, the box's coordinate will be return.
                  | None:if ret is set as 0, None will be return
                  
        .. warning::
          | 1.A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
          | 2.while ret is set as 0, repeat callings of this function can only make the last one work.
        '''
        return self._control_server.stream_draw_rectangle_by_mouse(rectangle_id, r, g, b, thickness, ret)
        
    def stream_clear_rectangle(self, rectangle_id = None):
        '''
        删除视频流上的画框
        
        :param rectangle_id: 画框的编号,当rectangle_id为None时清除所有画框
        :return:
                  | True:成功
                  | False:失败

        .. warning::
          | 1.需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
          | 2.画完一个画框后，画框会在下一帧的图像上开始显示。如果调用stream_draw_rectangle或者stream_draw_rectangle_by_mouse后立即调用stream_clear_rectangle，那么画框很可能没显示出来。
        ---------------------------------
        Delete boxes on the frame of video streaming
        
        :param rectangle_id: box's id. When rectangle_id is None(default), delet all boxes.
        :return:
                  | True:success
                  | False:failed

        .. warning::
          | 1.A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
          | 2.If this fucntion is called immediately after stream_draw_rectangle or stream_draw_rectangle_by_mouse，the box will not show out.
        '''
        return self._control_server.stream_clear_rectangle(rectangle_id)
        
    def stream_draw_text(self, text_id, string, x, y, size, r, g, b):
        '''
        在视频流上显示文字(目前只能正常显示英文)
        
        :param text_id: 文字的编号
        :param string: 显示的内容
        :param x: 文字放置的坐标x
        :param y: 文字放置的坐标y
        :param size: 字体大小（0-5）
        :param r: 设置边框红色色值(0-255)
        :param g: 设置边框绿色色值(0-255)
        :param b: 设置边框蓝色色值(0-255)
        :return:
                  | True:成功
                  | False:失败
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Draw a text on every frame of video streaming
        
        :param text_id: text's id
        :param string: the text to draw
        :param x: x-coordinate
        :param y: y-coordinate
        :param size: font size
        :param r: red channel(0-255)
        :param g: green channel(0-255)
        :param b: blue channel(0-255)
        :return:
                  | True:success
                  | False:failed

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.stream_draw_text(text_id, string, x, y, size, r, g, b)
        
    def stream_clear_text(self, text_id = None):
        '''
        删除在视频流上显示的文字
        
        :param text_id: 文字的编号, 当text_id为None时清除所有文字
        :return:
                  | True:成功
                  | False:失败
                  
        .. warning::
          | 1.需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
          | 2.调用显示文字后，文字会在下一帧的图像上开始显示。如果调用stream_draw_text后立即调用stream_clear_text，那么文字很可能没显示出来。
        ---------------------------------
        Delete texts on the frame of video streaming
        
        :param text_id: text's id. When text_id is None, clear all texts.
        :return:
                  | True:success
                  | False:failed
            
        .. warning::
          | 1.A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
          | 2.the text will not show in the stream after calling stream_draw_text and then calling this function immediately.
        '''
        return self._control_server.stream_clear_text(text_id)
    
#=============================================AI Control=========================================================================#

    def ai_target_detect(self, frame = None, width = -1, height = -1):
        '''
        目标识别,可识别: aeroplane、bicycle、bird、boat、bottle、bus、car、cat、chair、cow、diningtable、dog、horse、motorbike、person、pottedplant、sheep、sofa、train、tvmonitor
        
        :param frame: 需要识别的图像，如果frame为None，并且视频流已经启动，则自动获取最新的一帧填入
        :param width: 图像的宽度，如果frame为None,width可不填
        :param height: 图像的高度，如果frame为None,height可不填
        :return:
                  | []:未识别到目标 
                  | [['xx物体', 可信度, 左上角x坐标, 左上角y坐标, 右下角x坐标, 右下角y坐标], [...], ...]:识别到的目标
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Detect the target. Target could be aeroplane, bicycle, bird, boat, bottle, bus, car, cat, chair, cow, diningtable, dog, horse, motorbike, person, pottedplant, sheep, sofa, train, tvmonitor
        
        :param frame: the frame used for target detection. When frame is None and the video streaming is on, the current frame will be set
        :param width: frame's width, when frame is None, it doesn't need to set
        :param height: frame's height, when frame is None, it doesn't need to set
        :return:
                  | []:failed target detection
                  | [[target name, confidence, x-coordinate of top left, y-coordinate of top left, x-coordinate of lower right, y-coordinate of lower right], [...], ...]:target is detected

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.ai_target_detect(frame, width, height)

    def ai_gesture_detect(self, frame = None, width = -1, height = -1):
        '''
        手势识别，可识别 hand和fist

        :param frame: 需要识别的图像，如果frame为None，并且视频流已经启动，则自动获取最新的一帧填入
        :param width: 图像的高度，如果frame为None,width可不填
        :param height: 图像的宽度，如果frame为None,height可不填
        :return:
                  | []:未识别到目标
                  | [['xx手势', 可信度, 左上角x坐标, 左上角y坐标, 右下角x坐标, 右下角y坐标], [...], ...]:识别到的目标

        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Detect gestures. Gestures could be hand and fist
        
        :param frame: the frame used for target detection. When frame is None and the video streaming is on, the current frame will be set
        :param width: frame's width, when frame is None, it doesn't need to set
        :param height: frame's height, when frame is None, it doesn't need to set
        :return:
                  | []:failed gesture detection
                  | [[gesture, confidence, x-coordinate of top left, y-coordinate of top left, x-coordinate of lower right, y-coordinate of lower right], [...], ...]:gesture is detected

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.ai_gesture_detect(frame, width, height)

    def ai_tracker_on(self, start_x, start_y, end_x, end_y, rectangle_id = None):
        '''
        开始跟踪画框框出的目标
        
        :param start_x: 画框的左上角x坐标
        :param start_y: 画框的左上角y坐标
        :param end_x: 画框的右下角x坐标
        :param end_y: 画框的右下角y坐标
        :param rectangle_id: 画框id号,当该参数被填入时,之前的四个坐标会被忽略,同时会自动更新画框的位置
        :return:
                  | True:成功
                  | False:失败
                  
        .. warning::
               
          | 1.需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
          | 2.跟踪画框的大小能不小于50x50
        ---------------------------------
        Start tracking the target appointed by the box

        :param start_x: the x-coordinate of the box's top left corner
        :param start_y: the y-coordinate of the box's top left corner
        :param end_x: the x-coordinate of the box's lower right corner
        :param end_y: the y-coordinate of the box's lower right corner
        :param rectangle_id: box's thickness(0-20)
        :return:
                  | True:success
                  | False:failed
                  
        .. warning::
          | 1.A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
          | 2.The minimum size of the box is 50x50
        '''
        return self._control_server.ai_tracker_on(start_x, start_y, end_x, end_y, rectangle_id)
        
    def ai_tracker_off(self):
        '''
        停止目标跟踪
        
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Stop tracking
        
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.ai_tracker_off()

    def ai_tracker_get_target(self):
        '''
        获取跟踪目标的坐标

        :return:
                  | []:跟踪目标丢失
                  | [左上角x坐标, 左上角y坐标, 右下角x坐标, 右下角y坐标]:获取到目标
                  
        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Get the tracking target's coordinates
        
        :return:
                  | []:target is lose
                  | [x-coordinate of top left, y-coordinate of top left, x-coordinate of lower right, y-coordinate of lower right]:target coordinate is get
                  
        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.ai_tracker_get_target()

    def ai_qrcode_detect(self, frame = None, width = -1, height = -1):
        '''
        二维码识别，可识别Folk定制的二维码

        :param frame: 需要识别的图像，如果frame为None，并且视频流已经启动，则自动获取最新的一帧填入
        :param width: 图像的宽度，如果frame为None,width可不填
        :param height: 图像的高度，如果frame为None,height可不填
        :return:
                  | []:未识别到二维码 
                  | [[数据,中心X坐标,中心Y坐标,二维码面积,二维码旋转角度], [...], ...]:识别到的二维码

        .. warning::
          需要飞机连接上摄像头，并且创建设备时设备类型需要设置为EquipmentType.CameraPlane
        ---------------------------------
        Detect QR code. The QR codes are custom for Folk

        :param frame: the frame used for target detection. When frame is None and the video streaming is on, the current frame will be set
        :param width: frame's width, when frame is None, it doesn't need to set
        :param height: frame's height, when frame is None, it doesn't need to set
        :return:
                  | []:failed to detect any QR code
                  | [[data, x-coordinate of center, y-coordinate of center, size, angle], [...], ...]:QR code is detected

        .. warning::
          A camera should be installed on the plane and the equipment type should be EquipmentType.CameraPlane when creating a equipment
        '''
        return self._control_server.ai_qrcode_detect(frame,width,height)

#=============================================Led Control========================================================================#

    def led_get(self, led_id):
        '''
        获取飞机灯带灯光样式
        
        :param led_id: 灯光编号（0-5）
        :return:
                  | []:参数错误
                  | [r, g, b, delay, mode, send]:获取灯光当前样式状态成功 
                  | r:红色灯亮度(延时模式:0-255 三色灯模式:0)
                  | g:绿色灯亮度(延时模式:0-255 三色灯模式:0)
                  | b:蓝色灯亮度(延时模式:0-255 三色灯模式:0)
                  | delay:剩余时长(ms)
                  | mode:灯光模式(延时模式:0 三色灯模式:1)
                  | send:灯光样式是否已经提交。使用led_set_sync设置灯光样式后灯光样式处于未提交状态，调用led_set_sync_confirm后灯光样式才会提交(未提交:0, 已提交:1)
                  
        .. warning::
          需要飞机连接上灯带，并且创建设备时，设备类型需要设置为EquipmentType.LedPlane
        ---------------------------------
        Get the led status of light band
        
        :param led_id: led id(0-5)
        :return:
                  | []:parameter error
                  | [r, g, b, delay, mode, send]:light band status is get
                  | r:red channel(mode0:0-255 mode1:0)
                  | g:red channel(mode0:0-255 mode1:0)
                  | b:red channel(mode0:0-255 mode1:0)
                  | delay:delay time(ms)
                  | mode:light mode(delay mode:0 three-color-change mode:1)
                  | send:whether the led status is sent to equipment(no:0 yes:1). It will be 0 after function led_set_sync is called, and will be 1 after function led_set_sync_confirm is called.

        .. warning::
          A light band should be installed on the plane and the equipment type should be EquipmentType.LedPlane when creating a equipment
        '''
        return self._control_server.led_get(led_id)
        
    def led_set(self, led_id, mode, delay, r, g, b):
        '''
        设置灯光样式
        
        :param led_id: 灯光编号（0-5）
        :param mode: 灯光模式（填0）
        :param delay: 时长(0-50000ms)
        :param r: 灯光红色色值(0-255)
        :param g: 灯光绿色色值(0-255)
        :param b: 灯光蓝色色值(0-255)
        :return:
                  | True:成功
                  | False:失败
                  
        .. warning::
          需要飞机连接上灯带，并且创建设备时，设备类型需要设置为EquipmentType.LedPlane
        ---------------------------------
        Set Led status and send it to equipment
        
        :param led_id: led id(0-5)
        :param mode: light mode(should be 0)
        :param delay: delay time(0-50000ms)
        :param r: red channel(0-255)
        :param g: red channel(0-255)
        :param b: red channel(0-255)
        :return:
                  | True:success
                  | False:failed

        .. warning::
          A light band should be installed on the plane and the equipment type should be EquipmentType.LedPlane when creating a equipment
        '''
        return self._control_server.led_set(led_id, mode, delay, r, g, b)
    
    def led_set_sync(self, led_id, mode, delay, r, g, b):
        '''
        同时设置灯光样式。调用该函数后灯光样式不会立即改变，需要调用led_set_sync_confirm提交灯光样式。连续使用led_set设置灯光时，无法保证灯光样式是同时配置的。使用该函数可以确保灯光样式是同时配置的。

        :param led_id: 灯光编号（0-5）
        :param mode: 灯光模式（填0）
        :param delay: 时长(0-50000ms)
        :param r: 灯光红色色值(0-255)
        :param g: 灯光绿色色值(0-255)
        :param b: 灯光蓝色色值(0-255)
        :return:
                  | True:成功
                  | False:失败

        .. warning::
          需要飞机连接上灯带，并且创建设备时，设备类型需要设置为EquipmentType.LedPlane
        ---------------------------------
        Set synchronous led status but not send it to equipment. It will be sent to equipment after function led_set_sync_confirm is called.

        :param led_id: led id(0-5)
        :param mode: light mode(should be 0)
        :param delay: delay time(0-50000ms)
        :param r: red channel(0-255)
        :param g: red channel(0-255)
        :param b: red channel(0-255)
        :return:
                  | True:success
                  | False:failed

        .. warning::
          A light band should be installed on the plane and the equipment type should be EquipmentType.LedPlane when creating a equipment
        '''
        return self._control_server.led_set_sync(led_id, mode, delay, r, g, b)
    
    def led_set_sync_confirm(self):
        '''
        提交灯光样式

        :return:
                  | True:成功
                  | False:失败
                  
        .. warning::
          需要飞机连接上灯带，并且创建设备时，设备类型需要设置为EquipmentType.LedPlane
        ---------------------------------
        Send the synchronous led status to equipment
        
        :return:
                  | True:success
                  | False:failed

        .. warning::
          A light band should be installed on the plane and the equipment type should be EquipmentType.LedPlane when creating a equipment
        '''
        return self._control_server.led_set_sync_confirm()

    def led_set_front_color(self, left_color, right_color, mode, delay, equipment_type, id = 0):
        '''
        飞机头部灯光设置

        :param left_color: 左灯颜色('red', 'green', 'black')
        :param right_color: 右灯颜色('red', 'green', 'black')
        :param mode: 灯光模式（填1）
        :param delay: 灯光时长(ms)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Set plane front's led status

        :param left_color: left led's color('red', 'green', 'black')
        :param right_color: right led's color('red', 'green', 'black')
        :param mode: light mode(should be 1)
        :param delay: delay time(ms)
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.led_set_front_color(left_color, right_color, mode, delay, equipment_type, id)

#=============================================Dance Control=====================================================================#

    def dance_fly_virtual_mode(self, flag): 
        '''
        切换舞步仿真模式，只有调用舞步模式相关接口才能仿真。在仿真模式下，调用dance_fly_takeoff会自动开启仿真界面。
        
        :param flag: True:进入仿真模式 False:退出仿真模式
        :return:
                  | True:进入（退出）仿真模式成功
                  | False:进入（退出）仿真模式失败
        ---------------------------------
        Switch to virtual mode. In virtual mode, plane's flight path will be showing in software when dance_fly_* function be called.
        
        :param flag: True:entry virtual mode False:exit virtual mode
        :return:
                  | True:switch mode success
                  | False:switch mode failed
        '''
        return self._control_server.dance_fly_virtual_mode(flag)

    def dance_fly_entry_dance_mode(self, equipment_type, id = 0):
        '''
        进入舞步飞行模式，只有进入舞步飞行模式后，才可以正常调用舞步飞行相关函数。
        
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:进入舞步飞行模式
                  | False:未能进入舞步飞行模式
        ---------------------------------
        Switch to dance mode. Only in dance mode can any dance_fly_* function be called. 
        
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_entry_dance_mode(equipment_type, id)

    def dance_fly_get_status(self, equipment_type, id = 0):
        '''
        返回飞机舞步执行状态(以dance为开头的函数)

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | lock:上锁
                  | unlock:解锁
                  | action_done:舞步执行完毕
                  | action:舞步执行中
                  | action_land:降落中
                  | action_low:低空飞行中
                  | action_takeoff:起飞中
                  | check_no_pass:自检未通过
        ---------------------------------
        equipment's flying status(the functions started with dance_fly_*)

        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | lock:lock
                  | unlock:unlock
                  | action_done:dance is done
                  | action:doing dance
                  | action_land:doing touchdown dance
                  | action_low:doing dance in low altitude
                  | action_takeoff:doing takeoff dance
                  | check_no_pass:plane is not ready to takeoff
        '''
        return self._control_server.dance_fly_get_status(equipment_type, id)

    def dance_fly_takeoff(self, block, equipment_type, id = 0):
        '''
        飞机起飞

        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Takeoff program
        
        :param block: whether to wait untill the program is done
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_takeoff(block, equipment_type, id)

    def dance_fly_touchdown(self, block, equipment_type, id = 0):
        '''
        飞机降落
        
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Landing program
        
        :param block: whether to wait untill the program is done
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_touchdown(block, equipment_type, id)
        
    def dance_fly_wait(self, time, block, equipment_type, id = 0):
        '''
        飞机悬停

        :param time: 悬停时间（1毫秒~600000毫秒）        
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Hover program

        :param time: hover time(1ms~600000ms)
        :param block: whether to wait untill the program is done
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_wait(time, block, equipment_type, id)

    def dance_fly_forward(self, distance, speed, block, equipment_type, id = 0):
        '''
        飞机向前飞
        
        :param distance: 飞行距离（1厘米~500厘米）
        :param speed: 飞行速度（0-200）
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flying forward program
        
        :param distance: flying distance(1cm~500cm)
        :param speed: flying speed
        :param block: whether to wait untill the program is done
        :param equipment_type: EquipmentType.Plane, EquipmentType.CameraPlane or EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_forward(distance, speed, block, equipment_type, id)
        
    def dance_fly_back(self, distance, speed, block, equipment_type, id = 0):
        '''
        飞机向后飞
        
        :param distance: 飞行距离（1厘米~500厘米）
        :param block: 是否等待动作完成再返回
        :param speed: 飞行速度（0-200）
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Flying back program
        
        :param distance: flying distance(1cm~500cm)
        :param speed: flying speed
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_back(distance, speed, block, equipment_type, id)
        
    def dance_fly_left(self, distance, speed, block, equipment_type, id = 0):
        '''
        飞机向左飞
        
        :param distance: 飞行距离（1厘米~500厘米）
        :param speed: 飞行速度（0-200）
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flying left program
        
        :param distance: flying distance(1cm~500cm)
        :param speed: flying speed
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_left(distance, speed,block, equipment_type, id)
        
    def dance_fly_right(self, distance, speed, block, equipment_type, id = 0):
        '''
        飞机向右飞
        
        :param distance: 飞行距离（1厘米~500厘米）
        :param speed: 飞行速度（0-200）
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flying right program
        
        :param distance: flying distance(1cm~500cm)
        :param speed: flying speed
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_right(distance,speed,block, equipment_type, id)
        
    def dance_fly_up(self, height, speed, block, equipment_type, id = 0):
        '''
        飞机向上飞
        
        :param distance: 飞行距离（1厘米~500厘米）
        :param speed: 飞行速度（0-200）
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flying up program
        
        :param height: flying up height(1cm~500cm)
        :param speed: flying speed
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_up(height, speed,block,equipment_type, id)
        
    def dance_fly_down(self, height, speed, block, equipment_type, id = 0):
        '''
        飞机向下飞
        
        :param distance: 飞行距离（1厘米~500厘米）
        :param speed: 飞行速度（0-200）
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flying down program
        
        :param height: flying down height(1cm~500cm)
        :param speed: flying speed
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_down(height, speed,block,equipment_type, id)

    def dance_fly_turnleft(self, angle, block, equipment_type, id = 0):
        '''
        飞机左转
        
        :param block: 是否等待动作完成再返回
        :param angle: 旋转角度（1度~360度）
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Turning left program
        
        :param angle: turn left angle(1°~360°)
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_turnleft(angle,block, equipment_type, id)

    def dance_fly_turnright(self, angle, block, equipment_type, id = 0):
        '''
        飞机右转
        
        :param block: 是否等待动作完成再返回
        :param angle: 旋转角度（1度~360度）
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Turning right program
        
        :param angle: turn right angle(1°~360°)
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_turnright(angle,block, equipment_type, id)

    def dance_fly_turnleftrounds(self, rounds, block, equipment_type, id = 0):
        '''
        飞机向左转圈
        
        :param block: 是否等待动作完成再返回
        :param rounds: 旋转圈数（1~10）
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Anticlockwise spin program

        :param rounds: number of cycles(1~10)
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_turnleftrounds(rounds, block,equipment_type, id)

    def dance_fly_turnrightrounds(self, rounds, block, equipment_type, id = 0):
        '''
        飞机向右转圈

        :param rounds: 旋转圈数（1~10）
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Clockwise spin program

        :param rounds: number of cycles(1~10)
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_turnrightrounds(rounds,block, equipment_type, id)        

    def dance_fly_bounce(self, time, block, equipment_type, id = 0):
        '''
        飞机进入弹跳模式

        :param time: 进入弹跳模式的时间（1ms~60000ms）
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Bounce program

        :param times: bounce time(1ms~60000ms)
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_bounce(time, block, equipment_type, id)

    def dance_fly_surround(self, radius, block, equipment_type, id = 0):
        '''
        飞机环绕飞行

        :param radius: 环绕半径(15cm~300cm)
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flying surround program

        :param radius: flying radius(15~300cm)
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_surround(radius, block,equipment_type, id)
        
    def dance_fly_straight_flight(self, x, y, z, speed, block, equipment_type, id = 0):
        '''
        飞机直线移动，(x,y,z)是从当前位置到目标位置的位移
        
        :param x: x分量(-500厘米 - 500厘米)
        :param y: y分量(-500厘米 - 500厘米)
        :param z: z分量(-300厘米 - 300厘米)
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Flying straight program. (x,y,z) is shift vector to the target position
        
        :param x: distance on x axis(-500cm - 500cm)
        :param y: distance on y axis(-500cm - 500cm)
        :param z: distance on z axis(-500cm - 500cm)
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_straight_flight(x, y, z, speed, block, equipment_type, id)

    def dance_fly_curve_flight_clockwise(self, x, y, z, speed, block, equipment_type, id = 0):
        '''
        飞机按照椭圆的方式顺时针方向曲线飞行，(x,y,z)是从当前位置到目标位置的位移
        
        :param block: 是否等待动作完成再返回
        :param x: 飞行距离(-500厘米 - 500厘米)
        :param y: 飞行距离(-500厘米 - 500厘米)
        :param z: 飞行距离(-300厘米 - 300厘米)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Flying curve program. (x,y,z) is the shift vector to the target position 

        :param x: shift on x axis(-500cm - 500cm)
        :param y: shift on y axis(-500cm - 500cm)
        :param z: shift on z axis(-300cm - 300cm)
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_curve_flight_clockwise(x, y, z,speed, block,equipment_type, id)

    def dance_fly_curve_flight_anticlockwise(self, x, y, z, speed, block, equipment_type, id = 0):
        '''
        飞机按照椭圆的方式逆时针方向曲线飞行，(x,y,z)是从当前位置到目标位置的位移
        
        :param block: 是否等待动作完成再返回
        :param x: 飞行距离(-500厘米 - 500厘米)
        :param y: 飞行距离(-500厘米 - 500厘米)
        :param z: 飞行距离(-500厘米 - 500厘米)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Flying curve program. (x,y,z) is the shift vector to the target position 

        :param x: shift on x axis(-500cm - 500cm)
        :param y: shift on y axis(-500cm - 500cm)
        :param z: shift on z axis(-500cm - 500cm)
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_curve_flight_anticlockwise(x, y, z,speed, block,equipment_type, id)

    def dance_fly_flip_forward(self, block, equipment_type, id = 0):
        '''
        飞机向前翻滚

        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Flipping forward program
        
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_flip_forward(block,equipment_type, id)

    def dance_fly_flip_back(self, block, equipment_type, id = 0):
        '''
        飞机向后翻滚
        
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flipping back program
        
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_flip_back(block,equipment_type, id)
        
    def dance_fly_flip_left(self, block, equipment_type, id = 0):
        '''
        飞机向左翻滚
        
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flipping left program
        
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_flip_left(block,equipment_type, id)
        
    def dance_fly_flip_right(self, block, equipment_type, id = 0):
        '''
        飞机向右翻滚
        
        :param block: 是否等待动作完成再返回
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flipping right program
        
        :param block: whether to wait untill the program is done
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.dance_fly_flip_right(block,equipment_type, id)
        
#=================================================Arm Control===============================================================#

    def single_fly_arm(self, equipment_type, id = 0):
        '''
        飞机解锁

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Unlock plane
        
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.single_fly_arm(equipment_type, id)

    def single_fly_disarm(self, equipment_type, id = 0):    
        '''
        飞机上锁，紧急停桨

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Lock plane

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.single_fly_disarm(equipment_type, id)

#=================================================Multiple Control===============================================================#

#=================================================Remote Control=================================================================#

    def remote_fly_entry_remote_mode(self, equipment_type, id = 0):
        '''
        进入遥控器模式，只有进入遥控器模式后，才可以正常调用遥控模式的相关控制函数。

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:进入遥控器模式
                  | False:未能进入遥控器模式
        ---------------------------------
        Switch to remote mode. Only in remote mode can any remote_fly_remote_* function be called. 

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.remote_fly_entry_remote_mode(equipment_type, id)

    def remote_fly_takeoff_remote(self, equipment_type, id = 0):
        '''
        遥控器模式起飞
    
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Takeoff in remote mode
        
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.remote_fly_takeoff_remote(equipment_type, id)

    def remote_fly_touchdown_remote(self, equipment_type, id = 0):
        '''
        遥控器模式降落
        
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功
                  | False:失败
        ---------------------------------
        Landing in remote mode

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.remote_fly_touchdown_remote(equipment_type, id)
        
    def remote_fly_remote(self, pitch, roll, yaw, accelerator, equipment_type, id = 0):
        '''
        遥控器模式控制飞行方向
        
        :param pitch: 俯仰(-1000,1000)
        :param roll: 横滚(-1000,1000)
        :param yaw: 航向(-1000,1000)
        :param accelerator: 油门(-1000,1000)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        
        .. note::
          pitch、roll、yaw、accelerator全为0时，代表飞机悬停。
        ---------------------------------
        Flying in remote mode
        
        :param pitch: picth(-1000,1000)
        :param roll: roll(-1000,1000)
        :param yaw: yaw(-1000,1000)
        :param accelerator: accelerator(-1000,1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        
        ..note::
            When pitch, roll, yaw and accelerator are 0, the plane will hover
        '''
        return self._control_server.remote_fly_remote(pitch, roll, yaw, accelerator, equipment_type, id)

    def remote_fly_forward_remote(self, speed, equipment_type, id = 0):
        '''
        遥控器模式控制飞机向前飞
        
        :param speed: 速度(-1000,1000)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Flying forward in remote mode
        
        :param speed: flying speed(-1000, 1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        '''
        return self.remote_fly_remote(speed, 0, 0, 0, equipment_type, id)
    
    def remote_fly_back_remote(self, speed, equipment_type, id = 0):
        '''
        遥控器模式控制飞机向后飞
        
        :param speed: 速度(-1000,1000)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Flying back in remote mode
        
        :param speed: flying speed(-1000, 1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        '''
        return self.remote_fly_remote(-speed, 0, 0, 0, equipment_type, id)
    
    def remote_fly_left_remote(self, speed, equipment_type, id = 0):
        '''
        遥控器模式控制飞机向左飞
        
        :param speed: 速度(-1000,1000)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Flying left in remote mode
        
        :param speed: flying speed(-1000, 1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        '''
        return self.remote_fly_remote(0, -speed, 0, 0, equipment_type, id)
    
    def remote_fly_right_remote(self, speed, equipment_type, id = 0):
        '''
        遥控器模式控制飞机向右飞
        
        :param speed: 速度(-1000,1000)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Flying right in remote mode
        
        :param speed: flying speed(-1000, 1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        '''
        return self.remote_fly_remote(0, speed, 0, 0, equipment_type, id)
    
    def remote_fly_up_remote(self, speed, equipment_type, id = 0):
        '''
        遥控器模式控制飞机向上飞
        
        :param speed: 速度(-1000,1000)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Flying up in remote mode
        
        :param speed: flying speed(-1000, 1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        '''
        return self.remote_fly_remote(0, 0, 0, speed, equipment_type, id)
    
    def remote_fly_down_remote(self, speed, equipment_type, id = 0):
        '''
        遥控器模式控制飞机向下飞
        
        :param speed: 速度(-1000,1000)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Flying down in remote mode
        
        :param speed: flying speed(-1000, 1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        '''
        return self.remote_fly_remote(0, 0, 0, -speed, equipment_type, id)

    def remote_fly_turnleft_remote(self, speed, equipment_type, id = 0):
        '''
        遥控器模式控制飞机向左转
        
        :param speed: 速度(-1000,1000)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Turning left in remote mode
        
        :param speed: flying speed(-1000, 1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        '''
        return self.remote_fly_remote(0, 0, -speed, 0, equipment_type, id)

    def remote_fly_turnright_remote(self, speed, equipment_type, id = 0):
        '''
        
        遥控器模式控制飞机向右转
        
        :param speed: 速度(-1000,1000)
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Turning right in remote mode
        
        :param speed: flying speed(-1000, 1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        '''
        return self.remote_fly_remote(0, 0, speed, 0, equipment_type, id)

    def remote_fly_flip_forward_remote(self, equipment_type, id = 0):
        '''
        飞机向前翻滚

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flipping forward in remote mode

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.remote_fly_flip_forward_remote(equipment_type, id)

    def remote_fly_flip_back_remote(self, equipment_type, id = 0):
        '''
        飞机向后翻滚

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flipping back in remote mode
        
        :param speed: flying speed(-1000, 1000)
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.remote_fly_flip_back_remote(equipment_type, id)

    def remote_fly_flip_left_remote(self, equipment_type, id = 0):
        '''
        飞机向左翻滚

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flipping left in remote mode

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.remote_fly_flip_left_remote(equipment_type, id)

    def remote_fly_flip_right_remote(self, equipment_type, id = 0):
        '''
        飞机向右翻滚

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | True:成功 
                  | False:失败
        ---------------------------------
        Flipping right in remote mode

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:success
                  | False:failed
        '''
        return self._control_server.remote_fly_flip_right_remote(equipment_type, id)
        
#=================================================Plane State====================================================================#

    def get_battery(self, equipment_type, id = 0):
        '''
        获取飞机电量
        
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return:
                  | 0-100:飞机电量
                  | -1:获取失败
        ---------------------------------
        Get equipment's power level
        
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | 0-100:power level
                  | -1:failed
        '''
        return self._control_server.get_battery(equipment_type, id)
        
    def get_attitude(self, equipment_type, id = 0):    
        '''
        获取飞机姿态

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return: [yaw, pitch, roll]:飞机的偏航角，俯仰角，翻滚角
        ---------------------------------
        Get equipment's attitude

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return: [yaw, pitch, roll]:plane attitude
        '''
        return self._control_server.get_attitude(equipment_type, id)

    def get_coordinate(self, equipment_type, id = 0):
        '''
        获取飞机坐标

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return: [x, y, z]: 飞机的x,y,z坐标
        ---------------------------------
        Get equipment's coordinates

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return: [x-coordinate, y-coordinate, z-coordinate]:coordinate is get
        '''
        return self._control_server.get_coordinate(equipment_type, id)

    def get_speed(self, equipment_type, id = 0):
        '''
        获取飞机飞行速度

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return: [x, y, z]:飞机的x,y,z轴速度（厘米/秒）
        ---------------------------------
        Get equipment's speed

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return: [x-speed, y-speed, z-speed]:flying speed is get(cm/s)
        '''
        return self._control_server.get_speed(equipment_type, id)

    def get_accelerated_speed(self, equipment_type, id = 0):
        '''
        获取飞机飞行加速度

        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        :return: [x, y, z]:飞机的x,y,z轴加速度(厘米/(秒*秒))
        ---------------------------------
        Get equipment's acceleration

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return: [x-speed, y-speed, z-speed]:acceleration on three axis(cm/s)
        '''
        return self._control_server.get_accelerated_speed(equipment_type, id)

    def get_sensor_is_healthly(self, equipment_type, id = 0):
        '''
        获取飞机传感器健康状态
        
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param  id: 无人机编号，不填时默认为0
        :return:
                  | True:健康 
                  | False:异常
        ---------------------------------
        Whether sensor is healthly

        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        :return:
                  | True:healthly
                  | True:abnormal
        '''
        return self._control_server.get_sensor_is_healthly(equipment_type, id)

    def get_version(self,equipment_type, id = 0):
        '''
        获取飞机版本号

        :return: 
                  | 飞机版本号:成功
                  | '':失败
        ---------------------------------
        Get equipment's firmware version

        :return: 
                  | firmware version:success
                  | '':failed
        '''
        return self._control_server.get_version(equipment_type,id)

#=====================================================Extend====================================================================#

    def extend_get_data(self):
        '''
        拓展接口
        ---------------------------------
        For extend
        '''
        return self._control_server.extend_get_data()

#=====================================================Debug=====================================================================#

    def show_plane_sensor(self, equipment_type, id = 0):
        '''
        打印输出飞机传感器健康状态
        
        :param equipment_type: 无人机设备类型 EquipmentType.Plane、EquipmentType.CameraPlane、EquipmentType.LedPlane
        :param id: 无人机编号，不填时默认为0
        ---------------------------------
        Show equipment sensor status
        
        :param equipment_type:  EquipmentType.Plane, EquipmentType.CameraPlane and EquipmentType.LedPlane
        :param id: plane id, default is 0
        '''
        return self._control_server.show_plane_sensor(equipment_type, id)