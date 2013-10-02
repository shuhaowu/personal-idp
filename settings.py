import os
DEBUG = os.environ.get("DEBUG", False)
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = os.environ.get("PORT", 8999)
DOMAIN = os.environ.get("DOMAIN")

SECRET_KEY = os.environ.get("SECRET_KEY", "setsomething")

if DOMAIN is None:
  raise RuntimeError("DOMAIN setting not set!")

