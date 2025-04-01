# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add paths to the microservices
sys.path.insert(0, os.path.abspath('../../customer_microservice'))
# sys.path.insert(0, os.path.abspath('../../admin_microservice'))
# sys.path.insert(0, os.path.abspath('../../auth_microservice'))
# sys.path.insert(0, os.path.abspath('../../employee_microservice'))
# sys.path.insert(0, os.path.abspath('../../synch_microservice'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'KEA Car Microservices'
copyright = '2025, Marcus Klinke Thorsen and Oliver Roat Jørgensen'
author = 'Marcus Klinke Thorsen and Oliver Roat Jørgensen'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
]

autosummary_generate = True

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'inherited-members': True,
    'show-inheritance': True,
    'exclude-members': 'validate_created_at, validate_updated_at, name, price, logo_url, red_value, green_value, blue_value, brand, colors, image_url, accessories, insurance, models',
}

# Automatically mock external dependencies
autodoc_mock_imports = [
    # FastAPI and related libraries
    'fastapi',
    'pydantic',
    'uvicorn',

    # MongoDB and related libraries
    'pymongo',
    
    # MySQL and related libraries
    'sqlalchemy',

    # RabbitMQ and related libraries
    'pika',
    
    # PyTest and related libraries
    'pytest',

    # Environment management
    'dotenv',
]

autodoc_typehints = "none"


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**/__pycache__', '**/*.pyc', '.venv', 'venv', 'env', '.env', '/scripts']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
