# cz-nic-test-task

## File client task

How to instal and use:
1. Copy this repository to your folder ```git clone ...```.
2. Then create a virtual environment and install the required packages and dependencies.
    - Go to folder with script ```/file_client/``` then create some venv ```python -m venv .env```.
    - Next, activate your virtual environment and install the dependencies from the folder ```/file_client/``` like this ```pip install -r requirements.txt``` - now you're ready to run the script.
3. Examples of use:
    - Basic use - (```python main.py --backend grpc --grpc_server_url your_address:50051 stat 1```) or in you want read the hole file - ```python main.py --backend grpc --grpc_server_url your_address:50051 read 1```\
    In this example, we are accessing the grpc server.

    - You can also query the rest api:
    If you want to see file specifications:\
    ```python main.py --backend rest --base_url_rest http://your_address/ stat 1```\
    Or if you want to read the file:\
    ```python main.py --backend rest --base_url_rest http://your_address/ read 1```

     - It is also possible to download the contents of the file to yourself locally:\
    gRPC:\
    ```python main.py --backend grpc --grpc_server_url your_address:50051 --output textfile --file-name text_file_name read 1```\
    REST:\
    ```python main.py --backend rest --base_url_rest http://your_address/ --output textfile --file-name text_file_name read 1```

4. More info you can get of you type: ```python main.py --help```

## How to run tests

You can run the tests like this:
1. With the virtual environment enabled, go to the folder ```/file_client/test/``` and run the following command: ```pytest test_file_client.py``` and that's it.

    - P.S.: ```sys.path.append('/home/apti/cz-nic-test-task/file_client/')``` - don't forget to change the path here to make the import work correctly.

## About data you can access

```
MOCK_DATABASE = {
    '1': {'uuid': 1, 'file_path': './files/', 'file_name': 'test_file_1.txt'},
    '2': {'uuid': 2, 'file_path': './files/', 'file_name': 'test_file_2.txt'},
    '3': {'uuid': 3, 'file_path': './files/', 'file_name': 'test_file_3.txt'},
    '4': {'uuid': 4, 'file_path': './files/', 'file_name': 'test_file_4.txt'},
}
```
# ATTENTION !!!!!
__Files are located locally on the server and in order not to raise a separate database with data about files, I created a mock database. As you can see, we have only four files on the server and in the database, so requests can be made only for them__


---

## SQL task

Solution you can find in ```/sql_task/tasl_solution.sql```

Function with trigger ```check_value_is_boolean_function()``` triggers on insert ```domain``` table and check the flags on the insert don't equal the TRUE.

Function with trigger ```update_domain_table_function()``` triggers on update ```domain``` table, and make record to ```domain_flag``` table with ```valid_from``` field and blank ```valid_to``` field.

If we change a flag on FALSE in the table ```domain```, the trigger will be triggered and in the table ```domain_flag``` in field ```valid_to``` we'll have the date and time when the flag stopped working.

For one record in ```domain``` at a time, there can be no duplicate flag in ```domain_flag```


First insert data:
```sql
INSERT INTO domain(domain_name) VALUES ('google.com');
INSERT INTO domain(domain_name) VALUES ('seznam.cz');
INSERT INTO domain(domain_name) VALUES ('posta.ua');
```
TEST CASES:
```sql
INSERT INTO domain(domain_name, expired) VALUES ('yahoo.com', TRUE);
INSERT INTO domain(domain_name, outzone) VALUES ('yahoo.com', TRUE);
INSERT INTO domain(domain_name, delete_candidate) VALUES ('yahoo.com', TRUE);
INSERT INTO domain(domain_name, expired, outzone, delete_candidate) VALUES ('yahoo.com', TRUE, TRUE, TRUE);
INSERT INTO domain(domain_name, expired, outzone, delete_candidate) VALUES ('yahoo.com', TRUE, FALSE, TRUE);
```
Will return error because of constrait. We can't INSERT record in ```domain``` table with already TRUE flags.

---

But if we update table ```domain```, flag will automaticaly appear in ```domain_flag``` table
Examples of use:
```sql
UPDATE domain SET expired=TRUE WHERE domain_name='google.com';
UPDATE domain SET outzone=TRUE WHERE domain_name='google.com';
UPDATE domain SET delete_candidate=TRUE WHERE domain_name='google.com';

UPDATE domain SET expired=FALSE WHERE domain_name='google.com';
UPDATE domain SET outzone=FALSE WHERE domain_name='google.com';
UPDATE domain SET delete_candidate=FALSE WHERE domain_name='google.com';
```

---
