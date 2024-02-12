FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_sgd.txt /pipeline
RUN pip install -r requirements_sgd.txt
COPY sgd.py /pipeline