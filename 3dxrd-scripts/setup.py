from distutils.core import setup
import glob

setup(
    name = '3dxrd-scripts',
    version = '0.1.0',
    author = 'Fable Development Team',
    description = 'diffraction data analysis',
    license = 'LGPLv2',
    packages = ['hedm-scripts'],
    scripts = glob.glob('scripts/*.py'),
    data_files = [('share/3dxrd-scripts', glob.glob('share/*.ini'))]
    )
