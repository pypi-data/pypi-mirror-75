import setuptools
setuptools.setup(
    name="k3color",
    packages=["k3color"],
    version="0.1.0",
    license='MIT',
    description='create colored text on terminal',
    long_description="# k3color\n\n[![Build Status](https://travis-ci.com/pykit3/k3color.svg?branch=master)](https://travis-ci.com/pykit3/k3color)\n[![Documentation Status](https://readthedocs.org/projects/k3color/badge/?version=stable)](https://k3color.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3color)](https://pypi.org/project/k3color)\n\ncreate colored text on terminal\n\nk3color is a component of [pykit3] project: a python3 toolkit set.\n\n\n# Install\n\n```\npip install k3color\n```\n\n# Synopsis\n\n```python\n# output text in blue:\n>>> blue('I am blue')\n '\\x01\\x1b[38;5;67m\\x02I am blue\\x01\\x1b[0m\\x02'\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3",
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/drmingdrmer/k3color',
    keywords=['console', 'terminal', 'color'],
    python_requires='>=3.0',

    install_requires=['semantic_version~=2.8.5', 'jinja2~=2.11.2', 'PyYAML~=5.3.1', 'sphinx~=3.1.1', 'k3ut~=0.1.7'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
