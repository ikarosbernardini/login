FROM python:3.11-slim
RUN pip install flask
# Kopiera hela projektet
COPY . /app
WORKDIR /app
# Kör mitt skript.
CMD ["python", "main.py"]

