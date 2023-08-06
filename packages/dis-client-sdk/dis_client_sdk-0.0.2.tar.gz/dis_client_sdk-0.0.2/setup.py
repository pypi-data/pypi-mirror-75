import setuptools

# with open("./dis_client_sdk/README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="dis_client_sdk",
    version="0.0.2",
    author="bjyurkovich",
    author_email="bj.yurkovich@technicity.io",
    description="DIS Client SDK",
    long_description="In development...",
    long_description_content_type="text/markdown",
    url="https://github.com/bjyurkovich",
    # packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # data_files=[('api', ['path/to/files'])],
    license='MIT',
    packages=['dis_client_sdk'],
    install_requires=["requests", "pydantic"],
    include_package_data=True
)
