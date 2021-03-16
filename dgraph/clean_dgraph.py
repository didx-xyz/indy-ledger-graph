import datetime
import json

import pydgraph


# Create a client stub.
def create_client_stub():
    return pydgraph.DgraphClientStub('localhost:9080')


# Create a client.
def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


# Drop All - discard all data and start from a clean slate.
def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))

def main():
    client_stub = create_client_stub()
    client = create_client(client_stub)
    drop_all(client)

    # Close the client stub.
    client_stub.close()


if __name__ == '__main__':
    try:
        main()
        print('DONE!')
    except Exception as e:
        print('Error: {}'.format(e))
