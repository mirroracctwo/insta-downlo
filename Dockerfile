FROM python:3.10

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY Requirements.txt .

RUN pip install --no-cache-dir -r Requirements.txt

COPY . .

CMD ["python","app.py"]
