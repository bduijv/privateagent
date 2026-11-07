FROM python:3.11-slim-bookworm

# Prevent Python from writing bytecode and buffer delays in logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create an unprivileged executor user.
RUN groupadd --gid 1001 executor && \
    useradd --uid 1001 --gid 1001 --create-home executor

WORKDIR /app

# Install the API dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the executor application.
COPY --chown=executor:executor server.py .

# Run without root privileges.
USER 1001:1001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
