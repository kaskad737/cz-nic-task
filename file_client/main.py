import requests
import argparse
import datetime
import json
import grpc
import service_file_pb2, service_file_pb2_grpc
from logging_config import dict_config
import logging
import logging.config

logging.config.dictConfig(dict_config)
file_client_logger: logging.Logger = logging.getLogger('fileClientLogger')

class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)


def rest_url_checker(url) -> str:
    '''
    Because I start a flask server on port :5000 I made It for test purposes
    '''
    return url[:-1] + ':5000' if not url.split('/')[-1] else url

def get_rest_data(url, uuid, command_type) -> str:
    '''
    Get data from rest endpoints
    '''
    if command_type:
        target_url = f'{url}/file/{uuid}/{command_type}'
        response = requests.get(url=target_url)
        if response.ok:
            return response.text
        else:
            file_client_logger.error(f'Bad request. Response code: {response.status_code}')

def get_grcp_data(url, uuid, command_type) -> str:
    '''
    Get data from grpc endpoints
    '''
    try:
        with grpc.insecure_channel(url) as channel:
            stub = service_file_pb2_grpc.FileStub(channel)
            if command_type == 'stat':
                stat_request = service_file_pb2.StatRequest(uuid={'value': uuid})
                try:
                    response = stub.stat(stat_request)
                    response = {"create_datetime": response.data.create_datetime.seconds, "size": response.data.size, "mimetype": response.data.mimetype, "name": response.data.name}
                except grpc.RpcError as e:
                    file_client_logger.error(f"Error while calling stat RPC: {e}")
            elif command_type == 'read':
                try:
                    read_request = service_file_pb2.ReadRequest(uuid={'value': uuid})
                    read_response = stub.read(read_request)
                    response = []
                    for data in read_response:
                        response.append(data)
                    response = response[0].data.data.decode()
                except grpc.RpcError as e:
                    file_client_logger.error(f"Error while calling read RPC: {e}")
            return response
    except Exception as exc:
        file_client_logger.error(f'Can\'t open connection, error - {exc}')

def get_result(data, backend_type, command_type, output, new_file_name=None) -> str:
    '''
    Returns formatted results
    '''
    if command_type == 'stat':
                data_dict = json.loads(data) if backend_type == 'rest' else data
                create_datetime = datetime.datetime.fromtimestamp(data_dict['create_datetime']).strftime("%Y-%m-%d %H:%M:%S")
                file_size = int(data_dict['size']) / (1024 ** 1)
                file_size_mb = int(data_dict['size']) / (1024 ** 2)
                mime_type = data_dict['mimetype']
                file_name = data_dict['name']
                result = f'Create datetime: {create_datetime} File size in Kilobytes: {file_size} File size in Megabytes: {file_size_mb} Mimetype: {mime_type} File name: {file_name}'
                return result
    elif command_type == 'read':
        if output == 'textfile':
            save_text_to_file(text_to_save=data, new_file_name=new_file_name)
        elif output == 'stdout':
            return data

def save_text_to_file(text_to_save, new_file_name):
    '''
    Write text to current filename.
    '''
    new_file_name = f'./{new_file_name}.txt'
    with open(new_file_name, mode='w', encoding='utf-8') as f:
        f.write(text_to_save)


def main():
    parser = argparse.ArgumentParser(add_help=False, formatter_class=CapitalisedHelpFormatter, prog='file-client')

    parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
    parser.add_argument('--backend', choices=['grpc', 'rest'], default='grpc', help='Set a backend to be used, choices are grpc and rest. Default is grpc.')
    parser.add_argument('--grpc_server_url', default='localhost:50051', help='Set a host and port of the gRPC server. Default is localhost:50051.')
    parser.add_argument('--base_url_rest', default='http://localhost/', help='Set a base URL for a REST server. Default is http://localhost/.')
    parser.add_argument('--output', choices=['textfile', 'stdout'], default='stdout', help='Set the file where to store the output. Default is - "stdout", alternative - "textfile".')
    parser.add_argument('--file-name', default='file', help='File name without extension (defaul name: "file"). The file will be saved in the same folder where you run the script.')
    parser.add_argument('command', choices=['stat', 'read'], help='"stat" - Prints the file metadata in a human-readable manner. "read" - Outputs the file content.')
    parser.add_argument('uuid', help='UUID of the file')
    parser._positionals.title = 'Positional arguments'
    parser._optionals.title = 'Optional arguments'

    args = parser.parse_args()

    if args.backend == 'rest':
            # Because I start a flask server on port :5000 I made It for test purposes
            valid_url = rest_url_checker(url=args.base_url_rest)
            data = get_rest_data(url=valid_url, uuid=args.uuid, command_type=args.command)
    if args.backend == 'grpc':
        data = get_grcp_data(url=args.grpc_server_url, uuid=args.uuid, command_type=args.command)

    result = get_result(data=data, backend_type=args.backend, command_type=args.command, new_file_name=args.file_name, output=args.output)
    if result:
        file_client_logger.info(result)

if __name__ == '__main__':
    main()


