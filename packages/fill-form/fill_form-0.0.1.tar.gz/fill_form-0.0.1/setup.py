# sudo apt install python3-setuptools  ---> pehle Python3 ..ke under..setuptools..ko install karo.
from setuptools import setup   # setuptools, ke under 'setup.py' pehle se nahi tha.

setup(
    name = 'fill_form',
    version = '0.0.1',
    setup_requires=['wheel'],
    description = 'fill the form....',
    py_modules = ['fill_form'],
    package_dir = {'' : 'sanju' },  
                                  
)




