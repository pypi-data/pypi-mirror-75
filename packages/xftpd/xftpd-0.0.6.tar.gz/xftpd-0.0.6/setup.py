import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xftpd",
    version="0.0.6",
    author="John Mapp",
    author_email="spidermonkey2012@gmail.com",
    description="XFTPD Server: SFTP and FTP server Class that can be started and stopped programmatically.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mapp-john/xftpd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['netifaces',
                      'sftpserver',
                      'pyftpdlib',
                      'paramiko',
                      'cryptography'],
    python_requires='>=3.6',
)
