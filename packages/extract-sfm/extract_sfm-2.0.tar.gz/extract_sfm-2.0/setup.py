import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extract_sfm", # Replace with your own username
    version="2.0",
    author="Yueen Ma",
    # author_email="author@example.com",
    description="Knowledge Graph Extraction for SFM dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Panmani/KGE",
    packages=setuptools.find_packages(),
    package_data={'': ['results/*', 'results/scores/*', 'results/scores/*', 'results/model/*',\
                'SFM_STARTER/*', \
                'jPTDP/*', 'jPTDP/utils/*', 'jPTDP/sample/*']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'tensorflow',
        'tensorflow-addons',
        'spacy',
        'dynet',
        'pathlib',
    ]
)
