import setuptools
from MsCoppel import version

with open("README.md", "r") as fh:
    long_description = ''  # fh.read()

setuptools.setup(
    name="MsCoppel",
    version=version,
    author="Enoi Barrera Guzman",
    author_email="zafiro3000x@gmail.com",
    description="Libreria para microservicios basados en mensajes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        'kafka-python==2.0.1',
        'Logbook',
        'asyncio-nats-client==0.9.2',
        'jaeger-client==4.1.0',
        'fluent-logger==0.9.3',
        'Flask==1.1.1',
        'bottle==0.12.18',
        'coloredlogs==14.0',
        'colorama==0.4.0',
        'Pygments==2.6.1',
        'event-signal==1.8.0',
        "redis==2.10.6",
        "pycryptodome==3.9.8"
    ]

)
