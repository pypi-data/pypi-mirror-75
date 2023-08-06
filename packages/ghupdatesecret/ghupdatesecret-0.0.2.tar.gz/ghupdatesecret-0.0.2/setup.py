import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="ghupdatesecret",
    version="0.0.2",
    author="Ian Duncan",
    author_email="janskykd@gmail.com",
    description="A command-line utility to update GitHub repository secrets.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jansky/ghupdatesecret",
    packages=['ghupdatesecret'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Version Control",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    install_requires=['requests>=2.24.0', 'pynacl>=1.4.0'],
    entry_points={
        'console_scripts':
        ['ghupdatesecret=ghupdatesecret.ghupdatesecret:main']
    },
    python_requires='>=3.6',
)
