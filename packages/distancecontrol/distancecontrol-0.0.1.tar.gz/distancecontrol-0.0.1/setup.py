from setuptools import setup, find_packages

setup(
    name='distancecontrol',
    version='0.0.1',
    description='A library used to control programs(mainly games) without focusing them.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='http://flafy.herokuapp.com/',
    author='Flafy Arazi',
    author_email='flafyarazi@gmail.com',
    license='MIT',
    keywords='control send keys game program without focus active top topmost SendMessage PostMessage',
    packages=find_packages(),
    install_requires=['pillow', 'pywin32'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)