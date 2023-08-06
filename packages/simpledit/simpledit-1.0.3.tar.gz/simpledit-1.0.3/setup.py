from setuptools import setup

setup(name='simpledit',
    version='1.0.3',
    description='',
    url='https://gitlab.com/torresed/simpledit',
    author='Programmers',
    author_email='noreply@ufl.edu',
    license='GPL3',
    packages=['simpledit'],
    install_requires=['Pillow', 'PyQt5', 'PyQt5-sip', 'numpy', 'scikit-image'],
    include_package_data=True,
    scripts=['simpledit/SimplEdit'])