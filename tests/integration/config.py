"""Integration test configuration."""

import os
from os.path import dirname, join

from dotenv import load_dotenv

# Load environment variables from a .env file if present
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

QA_BASE_URL = (
    os.environ.get("QA_BASE_URL")
    or "https://qa-ows-REST-Api.theorchard.io"
)
