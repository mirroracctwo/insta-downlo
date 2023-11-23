FROM python:3.10-alpine

COPY Requirements.txt .

RUN pip install --no-cache-dir -r Requirements.txt

COPY . .

CMD ["Python","app.py"]