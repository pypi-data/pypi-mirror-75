from setuptools import setup, find_packages

setup(name='simpledit',
    version='0.1.2',
    description='',
    url='https://gitlab.com/torresed/simpledit',
    author='Programmers',
    author_email='noreply@ufl.edu',
    license='GPL3',
    packages=find_packages(),
    install_requires=['Pillow', 'PyQt5', 'PyQt5-sip', 'numpy', 'scikit-image'],
    include_package_data=True,
    scripts=['simpledit/SimplEdit'])