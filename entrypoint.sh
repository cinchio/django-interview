#!/bin/bash

# Wait for postgres
echo "Waiting for postgres..."
python << END
import socket
import time
import sys

port = 5432
host = "db"
start_time = time.time()

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((host, port))
        sock.close()
        break
    except (socket.error, socket.timeout):
        if time.time() - start_time > 30:
            print("Timeout waiting for postgres")
            sys.exit(1)
        time.sleep(0.1)
END

echo "PostgreSQL started"

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

exec "$@"
