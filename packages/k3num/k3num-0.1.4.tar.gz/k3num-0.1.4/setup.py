import setuptools
setuptools.setup(
    name="k3num",
    packages=["k3num"],
    version="0.1.4",
    license='MIT',
    description='Convert number to human readable format in a string.',
    long_description="# k3num\n\n[![Build Status](https://travis-ci.com/pykit3/k3num.svg?branch=master)](https://travis-ci.com/pykit3/k3num)\n[![Documentation Status](https://readthedocs.org/projects/k3num/badge/?version=stable)](https://k3num.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3num)](https://pypi.org/project/k3num)\n\nConvert number to human readable format in a string.\n\nk3num is a component of [pykit3] project: a python3 toolkit set.\n\n\n# Install\n\n```\npip install k3num\n```\n\n# Synopsis\n\n```python\n>>> readable(103425)\n'101.0K'\n>>> readable({ 'total': 10240, 'progress': [1, 1024*2.1, 1024*3.2], })\n{'total': '10K', 'progress': ['1', '2.10K', '3.20K']}\n>>> parsenum('5.2K')\n5324.8\n>>> parsenum('10%')\n0.1\n>>> value_to_unit[1024**2]\n'M'\n>>> unit_to_value['K']\n1024\n>>> Hex(0x0102, 4)\n'00000102'\n>>> Hex(0x0102, 'crc32')\n'00000102'\n>>> Hex.crc32(0x0102)\n'00000102'\n>>> Hex('00000102', 'crc32')\n'00000102'\n>>> Hex.crc32('00000102')\n'00000102'\n>>> Hex(('12', 1), 'crc32')\n'12010101'\n>>> Hex(0x0102, 'crc32') + 1\n'00000103'\n>>> Hex(0x0102, 'crc32') * 2\n'00000204'\n>>> Hex(0x0102, 'crc32') - 1000000\n'00000000'\n>>> Hex(0x0102, 'crc32') * 1000000000\n'ffffffff'\n>>> Hex.sha1(0) + Hex.sha1(('10', 0))\n'1000000000000000000000000000000000000000'\n>>> Hex.sha1(0) + Hex.sha1(('10', 0)) * 2\n'2000000000000000000000000000000000000000'\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3",
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/drmingdrmer/k3num',
    keywords=['human', 'readable', 'number', 'digit', 'integer'],
    python_requires='>=3.0',

    install_requires=['semantic_version==2.8.5', 'jinja2==2.11.2', 'PyYAML==5.3.1', 'k3ut==0.1.7', 'sphinx==3.0.3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
