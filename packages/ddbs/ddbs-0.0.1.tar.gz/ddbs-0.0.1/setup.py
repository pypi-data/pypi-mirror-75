""" Setup file for the Docker Dev Build System """

import setuptools


with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()


setuptools.setup(
    name='ddbs',
    version='0.0.1',
    author='Zachary A. Tanenbaum',
    author_email='ZachTanenbaum+docker_dev_build_system@gmail.com',
    description='A package for injecting a development env into a docker compose project.',
    url='https://github.com/ZacharyATanenbaum/docker_dev_build_system',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'docker_dev_build_system = docker_dev.__main__:main',
        ]
    },
)
