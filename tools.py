#!/usr/bin/env python
# -*- coding: utf-8 -*-

def daemonize(func):
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target = func, args = args,
                         kwargs = kwargs)
        func_hl.daemon = True
        func_hl.start()
        return func_hl

    return async_func
