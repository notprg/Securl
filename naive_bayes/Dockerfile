FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_nb.txt /pipeline
RUN pip install -r requirements_nb.txt
COPY naive_bayes.py /pipeline