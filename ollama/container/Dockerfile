FROM docker.io/ollama/ollama:latest

# create unprivileged user
RUN useradd -m -u 1001 ollamauser

# create model directory
RUN mkdir -p /home/ollamauser/.ollama /models && \
    chown -R ollamauser:ollamauser /home/ollamauser /models

# copy startup script
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

USER ollamauser

ENV OLLAMA_MODELS=/models
ENV OLLAMA_HOST=0.0.0.0:11434
ENV OLLAMA_NUM_THREADS=6

ENTRYPOINT ["/usr/local/bin/start.sh"]

