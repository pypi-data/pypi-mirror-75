import warnings

def raycheck():
    from .base import BaseStudy
    from .ray import RayStudy
    from ..helpers import is_winos
    """
    Checks operating system and returns appropriate
    Study class; RayStudy not available on Windows systems
    """
    if is_winos():
        return BaseStudy
    else:
        return RayStudy

class CaseStudy(raycheck()):
    def __init__(self, *args, **kwargs):
        if 'RayStudy' not in str(CaseStudy.__bases__[0]):
            warnings.warn("""RayStudy has not been inherited, likely because
                Ray is not compatible with your machine. This is not recommended. 
                Ray provides significant performance improvements and certain
                BaseStudy methods are not optimized.
                """, stacklevel=2)
        super().__init__(*args, **kwargs)