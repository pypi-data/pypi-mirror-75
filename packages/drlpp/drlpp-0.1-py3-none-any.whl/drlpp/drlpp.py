#
# dynamic resource locator protocol for python
#

import sys
import importlib
from urllib import parse as _urlparse

def import_drlpp_mod(scheme):
    modname = 'drlpp_' + scheme
    try:
        mod = importlib.import_module(modname)
    except ModuleNotFoundError as e:
        print('No a processing unit found for scheme "%s://". You may try ```pip install drlpp_%s``` if it is safe.' % (parsed.scheme, parsed.scheme))
        exit(1)
    return mod

def run_url(url, argus):
    if not '://' in url:
        print('No a url "%s"' % url)
        exit(1)
    parsed = _urlparse.urlparse(url)
    if not parsed.scheme:
        print('No a scheme "%s"' % url)
        exit(1)
    if not parsed.netloc:
        print('No a theme field "%s"' % url)
        exit(1)
    mod = import_drlpp_mod(parsed.scheme)
    m = mod.Main()
    themefunc = 'run_' + parsed.netloc
    try:
        func = getattr(m, themefunc)
    except AttributeError:
        print('No such theme "%s" for scheme "%s"' % (parsed.netloc, parsed.scheme))
        exit(1)
    retcode = func(path=parsed.path, **argus)
    if retcode != 0 :
        exit(1)
    exit(0)
    
def main():
    if sys.argv[1] == '--show-themes':
        mod = import_drlpp_mod(sys.argv[2])
        m = mod.Main
        print(m.__doc__ or '')
        print()        
        for x in m.__dict__:
            if x.startswith('run_'):
                print('*-*-*- theme::%s -*-*-*' % (x[4:]))
                print(m.__dict__[x].__doc__ or '')
        exit(0)
    else:
        argus = {}
        key = None
        ptr = []
        for x in sys.argv[2:]:
            if x.startswith('--'):
                key = x
                ptr = argus[x[2:]] = []
            if key is not None:
                ptr.append(x)
        for x in argus:
            if len(argus[x]) == 0:
                del argus[x]
        run_url(sys.argv[1], argus)
    
if __name__ == '__main__':
    main()