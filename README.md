# RemoteDslrApi


## Requirements:
- libjpeg8-dev
- python-dev
- libgphoto2-dev
- gir1.2-gexiv2-0.1 ( or exiv2 and GExiv2 compiled with introspection for OS X)

## Note: 
- **Raspbian:** Apparently the libgexiv package from Raspbian have a bug. I get a segmentation faul after extracting the preview image from exiv. Because of this I use the testing-packages from *stretch* repository
- **OS X:** The gexiv2 library from *brew* isn't compiled with introspection. You have to compile it by yourself 

## Licence
RemoteDslrApi - Python based API to interact with your DSLR [http://github.com/scheckmedia/RemoteDslrApi](http://github.com/scheckmedia/RemoteDslrApi) Copyright (C) 2015  Tobias Scheck

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.