# Python API for Fluke 971X Series Dry Wells #
## License ##
Copyright 2020 Fluke
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Purpose ##
This project allows users with Windows 10 to interact with their Fluke 917X Dry Wells. This API allows users to read settings, features, and update them with python coding.

The library is composed of:
* An API to interact with the RS232 serial interface of the dry well
* An example script initiating communication with the dry well then automating a ramp soak program while plotting live data.

## Testing ## 
This program has only been tested with Windows 10 and a Fluke 9173 dry well. Users with a variety of connected COM ports and/or a different operating system, should adjust the __init__ function for their circumstances. For example, Linux systems use a different syntax for connected devices and require adjustments to the __init__ coding.

## Dependencies ##
This program was developed with following python package versions.
* python            3.7.7
* pyserial          3.4
* vs2015_runtime    14.16.27012      
* dpython-dateutil  2.8.1
* matplotlib        3.1.3