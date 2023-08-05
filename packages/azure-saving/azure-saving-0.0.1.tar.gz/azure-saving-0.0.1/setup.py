import setuptools
import azure_saving

setuptools.setup(
    name="azure-saving",
    version=azure_saving.__version__,
    author=azure_saving.__author__,
    author_email="alessandra.bilardi@gmail.com",
    description="Azure saving Python package",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    url="https://azure-saving.readthedocs.io/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        "Source":"https://github.com/bilardi/azure-saving",
        "Bug Reports":"https://github.com/bilardi/azure-saving/issues",
        "Funding":"https://donate.pypi.org",
    },
)
