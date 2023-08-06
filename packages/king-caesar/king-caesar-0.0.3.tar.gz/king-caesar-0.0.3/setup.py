import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name="king-caesar",
    version="0.0.3",
    author="Murilo Amais Bracero",
    author_email="murilobracero@gmail.com",
    description="video thumbnails generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/murilo-bracero/generate_thumbnail",
    packages=['generate_thumbnail'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='generator generate thumbnail',
    license='MIT',
    install_requires=['opencv-python', 'imageio'],
    include_package_data=True,
    zip_safe=False
)