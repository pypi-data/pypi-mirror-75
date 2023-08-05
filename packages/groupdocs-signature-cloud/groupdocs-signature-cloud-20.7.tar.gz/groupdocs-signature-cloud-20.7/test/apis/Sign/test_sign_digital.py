# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd">
#   Copyright (c) 2003-2020 Aspose Pty Ltd
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

from __future__ import absolute_import

import unittest
import os

from groupdocs_signature_cloud import *
from test.test_context import TestContext
from test.test_file import TestFile

class TestSignDigital(TestContext):

    def test_sign_digital_image(self):
        # Digital signatures are not supported for images
        pass

    def test_sign_digital_pdf(self):
        test_file = TestFile.pdf_one_page()
        signedFileName = "Output\\PdfDigitalSigned.pdf"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_digital_presentation(self):
        # Digital signatures are not supported for presentations
        pass

    def test_sign_digital_spreadsheet(self):
        test_file = TestFile.spreadsheet_xlsx()
        signedFileName = "Output\\SpreadsheetDigitalSigned.xlsx"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_digital_wordprocessing(self):
        test_file = TestFile.word_docx()
        signedFileName = "Output\\WordDigitalSigned.docx"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)                       

    @staticmethod
    def populate_sign_options(signedFileName, testFile):
        opts = SignDigitalOptions()        
        
        # set signature properties
        opts.signature_type = 'Digital'
        opts.image_file_path = TestFile.additional_signature01().FilePath()
        opts.certificate_file_path = TestFile.additional_pfx().FilePath()
        opts.password = '1234567890'

        # set signature position on a page
        opts.left = 100
        opts.top = 100
        opts.width = 200
        opts.height = 100
        opts.location_measure_type = "Pixels"
        opts.size_measure_type = "Pixels"        
        opts.rotation_angle = 0
        opts.horizontal_alignment = "None"
        opts.vertical_alignment = "None"
        opts.margin = Padding()
        opts.margin.all = 5
        opts.margin_measure_type = "Pixels"

        # set signature appearance
        opts.transparency = 0.8

        opts.page = 1
        opts.all_pages = False
        ps = PagesSetup()
        ps.even_pages = False
        ps.first_page = True
        ps.last_page = False
        ps.odd_pages = False
        ps.page_numbers = [1]
        opts.pages_setup = ps

        settings = SignSettings()
        settings.file_info = testFile.ToFileInfo()
        settings.options = [opts]
        settings.save_options = SaveOptions()
        settings.save_options.output_file_path = signedFileName
        return settings
    
    def check_response(self, response, signedFileName):
        self.assertTrue(response)
        self.assertTrue(response.file_info)
        self.assertEqual(response.file_info.file_path, signedFileName)
        # Check signed file
        request = ObjectExistsRequest(signedFileName)        
        data = self.storage_api.object_exists(request)
        self.assertTrue(data.exists)         


if __name__ == '__main__':
    unittest.main()
