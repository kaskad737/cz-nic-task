import sys
sys.path.append('/home/apti/cz-nic-test-task/file_client/')
from main import rest_url_checker, get_result

def test_case_1():
    
    result_one = rest_url_checker('http://localhost:5000')
    result_two = rest_url_checker('http://localhost/')

    assert result_one == 'http://localhost:5000'
    assert result_two == 'http://localhost:5000'


def test_case_2():
    MOCK_DATA = '{"create_datetime": 1701957371, "size": 1005, "mimetype": "text/plain", "name": "test_file_1.txt"}'

    r = get_result(data=MOCK_DATA, backend_type='rest', command_type='stat', output='stdout')

    test_string = 'Create datetime: 2023-12-07 13:56:11 File size in Kilobytes: 0.9814453125 File size in Megabytes: 0.0009584426879882812 Mimetype: text/plain File name: test_file_1.txt'

    assert r == test_string
