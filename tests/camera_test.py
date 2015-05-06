from RemoteDslrApi.camera import Camera
import unittest
from mock import patch


@patch('gphoto2.Camera')
@patch('gphoto2.Context')
@patch('gphoto2.CameraWidget')
class CameraTest(unittest.TestCase):        
    def setUp(self):
        unittest.TestCase.setUp(self)
        
    def tearDown(self):        
        pass  
        
    
    def test_initialize(self, widget, ctx, cam):
        c = Camera()
        self.assertTrue(c.has_camera, "Camera found")
        self.assertFalse(c.is_busy, "camera isn't busy on int")
        self.assertFalse(c.preview_running, "preview mode has to be false")
        
    
    def test_initialize_fail(self, widget, ctx, cam):
        ex_message = "throw an exception and fail initialize"
        cam.return_value.init.side_effect = Exception(ex_message)
        c = Camera()
        self.assertFalse(c.has_camera, "Camera not found")
        self.assertFalse(c.is_busy, "camera isn't busy on init fail")
        self.assertFalse(c.preview_running, "preview mode has to be false on init fail")
        self.assertEquals(ex_message, c.get_last_error().message, "last error should contain exception message")

    def test_methods_raise_without_camera(self, widget, ctx, cam):
        ex_message = "exception message"
        cam.return_value.init.side_effect = Exception(ex_message)
        c = Camera()
        self.assertFalse(c.has_camera, "Camera found")
        self.assertRaises(Exception, c.capture)
        self.assertRaises(Exception, c.start_preview)
        self.assertRaises(Exception, c.stop_preview)
        self.assertRaises(Exception, c.read_liveview_frame)
        self.assertRaises(Exception, c.manual_focus)
        self.assertRaises(Exception, c.set_capture_target)
        self.assertRaises(Exception, c.get_summary)
        self.assertRaises(Exception, c.get_config)
        self.assertRaises(Exception, c.get_config_value)
        self.assertRaises(Exception, c.set_config_value)
