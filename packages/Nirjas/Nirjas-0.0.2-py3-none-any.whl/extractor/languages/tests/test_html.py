import unittest
import re, os
from languages import html
from binder import readSingleLine,readMultiLineDiff

class HTMLTest(unittest.TestCase):
    
    def test_output(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.html")
        self.start_exclamation = "<!--"
        self.end_exclamation = "-->"
        self.syntax_start = "/*"
        self.syntax_end ='*/'
        comment_single = html.readMultiLineDiff(path,self.start_exclamation,self.end_exclamation)
        comment_multiline = html.readMultiLineDiff(path,self.syntax_start,self.syntax_end)

        self.assertTrue(comment_single)
        self.assertTrue(comment_multiline)



    def test_outputFormat(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.html")
        self.start_exclamation = "<!--"
        self.end_exclamation = "-->"
        self.syntax_start = "/*"
        self.syntax_end ='*/'
        expected = html.htmlExtractor(path)
        comment_single = readMultiLineDiff(path,self.start_exclamation,self.end_exclamation)
        comment_multiline = readMultiLineDiff(path,self.syntax_start,self.syntax_end)
        file = path.split("/")
        output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "HTML",
        "total_lines": comment_single[4],
        "total_lines_of_comments": comment_single[3]+comment_multiline[3],
        "blank_lines": comment_single[5],
        "sloc": comment_single[4]-(comment_single[3]+comment_multiline[3]+comment_single[5])
        }],
        "single_line_comment": [],
        "cont_single_line_comment": [],
        "multi_line_comment": []
        }


        if comment_single:
            try:
                for idx,i in enumerate(comment_single[0]):
                    output['multi_line_comment'].append({"start_line": comment_single[0][idx], "end_line": comment_single[1][idx], "comment": comment_single[2][idx]})
            except:
                pass
        
        if comment_multiline:
            try:
                for idx,i in enumerate(comment_multiline[0]):
                    output['multi_line_comment'].append({"start_line": comment_multiline[0][idx], "end_line": comment_multiline[1][idx], "comment": comment_multiline[2][idx]})
            except:
                pass

        self.assertEqual(output,expected)  
    
    def test_Source(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.html")
        name = "source.txt"
        newfile = html.htmlSource(path,name)

        self.assertTrue(newfile)