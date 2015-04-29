from RemoteDslrApi.camera import Camera
import unittest
import mock
from mock import patch


class CameraTest(unittest.TestCase):        
    def setUp(self):
        unittest.TestCase.setUp(self)
        
    def tearDown(self):        
        pass  
        
    
    @patch('gphoto2.Camera')
    @patch('gphoto2.Context')
    @patch('gphoto2.CameraWidget')
    def test_initialize(self, widget, ctx, cam):
        widget.get_choice.return_value={'choices' : {'23', 'test', 'test123'}}
        c = Camera()
        self.assertTrue(c.has_camera, "Camera found")
        
    @patch('gphoto2.Camera', side_effect=Exception )
    @patch('gphoto2.Context')
    @patch('gphoto2.CameraWidget')
    def test_initialize_fail(self, widget, ctx, cam):         
        cam.init.side_effect = Exception("boom")
        c = Camera()
        print c.has_camera
        self.assertTrue(c.has_camera, "Camera found")        
         