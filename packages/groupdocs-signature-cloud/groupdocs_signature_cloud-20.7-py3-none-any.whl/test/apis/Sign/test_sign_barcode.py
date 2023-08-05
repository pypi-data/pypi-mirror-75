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

class TestSignBarcode(TestContext):

    def test_sign_barcode_image(self):
        test_file = TestFile.image_jpg()
        signedFileName = "Output\\ImageBarcodeSigned.jpg"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_barcode_pdf(self):
        test_file = TestFile.pdf_one_page()
        signedFileName = "Output\\PdfBarcodeSigned.pdf"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_barcode_presentation(self):
        test_file = TestFile.presentation_pptx()
        signedFileName = "Output\\PresentationBarcodeSigned.pptx"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_barcode_spreadsheet(self):
        test_file = TestFile.spreadsheet_xlsx()
        signedFileName = "Output\\SpreadsheetBarcodeSigned.xlsx"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_barcode_wordprocessing(self):
        test_file = TestFile.word_docx()
        signedFileName = "Output\\WordBarcodeSigned.docx"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)                       

    @staticmethod
    def populate_sign_options(signedFileName, testFile):
        opts = SignBarcodeOptions()        
        
        # set signature properties
        opts.signature_type = 'Barcode'
        opts.text = '123456789012'
        opts.barcode_type = 'Code128'
        opts.code_text_alignment = 'None'

        # set signature position on a page
        opts.left = 100
        opts.top = 100
        opts.width = 300
        opts.height = 100
        opts.location_measure_type = "Pixels"
        opts.size_measure_type = "Pixels"
        opts.stretch = "None"
        opts.rotation_angle = 0
        opts.horizontal_alignment = "None"
        opts.vertical_alignment = "None"
        opts.margin = Padding()
        opts.margin.all = 5
        opts.margin_measure_type = "Pixels"

        # set signature appearance
        opts.fore_color = Color()
        opts.fore_color.web = "BlueViolet"
        opts.border = BorderLine()
        opts.border.color = Color()
        opts.border.color.web = "DarkOrange"
        opts.border.visible = True
        opts.border.style = "Dash"
        opts.border.weight = 12

        opts.background_color = Color()
        opts.background_color.web = "DarkOrange"
        opts.transparency = 0.8
        opts.inner_margins = Padding()
        opts.inner_margins.all = 2

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
