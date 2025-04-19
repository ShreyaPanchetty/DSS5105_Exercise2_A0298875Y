FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000

CMD ["python", "app.py"]
CMD [curl "http://localhost:7000/predict?W=1&X=20"]
CMD [curl "http://localhost:7000/ate"]
