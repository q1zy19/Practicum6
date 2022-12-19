#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Settings():
    name = 'SelfMadeServer v0.0.1'
    port = 80
    other_port = 8080
    max_size = 16384
    directory = 'web'
    types = {'html': 'text/html; charset=UTF-8',
             'css': 'text/css',
             'js': 'text/javascript',
             'gif': 'image/gif',
             'png': 'image/png'}

    stat = {'200': 'OK',
            '403': 'Forbidden',
            '404': 'Not found'
    }
    conn = {
        'close': 'close',
        'keep-alive': 'keep-alive'
    }

