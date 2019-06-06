FROM python:3.6-slim

WORKDIR /app

COPY requirements.txt /app

RUN python3 -m pip install -U discord.py
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "src/main.py"]