FROM python:3.9

RUN mkdir /flask_server

COPY requirements.txt /flask_server/
COPY files/ /flask_server/files/
COPY app.py /flask_server/

RUN python -m pip install -r /flask_server/requirements.txt

WORKDIR /flask_server

ENTRYPOINT ["python", "app.py"]
