# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitvector']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bitvector-for-humans',
    'version': '0.14.0',
    'description': 'A simple pure python Bit Vector class for Humans™.',
    'long_description': '![Pytest 3.7](https://github.com/JnyJny/bitvector/workflows/Pytest%203.7/badge.svg)\n\n# Bit Vectors For Humans™\n\nThis simple bit vector implementation aims to make addressing single\nbits a little less fiddly. It can be used by itself to work with bit\nfields in an integer word, but it really starts to shine when you use\nthe supplied `BitField` descriptor with a subclass of `BitVector`:\n\n```python\n> from bitvector import BitVector, BitField\n>\n> class IOTDeviceCommand(BitVector):\n>     def __init__(self):\n>         super().__init__(size=32)\n>\n>     power = BitField(0, 1) # offset and size\n>     spin  = BitField(1, 1)\n>     speed = BitField(2, 4)\n>     sense = BitField(6, 2)\n>     red   = BitField(8, 8)\n>     blue  = BitField(16, 8)\n>     green = BitField(24, 8)\n>\n> widget_cmd = IOTDeviceCommand()\n> widget_cmd.power = 1\n> widget_cmd.sense = 2\n> widget_cmd.speed = 5\n> widget_cmd.red = 0xaa\n> widget_cmd.blue = 0xbb\n> widget_cmd.green = 0xcc\n> widget_cmd\nIOTDeviceCommand(value=0xccbbaa95, size=32)\n> widget_cmd.bytes\nb\'\\xcc\\xbb\\xaa\\x95\'\n```\n\n\n## Installation\n\n```console\n$ pip install bitvector-for-humans\n$ pydoc bitvector\n...\n```\n\nOr directly from github:\n\n```console\n$ pip install git+https://github.com/JnyJny/bitvector.git\n```\n\n## Motivation\n\n1. Address sub-byte bits in a less error prone way.\n2. Minimize subdependencies.\n3. Learn something about descriptors. \n\n## Caveats\n\nThe tests need expanding and I got lazy when writing the multi-bit\nsetting / getting code and it could undoubtedly be improved. Pull\nrequests gladly accepted.\n\n## Other Ways to Implement a Bit Vector\n\n1. Python builtin `ctypes.Structure` allows sub-byte bit fields\n2. Python builtin `struct` provides extensive support for byte manipulations\n3. Python3 IntEnums can be used to build bit field masks\n4. The plain `int` will serve admirably with bitwise operators\n5. Provide cffi bindings to existing bit-twiddling libraries\n6. Use Numpy bool arrays as the "backing store"\n7. Other good ideas I overlooked, forgot about or just plain don\'t know.\n\n\n\n\n\n\n',
    'author': 'JnyJny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JnyJny/bitvector.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
