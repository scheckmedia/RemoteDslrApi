# -*- coding: utf-8 -*-
import gphoto2 as gp
from sys import platform
from os import system
from time import sleep
from RemoteDslrApi.error import RemoteDslrApiError
from RemoteDslrApi.image import Image, PreviewSize, ImagePath
import logging

class Camera:
    """
    Responsible for operations with a Camera    
    """
    def __init__(self):
        try:
            print "initialize camera..."
            logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
            gp.use_python_logging()
            # kill ptpcamera on osx which blocks a communication with the camera                 
            if platform == "darwin":
                system('killall PTPCamera 2> /dev/null')

            self.__is_busy = False
            self.__preview_running = False
            self.__last_error = None            
            self.__context = gp.Context()
            self.__camera = gp.Camera()
            self.__camera.init(self.__context)
            self.__has_camera = True
            self.set_capture_target(1)
            print "initialize camera finished"
        
        except Exception as ex:
            self.__has_camera = False
            self.__last_error = ex                   
    
    @property    
    def has_camera(self):        
        """
        determine a camera is connected and valid

        :returns: a flag to identify a camera was found
        :rtype: bool
        """
        return self.__has_camera 
    
    @property
    def is_busy(self):
        """
        flag to determine a camera is busy
        :return: a flag to check whether camera is in use
        :rtype: bool
        """
        return self.__is_busy
    
    @property
    def preview_running(self):        
        """
        flag to determine a camera is live view mode

        :returns: state of live view mode
        :rtype: bool
        """
        return self.__preview_running    
    
    def capture(self, return_image=True):
        """
        takes a picture and returns this, if needed
        
        Parameters
        ----------
        :type self: Camera
        return_image : bool
            if true image object will be returned (see :class:`Image`)        
                
        """
        if not self.__has_camera:
            raise self.__last_error
                                
        self.__check_busy()
        self.__is_busy = True
        
        if self.__preview_running:
            sleep(0.1)            
            self.__set_widget_value("viewfinder", 0, False)
            sleep(0.1)

        try:                                
            path = self.__camera.capture(gp.GP_CAPTURE_IMAGE, self.__context)
            data = None
            
            if return_image:
                camera_file = self.__camera.file_get(path.folder, path.name, gp.GP_FILE_TYPE_NORMAL, self.__context)
                data = memoryview(camera_file.get_data_and_size()).tobytes()

            return Image(data, path)  
        except Exception as ex:
            raise ex
        finally:
            self.__is_busy = False    
            if self.__preview_running:
                self.start_preview()              
    
    def start_preview(self):
        
        if not self.__has_camera:
            raise self.__last_error
                                
        self.__preview_running = True
        try:  
            pass           
        except Exception as ex:            
            raise ex
        finally:
            self.__is_busy = False        
    
    def stop_preview(self):
        if not self.__has_camera:
            raise self.__last_error                        
        
        try:            
            self.__preview_running = False
            self.__camera.exit(self.__context)
        except Exception as ex:            
            raise ex
        finally:
            self.__is_busy = False 
    
    def read_liveview_frame(self):
        if not self.__has_camera:
            raise self.__last_error            
        
        if self.__is_busy:
            return False
        
        try:            
            preview_file =  self.__camera.capture_preview(self.__context)
            preview = preview_file.get_data_and_size()
            return memoryview(preview).tobytes()
        except Exception as ex:            
            raise ex
    
    def manual_focus(self, step):
        if not self.__has_camera:
            raise self.__last_error
        
        self.__check_busy()
        self.__is_busy = True
        
        if not self.__preview_running:
            raise Exception("manual focus works only in live view mode")
        else:
            sleep(0.1)
            
        try:
            self.__set_widget_value("manualfocusdrive", float(step), False)
        except gp.GPhoto2Error as ex:
            if ex.code == -113:
                raise RemoteDslrApiError('Zoom reached max/min value', 405)
            else:
                raise ex
        except Exception as ex:            
            raise ex 
        finally:
            self.__is_busy = False

    def auto_focus(self):
        if not self.__has_camera:
            raise self.__last_error

        self.__check_busy()
        self.__is_busy = True

        try:
            self.__set_widget_value("autofocusdrive", 1, False)
        except Exception as ex:
            raise ex
        finally:
            self.__is_busy = False

    def set_capture_target(self, index):
        if not self.__has_camera:
            raise self.__last_error

        try:
            widget = self.__get_widget_value_by_key("capturetarget")
            choices = widget["choices"]
            if len(choices) > index:
                self.__set_widget_value("capturetarget", choices[index])
        except Exception as ex:            
            raise ex
        finally:
            self.__is_busy = False 

    def get_last_error(self): 
        return self.__last_error
    
    def get_summary(self):
        if not self.__has_camera:
            raise self.__last_error
                
        self.__check_busy()
        self.__is_busy = True
        
        text = self.__camera.get_summary(self.__context)
        data = str(text).splitlines()
        self.__is_busy = False
        return data
    
    def get_config(self):  
        if not self.__has_camera:
            raise self.__last_error
        
        self.__check_busy()
        self.__is_busy = True
        
        root = self.__camera.get_config(self.__context)
        settings = {}
        self.__read_widget(root, settings)
        self.__is_busy = False 
        return settings
    
    def get_config_value(self, key):
        if not self.__has_camera:
            raise self.__last_error
        print("is bussy %r" % self.__is_busy)
        if type(key) is list:
            settings = {}
            for k in key:
                settings[k] = self.__get_widget_value_by_key(str(k))
            return settings
        elif type(key) is unicode or type(key) is str:
            return self.__get_widget_value_by_key(str(key))
        else:
            raise RemoteDslrApiError("invalid key type", 400)
        
    def set_config_value(self, key, value):
        if not self.__has_camera:
            raise self.__last_error
        
        self.__check_busy()
        self.__is_busy = True
        
        if self.__preview_running:
            sleep(0.2)
            
        try:
            self.__set_widget_value(str(key), str(value))
        except Exception as ex:            
            raise ex 
        finally:
            self.__is_busy = False
        
    def read_folder(self, folder):
        if not self.__has_camera:
            raise self.__last_error

        self.__check_busy()
        self.__is_busy = True
        fs = {}
        try:
            self.__read_folder("/", fs)
        except Exception as ex:
            raise ex
        finally:
            self.__is_busy = False
        return fs

    def __read_folder(self, folder, node={}, recursive=True):
        folders = self.__camera.folder_list_folders(folder, self.__context)        
        files = self.__camera.folder_list_files(folder, self.__context)
        
        if folders.count() > 0:
            for index in range(0, folders.count()):
                name = folder + folders.get_name(index) + "/"
                node[name] = {}                
                
                if recursive:
                    self.__read_folder(name, node[name])

        if files.count() > 0:
            filelist = []
            for index in range(0, files.count()):                
                name = files.get_name(index)                                
                item = { 'file': name, 'path': folder}                
                filelist.append(item)
            node["files"] = filelist

    def read_file(self, f):
        if not self.__has_camera:
            raise self.__last_error

        self.__check_busy()
        self.__is_busy = True
        try:
            if type(f) is dict and f.has_key('file') and f.has_key('path'):
                image_path = ImagePath(f['path'], f['file'])
                return self.__read_file(image_path.folder, image_path.name, PreviewSize.big)
        except Exception as ex:
            raise ex
        finally:
            self.__is_busy = False

    def preview_for_files(self, files):
        if not self.__has_camera:
            raise self.__last_error

        self.__check_busy()
        self.__is_busy = True
        previews = []

        try:
            if type(files) is list:
                for f in files:
                    if type(f) is dict and f.has_key('file') and f.has_key('path'):
                        image = self.__read_file(f['path'], f['file'], PreviewSize.small)
                        d = image.copy()
                        d.update(f)
                        previews.append(d)
        except Exception as ex:
            raise ex
        finally:
            self.__is_busy = False

        return previews
    
    def __read_file(self, folder, filename, size):
        try:
            meta = self.__camera.file_get(str(folder), str(filename), gp.GP_FILE_TYPE_NORMAL, self.__context)
            data = memoryview(meta.get_data_and_size()).tobytes()
            path = ImagePath(folder, filename)
            img = Image(data, path, size)
            return img.serialize

        except Exception as ex:
            print(ex)

    def __read_widget(self, widget, settings={}):
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
        try:            
            # methods throws an error if no widget value is available, thats not that cool
            items = widget.count_choices()
            if items > 0:
                choices = []
                for index in range(0, items):                
                    choices.append(widget.get_choice(index))
                settings["choices"] = choices
        except Exception as ex:
            if ex.code != -2:
                raise ex
            
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
            
    def __set_widget_value(self, key, value, cast_as_string=True):                
        try:            
            root = self.__camera.get_config(self.__context)
            child = root.get_child_by_name(key)
            if cast_as_string:
                value = str(value)
                
            child.set_value(value)
            self.__camera.set_config(root, self.__context)
        except Exception as ex:            
            raise ex        
    
    def __check_busy(self):
        if self.__is_busy:
            raise RemoteDslrApiError("Camera is busy", 503)
    
    def __exit__(self):
        if self.__camera is not None and self.__context is not None:
            self.__camera.exit(self.__context)