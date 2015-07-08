define({ "api": [  {    "type": "post",    "url": "/api/camera/capture",    "title": "Capture",    "name": "GetCapture",    "group": "Camera",    "description": "<p>Takes a picture and optional returns an image as base64 encoded string(optional)</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/camera.py",    "groupTitle": "Camera"  },  {    "type": "put",    "url": "/api/camera/focus/auto",    "title": "Autofocus",    "name": "GetFocusAuto",    "group": "Camera",    "description": "<p>Responsible for focus adjustment</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/camera.py",    "groupTitle": "Camera"  },  {    "type": "put",    "url": "/api/camera/focus/manual",    "title": "Manual focus",    "name": "GetFocusManual",    "group": "Camera",    "description": "<p>Manual focus in live view</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/camera.py",    "groupTitle": "Camera"  },  {    "type": "get",    "url": "/api/liveview/start",    "title": "Live View start",    "name": "GetLiveviewStart",    "group": "Camera",    "description": "<p>Starts a mjpeg stream of camera Live View</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/camera.py",    "groupTitle": "Camera"  },  {    "type": "put",    "url": "/api/camera/liveview/stop",    "title": "Live View stop",    "name": "GetLiveviewStop",    "group": "Camera",    "description": "<p>Stops mjpeg stream and camera Live View</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/camera.py",    "groupTitle": "Camera"  },  {    "type": "get",    "url": "/api/config/list",    "title": "List",    "name": "GetConfig",    "group": "Config",    "description": "<p>Returns a list of the current configuration</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/config.py",    "groupTitle": "Config"  },  {    "type": "get",    "url": "/api/config/get/:key",    "title": "Get Custom Value",    "name": "GetConfigByKey",    "group": "Config",    "description": "<p>Returns a value of a key or a list of values for a list of keys</p> ",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>Object</p> ",            "optional": false,            "field": "value",            "description": "<p>settings key(s) to get value</p> "          }        ]      },      "examples": [        {          "title": "Request-Example:",          "content": "{\n    \"value\" : \"shutterspeed2\"\n}\n\nor\n\n{\n    \"value\" : [\"shutterspeed2\", \"iso\", \"f-number\"]\n}",          "type": "json"        }      ]    },    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/config.py",    "groupTitle": "Config"  },  {    "type": "put",    "url": "/api/config/aperture",    "title": "Aperture",    "name": "SetAperture",    "group": "Config",    "description": "<p>Updates Aperture value for a connected Camera</p> ",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>Object</p> ",            "optional": false,            "field": "value",            "description": "<p>ISO value</p> "          }        ]      },      "examples": [        {          "title": "Request-Example:",          "content": "{\n    \"value\" : \"f\\/10\"\n}",          "type": "json"        }      ]    },    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 201 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/config.py",    "groupTitle": "Config"  },  {    "type": "put",    "url": "/api/config/iso",    "title": "ISO",    "name": "SetISO",    "group": "Config",    "description": "<p>Updates ISO value for a connected Camera</p> ",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>Object</p> ",            "optional": false,            "field": "value",            "description": "<p>ISO value</p> "          }        ]      },      "examples": [        {          "title": "Request-Example:",          "content": "{\n    \"value\" : \"400\"\n}",          "type": "json"        }      ]    },    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 201 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/config.py",    "groupTitle": "Config"  },  {    "type": "put",    "url": "/api/config/set/:key",    "title": "Set Custom Value",    "name": "SetKeyValue",    "group": "Config",    "description": "<p>Updates Camera configuration with a key value pair from listconfig settings</p> ",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "key",            "description": "<p>configuration key</p> "          },          {            "group": "Parameter",            "type": "<p>Object</p> ",            "optional": false,            "field": "value",            "description": "<p>value for key</p> "          }        ]      },      "examples": [        {          "title": "Request-Example:",          "content": "{\n    \"value\" : \"1\\/128\"\n}",          "type": "json"        }      ]    },    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 201 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/config.py",    "groupTitle": "Config"  },  {    "type": "put",    "url": "/api/config/shutterspeed",    "title": "Shutter speed",    "name": "SetShutterSpeed",    "group": "Config",    "description": "<p>Updates Shutter speed value for a connected Camera</p> ",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>Object</p> ",            "optional": false,            "field": "value",            "description": "<p>shutter speed value</p> "          }        ]      },      "examples": [        {          "title": "Request-Example:",          "content": "{\n    \"value\" : \"1\\/128\"\n}",          "type": "json"        }      ]    },    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 201 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/config.py",    "groupTitle": "Config"  },  {    "type": "post",    "url": "/api/fs/file",    "title": "Get File",    "name": "GetFilesystemFile",    "group": "File_system",    "description": "<p>returns an image in full resolution with exif information</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/fs.py",    "groupTitle": "File_system"  },  {    "type": "GET",    "url": "/api/fs/list",    "title": "List File System",    "name": "GetFilesystemList",    "group": "File_system",    "description": "<p>returns a tree containing camera file system</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/fs.py",    "groupTitle": "File_system"  },  {    "type": "post",    "url": "/api/fs/previews",    "title": "Preview for Files",    "name": "GetFilesystemPreview",    "group": "File_system",    "description": "<p>returns the preview images for a list of files</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/fs.py",    "groupTitle": "File_system"  },  {    "type": "get",    "url": "/api/status",    "title": "Status",    "name": "GetStatus",    "group": "Status",    "description": "<p>Returns the camera state (found or not)</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK    \n{\n    \"camera\": true,\n    \"state\": \"ok\"\n}",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/status.py",    "groupTitle": "Status"  },  {    "type": "get",    "url": "/api/status/summary",    "title": "Summary",    "name": "GetSummary",    "group": "Status",    "description": "<p>Returns an array containing camera informations</p> ",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "HTTP/1.1 200 OK    \n{        \n    \"state\": \"ok\",\n    \"summary\": [\n        \"Hersteller: Nikon Corporation\",\n        \"Modell: D90\",\n        \" Version: V1.00\",\n        \" Seriennummer: xxxxxx\",\n        ...\n    ]\n}",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "RemoteDslrApi/routes/status.py",    "groupTitle": "Status"  }] });