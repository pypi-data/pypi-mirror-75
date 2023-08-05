from setuptools import setup, find_packages
import jcopvision

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="jcopvision",
    version=jcopvision.__version__,
    author="Wira Dharma Kencana Putra",
    author_email="wiradharma_kencanaputra@yahoo.com",
    description="J.COp Vision consists of helper tools for computer vision",
    long_description=description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6.7",
    install_requires=["opencv-python", "numpy"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Natural Language :: Indonesian",
        "Natural Language :: English"
    ],
    keywords="computer vision dl jcop indonesia",
    url="https://github.com/WiraDKP/jcopvision"
)