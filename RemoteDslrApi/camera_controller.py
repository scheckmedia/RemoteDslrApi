# -*- coding: utf-8 -*-
import gphoto2 as gp
from sys import platform
from os import system
from RemoteDslrApi.error import RemoteDslrApiError
from RemoteDslrApi.image import Image
from _ast import Load
import base64

class CameraController:
    def __init__(self):
        try:                        
            if platform == "darwin":
                print platform
                system('killall PTPCamera 2> /dev/null')
                
            self.__last_error = None
            self.__context = gp.Context()
            self.__camera = gp.Camera()
            self.__camera.init(self.__context)
            self.__has_camera = True            
            self.__is_busy = False     
            self.__preview_running = False       
            self.set_capture_target(1);
        except Exception as ex:
            print ex
            self.__has_camera = False
            self.__last_error = ex                   
        
    def has_camera(self):
        return self.__has_camera 
    
    @property
    def preview_running(self):
        return self.__preview_running
    
    def capture(self, return_image=True):
        if(self.__has_camera == False):
            raise self.__last_error
                
        self.__check_busy()
        self.__is_busy = True
        
        try:            
            path = self.__camera.capture(gp.GP_CAPTURE_IMAGE, self.__context)
            if(return_image):   
                camera_file = self.__camera.file_get(path.folder, path.name, gp.GP_FILE_TYPE_NORMAL, self.__context)        
                data = camera_file.get_data_and_size()
                img = Image(data)            
                return img            
        except Exception as ex:            
            raise ex
        finally:
            self.__is_busy = False        
    
    def start_preview(self):
        if(self.__has_camera == False):
            raise self.__last_error
                        
        self.__check_busy()
        self.__is_busy = True
        self.__preview_running = True
        try:  
            pass           
        except Exception as ex:            
            raise ex
        finally:
            self.__is_busy = False        
    
    def stop_preview(self):
        if(self.__has_camera == False):
            raise self.__last_error                        
        
        try:            
            self.__preview_running = False
            self.__camera.exit(self.__context)
        except Exception as ex:            
            raise ex
        finally:
            self.__is_busy = False 
    
    def set_capture_target(self, index):
        try:
            widget = self.__get_widget_value_by_key("capturetarget")
            choices = widget["choices"]
            print "choice: %s" % choices[index]
            self.__set_widget_value("capturetarget", choices[index]);
        except Exception as ex:            
            raise ex
        finally:
            self.__is_busy = False 
        
    
    def get_last_error(self): 
        return self.__last_error
    
    def get_summary(self):
        if(self.__has_camera == False):
            raise self.__last_error
                
        self.__check_busy()
        self.__is_busy = True
        
        text = self.__camera.get_summary(self.__context)
        data = str(text).splitlines()
        self.__is_busy = False
        return data
    
    def get_config(self):  
        if(self.__has_camera == False):
            raise self.__last_error
        
        self.__check_busy()
        self.__is_busy = True
        
        root = self.__camera.get_config(self.__context)
        settings = {}
        self.__read_widget(root, settings)
        self.__is_busy = False 
        return settings
    
    def get_config_value(self, key):
        print type(key)
        if (type(key) is list):
            settings = {}
            for k in key:
                settings[k] = self.__get_widget_value_by_key(str(k))
            return settings
        elif(type(key) is str): 
            return self.__get_widget_value_by_key(key)
        else:
            raise RemoteDslrApiError("invalid key type", 400)
        
    def set_config_value(self, key, value):
        self.__set_widget_value(str(key), str(value))
    
    def __read_widget(self, widget, settings = {}):                    
        items = widget.count_children()
        if items > 0:
            for index in range(0, items):
                child = widget.get_child(index)
                settings[child.get_name()] = {}
                self.__read_widget(child, settings[child.get_name()])
        else :            
            self.__get_widget_value(widget, settings)          
    
    def __get_widget_value(self, widget, settings):        
        settings["id"] = widget.get_id()
        settings["label"] = widget.get_label()
        settings["name"] = widget.get_name()
        settings["value"] = widget.get_value()
        settings["type"] = widget.get_type()                
            
        items = gp.gp_widget_count_choices(widget)
        if items > 0:
            choices = []
            for index in range(0, items):                
                choices.append(widget.get_choice(index))
            settings["choices"] = choices
    def __get_widget_value_by_key(self, key):
        self.__check_busy()
        self.__is_busy = True
        
        try:            
            root = self.__camera.get_config(self.__context)
            child = root.get_child_by_name(key)
            settings = {}
            self.__get_widget_value(child, settings)
            return settings
        except Exception as ex:            
            raise ex
        finally:
            self.__is_busy = False
            
    def __set_widget_value(self, key, value):
        self.__check_busy()
        self.__is_busy = True
        
        try:            
            root = self.__camera.get_config(self.__context)
            child = root.get_child_by_name(key)
            child.set_value(str(value))
            self.__camera.set_config(root, self.__context)
        except Exception as ex:            
            raise ex
        finally:
            self.__is_busy = False
    
    def __check_busy(self):
        if(self.__is_busy):
            raise RemoteDslrApiError("Camera is busy", 503)         
    
    def read_liveview_frame(self):
        if(self.__has_camera == False):
            raise self.__last_error            
        
        try:            
            preview_file = gp.CameraFile()            
            self.__camera.capture_preview(preview_file, self.__context)
            preview =  preview_file.get_data_and_size()
            return preview
        except Exception as ex:            
            raise ex
    
    def __exit__(self):
        print "exit"
        if(self.__camera != None and self.__context != None):
            self.__camera.exit(self.__context)