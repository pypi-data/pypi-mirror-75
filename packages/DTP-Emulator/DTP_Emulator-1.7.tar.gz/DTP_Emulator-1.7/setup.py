import setuptools


with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DTP_Emulator", # Replace with your own username
    version="1.7",
    author="azson",
    author_email="240326315@qq.com",
    description="DTP emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AItransCompetition/simple_emulator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    package_data={
        '':["*txt", "*csv"]
    }
)
