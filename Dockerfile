FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src

ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 8080

CMD ["python", "/src/main.py"]
