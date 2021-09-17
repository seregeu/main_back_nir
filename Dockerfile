FROM python:3.8

ENV PYTHONUNBUFFERED 1

USER root

WORKDIR /home/root
COPY . .

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY entrypoint.sh .


ENTRYPOINT ["sh", "/home/root/entrypoint.sh"]
