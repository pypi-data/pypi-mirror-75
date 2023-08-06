import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="deep-kolibri",
    version="0.2.5.2",
    author="Mohamed Ben Haddou",
    author_email="mbenhaddou@mentis.io",
    include_package_data=True,
    description="Deep Learning and more NLP toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["tensorflow>=2.0"],
    url="",
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.json', '*.npy', '*.db'],
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
    ],
    python_requires='>=3.7',
)
