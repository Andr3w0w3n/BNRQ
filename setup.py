import setuptools
import sys
import os

APP = ['RenderQ.py']
APP_NAME = 'RenderQ'
DATA_FILES = [('scripts', ['RenderQ/scripts/RenderScript.py'])]
OPTIONS = {
    'packages': ['RenderQ'],
    'include_files': ['RenderQ/scripts/RenderScript.py'],
    'entry_points': {
        'console_scripts': [
            'RenderQ = RenderQ.RenderQ:main'
        ],
    },
}

setuptools.setup(
    name="NukeRenderQueue",
    version="0.1",
    author="Andrew Owen",
    author_email="waowen17@gmail.com",
    description="This is a basic nuke render program.",
    long_description_content_type="text/markdown",
    url="https://github.com/Andr3w0w3n/BNRQ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows 10",
    ],
    python_requires='>=3.10.11',
    install_requires=[
        # List your dependencies here
    ],
    options={
        'pyinstaller': OPTIONS
    },
    app=APP,
    data_files=DATA_FILES,
    setup_requires=['pyinstaller']
)