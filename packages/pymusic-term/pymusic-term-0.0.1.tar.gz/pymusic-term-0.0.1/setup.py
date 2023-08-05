from setuptools import setup, find_packages

with open('requirements.txt','r') as req_file:
    required_packages= req_file.readlines()

with open('README.md','r') as readme_file:
    long_description=readme_file.read()

setup(
    name="pymusic-term",
    version="0.0.1",
    author="Gamaliel Garcia",
    author_email="",
    description="A music player and spotify client for a terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EGAMAGZ/pymusicterm",
    license="MIT",
    keywords="git cli cui curses command-line",
    classifiers=[
        'Intended Audience :: Information Technology',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3'
    ],
    packages=find_packages(exclude=['tests','docs']),
    entry_points={
        'console_scripts':['pymusicterm = pymusicterm:main',]
    },
    install_requires=required_packages,
    python_requires=">=3.8"
)
