from skbuild import setup as _skbuild_setup


_cython_keywords = []

def setup(*args, **kw):
    cython_metadata = { key: value for key, value in _cython_keywords.items() if key in kw }
    dist = __skbuild_setup(*args, **kw)
    dist.cython_metadata = cython_metadata
    return dist
