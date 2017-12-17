#~ # coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import with_statement

import pafy
from six.moves.urllib.request import urlopen

from .. import errors
from ..base import FS
from ..enums import ResourceType
from ..info import Info
from ..iotools import RawWrapper


class YoutubeFS(FS):
    
    """A filesystem for reading Youtube Playlists and Videos.

    Arguments:
        url (str): The YouTube URL for a Playlist or a Video

    """

    _meta = {
        'case_insensitive': False,
        'invalid_path_chars': '\0"\[]+|<>=;?*',
        'network': True,
        'read_only': True,
        'thread_safe': True,
        'unicode_paths': True,
        'virtual': False,
    }

    def __init__(self, url, playlist=True):
        super(YoutubeFS, self).__init__()
        self.playlist = playlist
        self.url = url
        self._cache = {}
        if playlist:
            self._title = pafy.get_playlist(self.url)['title']
        else:
            self._title = pafy.new(self.url).title

    def __str__(self):
        return 'YoutubeFS: %s' % self._title

    def _get_name(self, pafyobj):
        name = '%s.%s' % (pafyobj.title, pafyobj.getbest().extension)
        name.replace('/', '')
        name.replace('\\', '')
        return name

    def listdir(self, path):
        _path = self.validatepath(path)

        if _path in [u'.', u'/', u'./']:
            if self.playlist:
                parser = pafy.get_playlist(self.url)
                outlist = []
                for entry in parser['items']:
                    name = self._get_name(entry['pafy'])
                    self._cache[self.validatepath(u'/%s' % name)] = entry['playlist_meta']['encrypted_id']
                    outlist.append(u'%s' % name)
                return outlist
            else:
                parser = pafy.new(self.url)
                name = self._get_name(parser)
                self._cache[self.validatepath(u'/%s' % name)] = self.url
                return [name]
        else:
            if _path in self._cache:
                raise errors.DirectoryExpected(path)
            else:
                raise errors.ResourceNotFound(path)

    def getinfo(self, path, namespaces=None):
        _path = self.validatepath(path)
        namespaces = namespaces or ('basic')

        if _path in [u'', u'.', u'/', u'./']:

            info = Info({
                "basic":
                {
                    "name": '',
                    "is_dir": True
                },
                "details":
                {
                    "type": int(ResourceType.directory)
                }
                })
            return info
        else:
            if _path in self._cache:
                name = _path[1:]
                pafyobj = pafy.new(self._cache[_path])
                if not 'details' in namespaces:
                    info = Info({
                        "basic":
                        {
                            "name": name,
                            "is_dir": False
                        }})
                else:
                    stream = pafyobj.getbest()
                    info = Info({
                        "basic":
                        {
                            "name": pafyobj.title,
                            "is_dir": False
                        },
                        "details":
                        {
                            "type": int(ResourceType.file),
                            "size":stream.get_filesize(),
                        }
                        })
                return info
            else:
                raise errors.ResourceNotFound(path)

    def openbin(self, path, mode=u'r', *args, **kwargs):
        _path = self.validatepath(path)

        if mode == 'rt':
            raise ValueError('rt mode not supported in openbin')

        if mode == 'h':
            raise ValueError('h mode not supported in openbin')

        if not 'r' in mode:
            raise errors.Unsupported()

        try:
            pafyobj = pafy.new(self._cache[_path])
            url = pafyobj.getbest().url
            response = urlopen(url)
        except:
            raise errors.ResourceNotFound(path)

        class HTTPFile(RawWrapper):

            def writable(self):
                return False

            def seekable(self):
                return False

            def flush(self):
                return

        return HTTPFile(response, mode=mode, *args, **kwargs)

    def makedir(self, *args, **kwargs):
        raise errors.Unsupported()

    def remove(self, *args, **kwargs):
        raise errors.Unsupported()

    def removedir(self, *args, **kwargs):
        raise errors.Unsupported()

    def setinfo(self, *args, **kwargs):
        raise errors.Unsupported()
