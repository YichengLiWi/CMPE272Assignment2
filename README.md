### Requirements

Implement one way replicator using grpc [RocksDB]
(https://docs.google.com/drawings/d/1JEVSYzanWRfTLytnvP45IPuz9xpAf6SdlwHr0Hpjb8Q/edit)
(https://pypi.python.org/pypi/python-rocksdb).


Create a Docker image using [this example](https://github.com/sithu/cmpe273-fall17/tree/master/docker).

* Create a Docker network so that each container can connect to the host under the fixed IP 192.168.0.1.

```sh
docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet
```

* Run the server and client containers.

```sh
# Generate Stub for client and server
docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto


# Server
docker run -p 3000:3000 -it --rm --name lab1-server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 server.py

# Client
docker run -it --rm --name lab1-client -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client.py 192.168.0.1
```

### Expected Output on Client
```sh
Client is connecting to Server at 192.168.0.1:3000...
replicate
put value is b  key is  0
put value is b a key is  1
put value is b aa key is  2
delete value is  key is  0
put value is b aaa key is  3
put value is b aaaa key is  4
delete value is  key is  1
put value is b aaaaa key is  5
put value is b aaaaaa key is  6
delete value is  key is  2
[(b'\x03', b'b aaa'), (b'\x04', b'b aaaa'), (b'\x05', b'b aaaaa'), (b'\x06', b'b aaaaaa')]
```

### Expected Output on Master
```sh
Server started at...3000
master update: [(b'\x03', b'b aaa'), (b'\x04', b'b aaaa'), (b'\x05', b'b aaaaa'), (b'\x06', b'b aaaaaa')
```