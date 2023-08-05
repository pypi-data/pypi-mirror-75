import setuptools

setuptools.setup(
    name="socket_messenger",
    version="v0.2-alpha",
    author="Vineet Kulkarni",
    author_email="2vineetk@gmail.com",
    description="Makes communication between devices using pubnub through Python easy",
    packages=["socket_messenger"],
    include_package_data=True,
    url = "https://github.com/vink246/socket_messenger.git",
    download_url = "https://github.com/vink246/socket_messenger/archive/0.2-alpha.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.5',
    install_requires= ["pubnub"]
)
