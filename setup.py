import setuptools

setuptools.setup(
    name="Nuke Render Queue",
    version="0.1",
    author="Andrew Owen",
    author_email="your_email@example.com",
    description="A brief description of your package",
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/your_package_name",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # List your console scripts here
        ],
    },
)
