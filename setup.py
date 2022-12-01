# Licensed under the MIT License
# https://github.com/grongierisc/ipython-iris-magic/blob/main/LICENSE

import os

from setuptools import setup


def main():
    # Read the readme for use as the long description
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'README.md'), encoding='utf-8') as readme_file:
        long_description = readme_file.read()

    # Do the setup
    setup(
        name='ipython-iris-magic',
        description='ipython-iris-magic',
        long_description=long_description,
        long_description_content_type='text/markdown',
        version='0.0.5',
        author='grongier',
        author_email='guillaume.rongier@intersystems.com',
        keywords='ipython-iris-magic',
        url='https://github.com/grongierisc/ipython-iris-magic',
        license='MIT',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Topic :: Utilities'
        ],
        package_dir={'': 'src'},
        packages=['iris_magic'],
        python_requires='>=3.7',
        install_requires=[
            "ipython>=1.0",
            "ipython-genutils>=0.1.0",
            "sqlalchemy-iris>=0.4.0",
            "intersystems-iris",
        ]
    )


if __name__ == '__main__':
    main()
