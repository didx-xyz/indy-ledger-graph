import datetime
import json

import pydgraph

from tinydb import TinyDB, Query as DbQuery
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb_smartcache import SmartCacheTable

TinyDB.table_class = SmartCacheTable
db = TinyDB('../ledger_data/indy_mainnet_tinydb.json'
            '', storage=CachingMiddleware(JSONStorage))

# Create a client stub.
def create_client_stub():
    return pydgraph.DgraphClientStub('localhost:9080')


# Create a client.
def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


# Drop All - discard all data and start from a clean slate.
def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))

def resolve_txn_type(item):
    txn_type_int = item["data"]["txn"]["type"]

    if txn_type_int == '1':
        txn_type = 'NYM'
    elif txn_type_int == '100':
        txn_type = 'ATTRIB'
    elif txn_type_int == '101':
        txn_type = 'SCHEMA'
    elif txn_type_int == '102':
        txn_type = 'CLAIM_DEF'
    elif txn_type_int == '113':
        txn_type = 'REVOC_REG_DEF'
    elif txn_type_int == '114':
        txn_type = 'REVOC_REG_ENTRY'
    elif txn_type_int == '200':
        txn_type = 'SET_CONTEXT'
    elif txn_type_int == '0':
        txn_type = 'NODE'
    elif txn_type_int == '10':
        txn_type = 'POOL_UPGRADE'
    elif txn_type_int == '11':
        txn_type = 'NODE_UPGRADE'
    elif txn_type_int == '11':
        txn_type = 'POOL_CONFIG'
    elif txn_type_int == '12':
        txn_type = 'AUTH_RULE'
    elif txn_type_int == '12':
        txn_type = 'AUTH_RULES'
    elif txn_type_int == '4':
        txn_type = 'TXN_AUTHOR_AGREEMENT'
    elif txn_type_int == '5':
        txn_type = 'TXN_AUTHOR_AGREEMENT_AML'
    elif txn_type_int == '20000':
        txn_type = 'SET_FEES'
    else:
        txn_type = 'ERROR'

    return txn_type

def resolve_txn_time(item):
    if 'txnTime' in item["data"]["txnMetadata"]:
        txn_time_epoch = item["data"]["txnMetadata"]["txnTime"]
        return str(datetime.datetime.fromtimestamp(txn_time_epoch))
    else:
        return None

def resolve_endorser(item):
    # print("ENDORSER METADATA", parent["data"]["txn"]["metadata"])
    if 'endorser' in item["data"]["txn"]["metadata"]:
        endorser = item["data"]["txn"]["metadata"]["endorser"]

        TXN = DbQuery()
        return db.get((TXN['data']['txn']['data']['dest'] == endorser))
    else:
        return None
    # elif 'from' in item["data"]["txn"]["metadata"]:
    #     TXN = DbQuery()
    #     from_did = item["data"]["txn"]["metadata"]['from']
    #     # print(from_did)
    #     return db.get((TXN['data']['txn']['data']['dest'] == from_did) & (TXN['data']['txn']['type'] == "1"))

def resolve_author(item):
    if 'from' in item["data"]["txn"]["metadata"]:
        TXN = DbQuery()
        from_did = item["data"]["txn"]["metadata"]['from']
        # print(from_did)
        return db.get((TXN['data']['txn']['data']['dest'] == from_did) & (TXN['data']['txn']['type'] == "1"))
    else:
        return None

# Create data using JSON.
"""
type AddDIDInput {
seqNo: String!
type: String!
time: String!
endorser: DIDRef
author: DIDRef!
did: String!
verkey: String!
role: String
alias: String
attribs: [AttributeRef]!
authoredDefinitions: [CredDefRef]!
authoredSchema: [SchemaRef]!
authoredDids: [DIDRef]!
endorsedDefinitions: [CredDefRef]!
endorsedSchema: [SchemaRef]!
endorsedDids: [DIDRef]!
}
"""

def create_data(client):
    # Create a new transaction.
    print('in create data')
    txn = client.txn()
    # Create data.
    items = db.all()[100:105]
    for item in items:
        # print(type(item))
        # print(item)
        try:
            json_payload = {
                'dgraph.type': 'AddDIDInput',
                'seqNo': item['seqNo'],
                'type': resolve_txn_type(item),
                'time': resolve_txn_time(item),
                'endorser': '',
                'author': [{}],
                'did': item['data']['txn']['data']['dest'],
                'verkey': '',
                # 'verkey': item['data']['txn']['data']["verkey"],
                'role': '',
                # 'role': item['data']['txn']['data']['role'],
                'alias': '',
                # 'alias': item['data']['txn']['data']['alias'],
                'attribs': [],
                'authoredDefinitions': [],
                'authoredSchema': [],
                'authoredDids': [],
                'endorsedDefinitions': [],
                'endorsedSchema': [],
                'endorsedDids': [],
            }
            # p = {
            #     'uid': '_:seqNo',
            #     'dgraph.type': 'Transaction',
            #     'seqNo': seqNo,
            #     'type': type,
            #     'time': time,
            #     'endorser': [
            #         {
            #             'uid': '_:seqNo',
            #             'dgraph.type': 'DID',
            #             'endorser': endorser,
            #         }
            #     ],
            #     'author': [
            #         {
            #             'uid': '_:seqNo',
            #             'dgraph.type': 'DID',
            #             'author': author,
            #         }
            #     ],
            # }

            print('JSON UPDATE IS',json_payload)

            # Run mutation.
            response = txn.mutate(set_obj=json_payload)
            # print('response is', response)
            # Commit transaction.
            txn.commit()

            # Get uid of the outermost object (person named "Alice").
            # response.uids returns a map from blank node names to uids.
            print('Created Transaction with uid = {}'.format(response.uids['seqNo']))

        finally:
            # Clean up. Calling this after txn.commit() is a no-op and hence safe.
            # print('discarding tx')
            txn.discard()

def main():
    client_stub = create_client_stub()
    client = create_client(client_stub)
    # drop_all(client)
    create_data(client)

    # Close the client stub.
    client_stub.close()


if __name__ == '__main__':
    # try:
        main()
        print('DONE!')
    # except Exception as e:
        # pass
        # print('Error: {}'.format(e))