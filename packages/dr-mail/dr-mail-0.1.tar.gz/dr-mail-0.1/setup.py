import setuptools

with open('README.rst', 'rb') as fp:
    readme = fp.read()

# 版本号，自己随便写
VERSION = '0.1'

LICENSE = 'GNU General Public License v3.0'


setuptools.setup(
    name='dr-mail',
    version=VERSION,
    description=(
        'It\'s a simple email sending program'
    ),
    long_description=readme,
    author='Judy',
    author_email='ljd69154@liangjundi.cn',
    maintainer='Judy',
    maintainer_email='ljd69154@liangjundi.cn',
    license=LICENSE,
    packages=setuptools.find_packages(),
    platforms=["all"],
    url='',
    install_requires=[

        ],
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3'
    ],
)
