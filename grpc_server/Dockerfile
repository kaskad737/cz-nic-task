FROM python:3.9

RUN mkdir /grpc_server

COPY requirements.txt /grpc_server/
COPY files/ /grpc_server/files/
COPY grpc_server.py /grpc_server/
COPY service_file_pb2_grpc.py /grpc_server/
COPY service_file_pb2.py /grpc_server/
COPY service_file_pb2.pyi /grpc_server/

RUN python -m pip install -r /grpc_server/requirements.txt

WORKDIR /grpc_server

ENTRYPOINT ["python", "grpc_server.py"]