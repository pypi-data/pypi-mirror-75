import sys
import numpy as np
import pandas as pd
import functools

from tqdm.auto import tqdm

class ProgressBar:
    def __init__(self, num_checks, init_desc):
        self.num_checks = num_checks
        self.init_desc = init_desc

    def start(self):
        self.pbar = tqdm(
            total=self.num_checks, 
            desc=self.init_desc, 
            ncols=600, 
            bar_format='{desc}|{bar}{r_bar}'
        )

    def complete(self):
        self.pbar.set_description('Complete!')

    def wrap_multiple(self, instance, methods):
        for method, desc in methods:
            class_method = getattr(instance, method.__name__)
            wrapped_method = ProgressBar.wrap(self=self, desc=desc)(class_method)
            setattr(instance, method.__name__, wrapped_method)

    @staticmethod
    def wrap(_func=None, *, self, desc: str, ticks=1):
        """
        _func allows function to be passed directly or allows parameters to be passed, in which case
        the function has to be passed alongside

        Decorator that turns any method into a progress bar checkpoint
        """
        def decorator(func):                
            @functools.wraps(func)
            def update(*args, **kwargs):
                self.pbar.set_description(desc)
                result = func(*args, **kwargs)
                self.pbar.update(ticks)
                return result
            return update
        
        if _func is None:
            return decorator
        else:
            return decorator(_func)

    @staticmethod
    def wrap_make(func):
        def wrapper(self, *args, **kwargs):
            if self.use_pbar:
                pbar = self._setup_pbar()
                pbar.start()
            func(self, *args, **kwargs)

            if self.use_pbar:
                pbar.complete()

        return wrapper