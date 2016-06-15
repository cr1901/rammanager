# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding


setup(
    name="rammanager",
    version=1,
    description="SNES Ram Variable Database/Frontend",
    author="William D. Jones",
    author_email="thor0505@comcast.net",
    license="BSD",
    packages=["rammanager"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        ],
    include_package_data=True,
    install_requires=["tinydb", "flask"],
    zip_safe=False
)
