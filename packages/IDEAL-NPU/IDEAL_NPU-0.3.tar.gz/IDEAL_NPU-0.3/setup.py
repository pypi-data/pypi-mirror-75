import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IDEAL_NPU",
    version="0.3",
    author="Shenfei Pei",
    author_email="shenfeipei@gmail.com",
    description="A Python module for machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShenfeiPei/IDEAL",
    packages=setuptools.find_packages(),
    install_requires=['numpy==1.16.5'],
    package_data={'IDEAL_NPU': ['Funs/data/Agg.mat', 'cluster/_edg.dll']},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        'Operating System :: Microsoft :: Windows',
    ],
)
