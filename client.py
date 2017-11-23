'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2
import argparse
import rocksdb

PORT = 3000

class DatastoreClient():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)
        self.db = rocksdb.DB("client.db", rocksdb.Options(create_if_missing=True))
    
    def masterUpdate(self):
        return self.stub.masterUpdate(datastore_pb2.Request()) 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = DatastoreClient(host=args.host)

    #get a stream of commands from service    
    print("## replicate")
    resps = client.masterUpdate()

    #replicate slave database
    for resp in resps:
        command = resp.cmd
        key = resp.key
        value = resp.value
        print(command + " value is " + value + " key is ", resp.key)
        if (command == "put"):
            client.db.put(chr(key).encode(), value.encode())
        else:
            client.db.delete(chr(key).encode())

    #print the key-value in client database
    it = client.db.iteritems()
    it.seek_to_first()

        # prints [(b'key1', b'v1'), (b'key2, b'v2'), (b'key3', b'v3')]
    print(list(it))
#    curCounter = 0
#    while True:
#        print("##Match Counter Request: client counter = ", curCounter)
#        resp = client.matchCounter(curCounter)
#        serviceCounter = resp.counter
 #       print("##Match Counter Response: service counter = ", serviceCounter)
        # if serviceCounter != curCounter:
        #     curCounter+=1
        #     print("service counter = ", serviceCounter)
        #     print("update client counter = ", curCounter)

if __name__ == "__main__":
    main()

