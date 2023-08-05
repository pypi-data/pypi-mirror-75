S3 CRUD client

Pre-install

```sh
export S3_ENDPOINT_URL=[s3 api compatible server]
export S3_BUCKET=[bucket name]
export S3_ACCESS_KEY_ID=[s3 key id]
export S3_SECRET_ACCESS_KEY=[s3 secret key]
```

Usage
```sh
pip3 install s3-talenttech-oss
```

```python
from s3.client import Client

client = Client()

client.create_dir('dir')

client.create_file('dir/file.txt', 'qwerty')

content = client.read_file('dir/file.txt')

client.create_file('dir/file_another.txt', 'qwerty')

lst = client.bulk_read('dir')

print(lst)
>>> ['qwerty', 'qwerty']

client.delete_dir('dir')
```