# -*- coding: utf-8 -*-
import gphoto2 as gp
from RemoteDslrApi.error import RemoteDslrApiError

class CameraController:
    def __init__(self):
        try:
            self.__last_error = None
            self.__context = gp.Context()
            self.__camera = gp.Camera()
            self.__camera.init(self.__context)
            self.__has_camera = True
            self.__is_busy = False
        except Exception as ex:
            print ex
            self.__has_camera = False
            self.__last_error = ex                   
        
    def has_camera(self):
        return self.__has_camera 
    
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
    
    def set_iso(self, value):
        self.__set_widget_value("iso", value)
        
    def set_aperture(self, value):
        self.__set_widget_value("f-number", value)
        
    def set_shutter_speed(self, value):
        self.__set_widget_value("shutterspeed2", value)
    
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
    
    def __set_widget_value(self, key, value):
        self.__check_busy()
        self.__is_busy = True
        
        try:            
            root = self.__camera.get_config(self.__context)
            child = root.get_child_by_name(key)
            child.set_value(value)
            self.__camera.set_config(root, self.__context)
        except Exception as ex:
            self.__is_busy = False
            raise ex
    
    def __check_busy(self):
        if(self.__is_busy):
            raise RemoteDslrApiError("Camera is busy", 503)         
    
    def __del__(self):
        if(self.__camera != None and self.__context != None):
            self.__camera.exit(self.__context)