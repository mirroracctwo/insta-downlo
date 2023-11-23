FROM python:3.10

COPY Requirements.txt .

RUN pip install --no-cache-dir -r Requirements.txt

COPY . .

CMD ["Python","app.py"]
