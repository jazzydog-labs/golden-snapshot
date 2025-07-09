FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod -R 777 /app

EXPOSE 8000

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]