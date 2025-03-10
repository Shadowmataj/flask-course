FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["/bin/bash", "docker-entrypoint.sh"]