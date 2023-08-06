"""
Setup Module to set up Python handlers for Rubin Observatory Science Platform
interaction with JupyterHub.
"""
import setuptools

setuptools.setup(
    name="jupyterlab_lsstquery",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=["notebook", "requests"],
    package_data={"jupyterlab_rubinhub": ["*"]},
)
