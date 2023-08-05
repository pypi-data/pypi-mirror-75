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

class TestSignStamp(TestContext):

    def test_sign_stamp_image(self):
        test_file = TestFile.image_jpg()
        signedFileName = "Output\\ImageStampSigned.jpg"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_stamp_pdf(self):
        test_file = TestFile.pdf_one_page()
        signedFileName = "Output\\PdfStampSigned.pdf"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_stamp_presentation(self):
        test_file = TestFile.presentation_pptx()
        signedFileName = "Output\\PresentationStampSigned.pptx"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_stamp_spreadsheet(self):
        test_file = TestFile.spreadsheet_xlsx()
        signedFileName = "Output\\SpreadsheetStampSigned.xlsx"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)

    def test_sign_stamp_wordprocessing(self):
        test_file = TestFile.word_docx()
        signedFileName = "Output\\WordStampSigned.docx"        
        settings = self.populate_sign_options(signedFileName, test_file)            
        response = self.sign_api.create_signatures(CreateSignaturesRequest(settings))
        self.check_response(response, signedFileName)                       

    @staticmethod
    def populate_sign_options(signedFileName, testFile):
        opts = SignStampOptions()        
        
        # set signature properties
        opts.signature_type = 'Stamp'
        opts.image_file_path = TestFile.image_sign().FilePath()

        # set signature position on a page
        opts.left = 100
        opts.top = 100
        opts.width = 300
        opts.height = 200
        opts.location_measure_type = "Pixels"
        opts.size_measure_type = "Pixels"        
        opts.rotation_angle = 0
        opts.horizontal_alignment = "None"
        opts.vertical_alignment = "None"
        opts.margin = Padding()
        opts.margin.all = 5
        opts.margin_measure_type = "Pixels"

        # set signature appearance
        opts.background_color = Color()
        opts.background_color.web = "CornflowerBlue"   
        opts.background_color_crop_type = "InnerArea"
        opts.background_image_crop_type = "MiddleArea"
        opts.transparency = 0.8

        outline = StampLine()
        outline.text = "John Smith"
        outline.font = SignatureFont()
        outline.font.font_family = "Arial"
        outline.font.font_size = 12
        outline.font.bold = True
        outline.font.italic = True
        outline.font.underline = True
        outline.text_bottom_intent = 5
        outline.text_color = Color()
        outline.text_color.web = "Gold"
        outline.text_repeat_type = "FullTextRepeat"
        outline.background_color = Color()
        outline.background_color.web = "BlueViolet"
        outline.height = 20
        outline.inner_border = BorderLine()
        outline.inner_border.color = Color()
        outline.inner_border.color.web = "DarkOrange"
        outline.inner_border.style = "LongDash"
        outline.inner_border.transparency = 0.5
        outline.inner_border.weight = 1.2
        outline.outer_border = BorderLine()
        outline.outer_border.color = Color()
        outline.outer_border.color.web = "DarkOrange"
        outline.outer_border.style = "LongDashDot"
        outline.outer_border.transparency = 0.7
        outline.outer_border.weight = 1.4        
        outline.visible = True
        opts.outer_lines = [outline]

        innerline = StampLine()
        innerline.text = "John Smith"
        innerline.font = SignatureFont()
        innerline.font.font_family = "Times New Roman"
        innerline.font.font_size = 20
        innerline.font.bold = True
        innerline.font.italic = True
        innerline.font.underline = True
        innerline.text_bottom_intent = 3
        innerline.text_color = Color()
        innerline.text_color.web = "Gold"
        innerline.text_repeat_type = "None"
        innerline.background_color = Color()
        innerline.background_color.web = "CornflowerBlue"
        innerline.height = 30
        innerline.inner_border = BorderLine()
        innerline.inner_border.color = Color()
        innerline.inner_border.color.web = "OliveDrab"
        innerline.inner_border.style = "LongDash"
        innerline.inner_border.transparency = 0.5
        innerline.inner_border.weight = 1.2
        innerline.outer_border = BorderLine()
        innerline.outer_border.color = Color()
        innerline.outer_border.color.web = "GhostWhite"
        innerline.outer_border.style = "Dot"
        innerline.outer_border.transparency = 0.4
        innerline.outer_border.weight = 1.4        
        innerline.visible = True
        opts.inner_lines = [innerline]

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
