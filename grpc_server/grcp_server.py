from concurrent import futures

import grpc
import service_file_pb2, service_file_pb2_grpc
from google.protobuf.json_format import MessageToJson 
from google.protobuf import timestamp_pb2
import json
import os
import mimetypes 
import datetime



MOCK_DATABASE = {
    '1': {'uuid': 1, 'file_path': './files/', 'file_name': 'test_file_1.txt'},
    '2': {'uuid': 2, 'file_path': './files/', 'file_name': 'test_file_2.txt'},
    '3': {'uuid': 3, 'file_path': './files/', 'file_name': 'test_file_3.txt'},
    '4': {'uuid': 4, 'file_path': './files/', 'file_name': 'test_file_4.txt'},
}

class FileService(service_file_pb2_grpc.FileServicer):
    def stat(self, request, context):
        '''
        Method to retrieve file data
        '''
        request_uuid = json.loads(MessageToJson(request))
        request_uuid = request_uuid['uuid']['value']
        if not isinstance(request_uuid, str):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid UUID is used')
            return service_file_pb2.Response()
        if not MOCK_DATABASE:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Can\'t connect to database')
            return service_file_pb2.Response()
        
        data_from_db = MOCK_DATABASE.get(request_uuid)

        if not data_from_db:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('File not found in DB')
            return service_file_pb2.Response()

        file_path = data_from_db['file_path'] + data_from_db['file_name']
        file_name = os.path.basename(file_path)
        create_datetime = os.path.getmtime(file_path)
        size = os.path.getsize(file_path)
        mimetype = mimetypes.guess_type(file_path)[0]

        datetime_obj = datetime.datetime.fromtimestamp(create_datetime)
        timestamp_pb = timestamp_pb2.Timestamp()
        timestamp_pb.FromDatetime(datetime_obj)

        return service_file_pb2.StatReply(data={
            'name': file_name,
            'size': size,
            'mimetype': mimetype,
            'create_datetime': timestamp_pb,
        })
        
    def read(self, request, context):
        '''
        Method to retrieve file contents
        '''
        request_uuid = json.loads(MessageToJson(request))
        request_uuid = request_uuid['uuid']['value']
        if not isinstance(request_uuid, str):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid UUID is used')
            return service_file_pb2.Response()
        if not MOCK_DATABASE:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Can\'t connect to database')
            return service_file_pb2.Response()

        data_from_db = MOCK_DATABASE.get(request_uuid)

        if not data_from_db:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('File not found in DB')
            return service_file_pb2.Response()
        
        file_path = data_from_db['file_path'] + data_from_db['file_name']
        file_name = os.path.basename(file_path)

        with open(file_path, 'r') as f:
            file_content = f.read()

        file_content_in_bytes = bytes(file_content, encoding='utf-8')

        context.set_trailing_metadata([
            ('content-disposition', file_name),
        ])

        yield service_file_pb2.ReadReply(data={
            'data': file_content_in_bytes
        })

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_file_pb2_grpc.add_FileServicer_to_server(FileService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
