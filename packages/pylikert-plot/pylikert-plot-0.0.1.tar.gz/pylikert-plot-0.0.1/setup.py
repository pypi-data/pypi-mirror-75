from distutils.core import setup

from setuptools import find_packages

setup(
    name='pylikert-plot',
    packages=find_packages(),
    version='0.0.001',
    license='MIT',
    description='Plot likert questions in stacked distributed plot style',
    author='Cong Wang',
    url='https://github.com/jennnifer90/pylikert-plot',
    keywords=['likert', 'matplotlib', 'survey'],
    install_requires=[
        'matplotlib',
        'mpl-format',
        'pandas',
        'seaborn'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
