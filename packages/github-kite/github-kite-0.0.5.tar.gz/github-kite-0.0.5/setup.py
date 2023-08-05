import setuptools


setuptools.setup(
    name="github-kite",
    version="0.0.5",
    author="author no body",
    author_email="Shive.shell@gmail.com",
    description="github test proj",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/test/test",
    packages=['kiteprotocol'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "websocket_client",
        "netifaces",
    ],
    python_requires='>=3.8',
)