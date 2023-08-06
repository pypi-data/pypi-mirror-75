"""
Python module to initialize Server Extension for Rubin Observatory JupyterHub
interaction.
"""
from .handlers import setup_handlers


def _jupyter_server_extension_paths():
    """
    Function to declare Jupyter Server Extension Paths.
    """
    return [{"module": "jupyterlab_rubinhub",}]


def load_jupyter_server_extension(nbapp):
    """
    Function to load Jupyter Server Extension.
    """
    nbapp.log.info("Loading rubinhub server extension.")
    setup_handlers(nbapp.web_app)
