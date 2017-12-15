# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from ..opener.base import Opener

from . import exchangefs



class ExchangeOpener(Opener):
    #~ protocols = ['exchange']
    protocols = [
        'ews',
        'ews_calendar',
        'ews_contacts',
        'ews_notes',
        'ews_tasks',
    ]

    _protocol_mapping = {
        'ews': exchangefs.ExchangeFS,
        #~ 'ews_calendar': exchangefs.ExchangeCalFS,
        #~ 'ews_contacts': exchangefs.ExchangeContactFS,
        #~ 'ews_notes': exchangefs.ExchangeNoteFS,
        #~ 'ews_tasks': exchangefs.ExchangeTaskFS,
    }

    #~ @staticmethod
    def open_fs(self, host, parse_result, writeable, create, cwd):
        #~ print repr((self, host, parse_result, writeable, create))
        fs_class = self._protocol_mapping[parse_result.protocol]
        #~ print fs_class
        #~ exhost, _, dir_path = parse_result.resource.partition('/')
        endpoint = host.split('@')[-1]
        if host.count('@') == 1:
            user = parse_result.username
            passwd = parse_result.password
        elif host.count('@') == 2:
            user = '%s@%s'%(host.split('@')[0].split('//')[1],host.split('@')[1].split(':')[0])
            passwd = host.split('@')[1].split(':')[1]
            
            
        #~ print '<<<<<<', parse_result
        exchange_fs = fs_class(
            service_endpoint=endpoint,
            username=user or '',
            password=passwd or '',
        )

        return exchange_fs
