from distutils.core import setup
from setuptools import find_packages

setup(
    name='mpl_format',
    packages=find_packages(),
    version='0.271',
    license='MIT',
    description='Library for easier formatting of matplotlib plots written in '
                'a functional style.',
    author='Vahndi Minah',
    url='https://github.com/vahndi/mpl-format',
    download_url='https://github.com/vahndi/mpl-format/archive/v_0.269.tar.gz',
    keywords=['matplotlib'],
    install_requires=[
        'compound-types',
        'matplotlib',
        'numpy',
        'seaborn',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
