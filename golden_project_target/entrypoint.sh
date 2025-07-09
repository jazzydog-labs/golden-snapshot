#!/bin/bash
set -e

echo "Starting entrypoint script..."
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Remove blog.db if it's a directory
if [ -d "/app/blog.db" ]; then
    echo "Removing blog.db directory..."
    rm -rf /app/blog.db
fi

# Ensure the database file can be created
echo "Creating database file..."
touch /app/blog.db
chmod 666 /app/blog.db
echo "Database file created"

# Start the application
echo "Starting uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000