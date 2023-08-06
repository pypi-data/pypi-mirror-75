import os

try:
    configs = {
        "database": os.environ['PGDATABASE'],
        "user": os.environ['PGUSER'],
        "host": os.environ['PGHOST'],
        "password": os.environ['PGPASSWORD']
    }
except Exception as e:
    raise ConnectionError(
        e, "Environment Variables Not Found.\n Is `railway run` wrapping the command?")
