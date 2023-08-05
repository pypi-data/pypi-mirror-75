import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BDSExcelDriver", # Replace with your own username
    version="0.0.6",
    author="kinhnv",
    author_email="kinhnv1801@gmail.com.vn",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.batdongsan.com.vn/DuongNT4/MSV_Batdongsan_Automation_Testing",
    packages=setuptools.find_packages(),
    install_requires=[
        'openpyxl',
        'robot',
        'SeleniumLibrary'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)