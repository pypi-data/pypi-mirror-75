import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytrakem",
    version="0.0.1",
    author="Sergiy Popovych",
    author_email="sergiy.popovich@gmail.com",
    description="A python wrapper for TrakEM2 package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supersergiy/pytrakem",
    include_package_data=True,
    package_data={'': ['*.py']},
    install_requires=[
        'torchfields>=0.0.5',
        'torch>=1.5',
        #'pyimagej @ http://github.com/imagej/pyimagej.git@master',
        'pyjnius',
        'imageio',
        'imglyb',
        'numpy>=1.19.0',
        'scikit-image>=0.17.2',
    ],
    packages=setuptools.find_packages(),
)
