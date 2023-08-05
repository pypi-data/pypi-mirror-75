import setuptools
import gcp_saving

setuptools.setup(
    name="gcp-saving",
    version=gcp_saving.__version__,
    author=gcp_saving.__author__,
    author_email="alessandra.bilardi@gmail.com",
    description="GCP saving Python package",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    url="https://gcp-saving.readthedocs.io/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        "Source":"https://github.com/bilardi/gcp-saving",
        "Bug Reports":"https://github.com/bilardi/gcp-saving/issues",
        "Funding":"https://donate.pypi.org",
    },
)
