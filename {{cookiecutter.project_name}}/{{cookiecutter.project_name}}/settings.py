"""
Settings held within this file are gathered from Environment variables
"""

import os
import re

# Production mode is set by having any value in the `MODE` env variable
PRODUCTION = bool(os.environ.get("PRODUCTION", ""))

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))

# Cryptography -
# The secret passed must be a sha256 length string.
SECRET = os.environ.get("SECRET")
if SECRET is None:
    raise EnvironmentError("Missing Environment Variable: SECRET")
elif re.match('/^[a-f0-9]{64}$/gi', SECRET):
    raise EnvironmentError("Environment Variable SECRET is not a valid SHA256 string")

# JWT Algorithm
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_DURATION_MINUTES = int(os.environ.get("JWT_DURATION_MINUTE", "30"))

# Database
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "password")
