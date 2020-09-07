FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /portal
WORKDIR /portal
ADD . /portal/
RUN pip install --upgrade pip && pip install -r requirements.txt