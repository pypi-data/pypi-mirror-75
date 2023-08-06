import os
from setuptools import setup

requirements = [
    "boto3",
    "sense-core>=0.2.82"
]

# with open("README.md", "r", encoding='utf-8') as fh:
#     long_description = fh.read()

setup(
    name='sense-file',
    version='0.0.15',
    packages=[
            "sense_file",
    ],
    license='BSD License',  # example license
    description='sense file',
    install_requires=requirements,
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://upload.pypi.org/legacy/',
    author='liuguangbin',
    author_email='liuguangbin@sensedeal.ai',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)