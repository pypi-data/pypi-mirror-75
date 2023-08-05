# Copyright (C) 2019 Spiralworks Technologies Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import base64
import os
import requests
import json
from robotlibcore import HybridCore, keyword
from PIL import Image

__version__ = '0.6.1'


class CaptchaLibrary(HybridCore):
    """ ``CaptchaLibrary`` is a Robot Framework Test Library \
        for decoding captchas.

    This document explains the usage of each keywords in this test library.
    For more information about Robot Framework, see http://robotframework.org

    == About ==

    Created: 23/09/2019 UTC + 8 Philippines

    Author: Joshua Kim Rivera | joshua.rivera@mnltechnology.com

    Company: Spiralworks Technologies Inc.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, serviceUrl=None,
                 header={'Content-Type': 'application/x-www-form-urlencoded'},
                 payloadType='base64Captcha'
                 ):
        """CaptchaLibrary requires that you provide the captcha service's url \
            upon import.

        - ``serviceUrl``:
            The Captcha URL Service.
        - ``header``
            (optional) default = Content-Type=application/x-www-form-urlencoded
        - ``payloadType``:
            (optional) default = base64Captcha
        """
        libraries = [
        ]
        HybridCore.__init__(self, libraries)
        self.payloadType = payloadType
        self.header = header
        self.serviceUrl = serviceUrl

    @keyword
    def capture_element_from_screenshot(self, imagepath, location,
                                        size, outputpath):
        """Crops the specified element from a screenshot given the \
            location and size using Python's Pillow Module. Fails if \
                the supplied image PATH does not exist.

        Example:
        | `Capture Element From Screenshot` | image.png | ${coordinates} | \
            ${size} | output.jpg |

        Where:
         - `image.png`       = path to the captcha image
         - `${coordinates}`  = element location, must be a dictionary
         - `${size}`         = element size, must be a dictionary
         - `outputpath`      = cropped_image
        """
        try:
            image = Image.open(imagepath)
        except Exception as e:
            raise e
        element = image.crop((int(location['x']),
                              int(location['y']),
                              int(size['width'])+int(location['x']),
                              int(size['height'])+int(location['y'])
                              ))
        element.save(outputpath)

    @keyword
    def convert_captcha_image_to_base64(self, imagepath):
        """Converts the supplied Captcha image to a Base64 String.
        Fails if the image does not exist
        Example:
        | `Convert Captcha Image To Base64` | captcha.png |

        Where:
         - `captcha.png` = the captcha image to be converted to \
             Base64 String.
        """
        try:
            with open(imagepath, "rb") as img_file:
                decoded_string = base64.b64encode(img_file.read())
                decoded_string = decoded_string.decode("utf-8")
                return decoded_string
        except Exception as e:
            raise e

    @keyword
    def get_bypass_captcha_token(self, baseURL,
                                 header={'Accept': 'application/json'}):
        """Sends a GET Request to the base URL to retrieve the token to be
            used to bypass the captcha.
        """
        return self._create_get_request_for_captcha_bypass_token(baseURL,
                                                                 header)

    @keyword
    def decode_base64_captcha(self, imagepath):
        """Decodes the Base64 Captcha Image by converting the supplied \
            captcha image by sending a request to the captcha service URL.
        Example:
        | ${captcha_string} | `Decode Base64 Captcha` \
            | path/to/captcha/image |
        """
        base64_string = self.convert_captcha_image_to_base64(imagepath)
        payload = {self.payloadType: base64_string}
        decoded_string = \
            self._send_post_request_to_service_url(self.serviceUrl,
                                                   self.header, payload)
        return decoded_string.text

    def _create_get_request_for_captcha_bypass_token(self, baseURL, header):
        """ Provide Documentation.
        """
        req = requests.get(baseURL, headers=header)
        req = req.json()
        return req['ResponseData']

    def _send_post_request_to_service_url(self, serviceUrl, header, payload):
        """Send a POST Request to the Captcha Service API.
        """
        req = requests.post(serviceUrl, data=payload, headers=header)
        return req
