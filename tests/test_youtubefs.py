from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from fs.youtube import *


class TestYoutubeFS(unittest.TestCase):

    def make_fs(self):
        # Return an instance of your FS object here
        url = u'https://www.youtube.com/playlist?list=PLYlZ5VtcfgitfPyMGkZsYkhLm-eOZeQpY'
        self.url = url
        return YoutubeFS(url)

    def destroy_fs(self, fs):
        """
        Destroy a FS object.

        :param fs: A FS instance previously opened by
            `~fs.test.FSTestCases.make_fs`.

        """
        fs.close()

    def setUp(self):
        self.fs = self.make_fs()

    def tearDown(self):
        self.destroy_fs(self.fs)
        del self.fs
        
    def test_listdir(self):
        assert len(self.fs.listdir(u'/')) > 2
        
        
    def test_getinfo(self):
        files = self.fs.listdir(u'/')
        info = self.fs.getinfo(files[0])
        info = self.fs.getinfo(files[0],['basic','default'])
        
    def test_openbin(self):
        files = self.fs.listdir(u'/')
        fileobj = self.fs.openbin(files[0])
        print(fileobj.read(10))
        
        
        # ~ assert self.fs.isdir(u'/')
        # ~ assert self.fs.isdir(u'/')
        # ~ print (self.fs.getinfo(u'/%s'%files[0]).name)
        
        
        # ~ assert self.fs.listdir(u'/') == ['Planet Python']
        
        
        # ~ assert self.fs.listdir(u'/Planet Python')
        # ~ assert self.fs.isdir(u'/Planet Python')
        
    # ~ def test_getinfo(self):
        
        # ~ info = self.fs.getinfo(u'/').raw
        # ~ self.assertIsInstance(info['basic']['name'], text_type)
        # ~ self.asseertEqual(info['basic']['name'], '')
        # ~ self.assertTrue(info['basic']['is_dir'])
        
        # ~ info = self.fs.getinfo(u'/Planet Python').raw
        # ~ self.assertIsInstance(info['basic']['name'], text_type)
        # ~ self.assertEqual(info['basic']['name'], '')
        # ~ self.assertTrue(info['basic']['is_dir'])
        
        # ~ testfile = self.fs.listdir(u'/Planet Python')[0]
        # ~ print (testfile)
        
        # ~ info = self.fs.getinfo(u'/Planet Python/%s'%testfile).raw
        # ~ self.assertIsInstance(info['basic']['name'], text_type)
        # ~ self.assertEqual(info['basic']['name'], testfile)
        # ~ self.assertFalse(info['basic']['is_dir'])
        
        # ~ fo = self.fs.open(u'/Planet Python/%s'%testfile)
        # ~ print (repr(fo.read()))






# ~ def run():
    # ~ unittest.main()

# ~ if __name__ == '__main__':
    # ~ unittest.main()
