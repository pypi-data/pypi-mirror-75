from __future__ import absolute_import

import os
import sys
__version__='1.1'
# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl
if __package__ == '':
    # __file__ is pip-*.whl/pip/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/pip'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)
# try:
#     from pip._internal import main as _main  # isort:skip # noqa
# except:
#     from pip import main as _main

def yxspkg_required_main(_main,args):
    sys.argv = args
    _main()
def main():
    print('####################################')
    argvs = sys.argv[:]
    for i in argvs:
        if '-i' == i:
            break 
    else:
        sys.argv.extend(('-i','https://pypi.tuna.tsinghua.edu.cn/simple'))
    print('Commands ',' '.join(sys.argv),'\n')
    # if sys.argv[1] == 'install' and sys.argv[2] == '*':
    #     from multiprocessing import Process
    #     modules = ['lxml','pandas','bs4','requests','PyQt5','imageio','rsa','scipy','matplotlib','opencv-python',
    #     'tushare','lulu','yxspkg_encrypt','yxspkg_tecfile','yxspkg_wget','IPython',
    #     'yxspkg_songzgif','tensorflow','keras','PyInstaller','twine','torch','torchvision',
    #     'mpl_finance','quandl','xlrd','pandas_datareader','pytecio','webfile','cheroot'] 
    #     a = []
    #     for i in modules:
    #         argvs[2] = i
    #         s = Process(target = yxspkg_required_main,args =(argvs[:],) )
    #         s.start()
    #         s.join()
    #     d ={'opencv-python':'cv2'}
    #     for i in modules:
    #         try:
    #             m = d.get(i,i)
    #             exec('import '+m)
    #             a.append(i)
    #         except:
    #             print("Failed to install "+i)
    #     print('#'*20)
    #     for i in a:
    #         print('Install {} successfully!'.format(i))
    # else:
    #     _main()
    import pip
    version = pip.__version__.split('.')[0]
    if int(version) >= 20:
        from pip._internal.cli import main
        _main = main.main
    else:
        try:
            from pip._internal import main as _main  # isort:skip # noqa
        except:
            from pip import main as _main
    _main()

if __name__ == '__main__':
    main()
