import setuptools

from pulsestreamer.version import __CLIENT_VERSION__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pulsestreamer",
    version=__CLIENT_VERSION__,
    author="Swabian Instruments GmbH",
    author_email="support@swabianinstruments.com",
    description="A client software for Swabian Instrument's Pulse Streamer 8/2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.swabianinstruments.com/pulse-streamer-8-2/",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[
        'requests',
        'tinyrpc;python_version>="3.0"',
        'tinyrpc<1.0;python_version<"3.0"',
        'gevent-websocket',
        'numpy',
        'matplotlib',
        'enum34;python_version<"3.4"',
    ],
    extras_require={
        'grpc': ['grpcio', 'protobuf'], 
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
      #  "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Natural Language :: English",
    ],
)