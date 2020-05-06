# Enable Development Env

DEBUG = True

# Application Directory

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Example DB Configuration

SQLALCHEMY_DATABASE_URI = ''
DATABASE_CONNECT_OPTIONS = {}

TEMPLATES_AUTO_RELOAD = True

# Application threads. Common assumption is
# to use 2 threads per available core.
# Handles incoming requests using one and 
# performs background operations on other.

THREADS_PER_PAGE = 2

# CSRF

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'something'

# Key for cookies

SECRET_KEY = 'D@rKkn!ghtR!$e$'
BASE_URI = 'http://gen.lib.rus.ec/'
SEARCH_URI = '{}search.php?req={}&open=0&res=100&view=detailed&phrase=1&column=def'