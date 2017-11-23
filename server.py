'''
################################## server.py #############################
# Lab1 gRPC RocksDB Server 
################################## server.py #############################
'''
import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
import uuid
import rocksdb

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        self.db = rocksdb.DB("master.db", rocksdb.Options(create_if_missing=True))

    #replicator function
    def masterUpdate(self, request, context):
        print("master update: ")
        delete_key= 0
        put_key = 0
        key = 0
        put_value="b "
        
        # add behaviors(put/delete) every 3 seconds
        for i in range (10):
            if (i % 3 != 0) | (i == 0):
                command = "put"
                value = put_value
                key = put_key
                put_key += 1
                put_value += 'a'
                self.db.put(chr(key).encode(), value.encode())
            if (i % 3 == 0) & (i != 0):
                command = "delete"
                value = ""
                key = delete_key
                delete_key += 1
                self.db.delete(chr(key).encode())
            yield datastore_pb2.Response(cmd=command,key=key,value=value)
            time.sleep(3)

        it = self.db.iteritems()
        it.seek_to_first()

        # prints [(b'key1', b'v1'), (b'key2, b'v2'), (b'key3', b'v3')]
        print(list(it))

def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    myServer = MyDatastoreServicer()
    datastore_pb2_grpc.add_DatastoreServicer_to_server(myServer, server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)
