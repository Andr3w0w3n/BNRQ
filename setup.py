import setuptools
import sys
import os

APP = ['RenderQ.py']
APP_NAME = 'BNRQ'
DATA_FILES = [('scripts', ['BNRQ/scripts/RenderScript.py', 'BNRQ/scripts/RenderScriptList.py']),
              ('data', ['FourCharacter-Codes.json'])]
OPTIONS = {
    'packages': ['BNRQ'],
    'include_files': ['BNRQ/scripts/RenderScript.py', 'BNRQ/scripts/RenderScriptList.py'],
    'entry_points': {
        'console_scripts': [
            'RenderQ = RenderQ.RenderQ:main'
        ],
    },
}

setuptools.setup(
    name="Basic Nuke Render Queue",
    version="2.0",
    author="Andrew Owen",
    author_email="waowen17@gmail.com",
    description="This is a basic nuke render queue.",
    long_description_content_type="text/markdown",
    url="https://github.com/Andr3w0w3n/BNRQ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows 10",
    ],
    python_requires='>=3.7.7',
    install_requires=[
        # List your dependencies here
    ],
    options={
        'build_exe': {
            'packages': OPTIONS['packages'],
            'include_files': OPTIONS['include_files']
        }
    },
    data_files=DATA_FILES,
    entry_points=OPTIONS['entry_points'],
    setup_requires=['pyinstaller'],
    executables=[setuptools.Executable(script='RenderQ.py', base=None)]
)
