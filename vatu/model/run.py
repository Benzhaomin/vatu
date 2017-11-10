# -*- coding: utf-8 -*-
import time


class Run(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.get('uuid'):
            self['uuid'] = str(int(time.time() * 1000))
