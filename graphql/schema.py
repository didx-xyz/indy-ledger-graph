from graphene import String, ObjectType, List, Field, Int, ID, Boolean, Interface, Schema as GqSchema, relay, DateTime
from tinydb import TinyDB, Query as DbQuery
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb_smartcache import SmartCacheTable

import datetime
import json

from promise import Promise
from promise.dataloader import DataLoader

class SchemabytxIDLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        TXN = DbQuery()
        result = db.get(TXN["data"]["txnMetadata"]["txnId"] == keys)
        return Promise.resolve([result for key in keys])

schemabytxid_loader = SchemabytxIDLoader()

schemabytxid_loader.load(1).then(lambda schemabytxid: schemabytxid_loader.load(Schema.id))

class SchemabyseqNoLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        TXN = DbQuery()
        result = db.get(TXN["seqNo"] == keys[0])
        return Promise.resolve([result for key in keys])

schemabyseqno_loader = SchemabyseqNoLoader()

schemabyseqno_loader.load(1).then(lambda schemabyseqno: schemabyseqno_loader.load(Schema.id))

class DefinitionsbySchemaLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # schemas = {schema.id: schema for schema in schema.objects.filter(id__in=keys)}
        TXN = DbQuery()
        print('defintions loader')
        print(keys)
        schema_txn = db.get(TXN["data"]["txnMetadata"]["txnId"] == keys[0])
        print(schema_txn)
        cred_def_txns = db.search(TXN["data"]["txn"]["data"]["ref"] == schema_txn["seqNo"])
        print(cred_def_txns)

        return Promise.resolve([cred_def_txns(id=key) for key in keys])

definitions_by_schema_loader = DefinitionsbySchemaLoader()
definitions_by_schema_loader.load(1).then(lambda definitions_by_schema_loader: definitions_by_schema_loader.load(Schema.id))

class DefinitionsbySeqNoLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # schemas = {schema.id: schema for schema in schema.objects.filter(id__in=keys)}
        # print('defs loader1')
        TXN = DbQuery()
        # def_txns = db.search((TXN['data']['txn']['type'] == "101"))
        # print(def_txns)
        def_txns = db.search((TXN["data"]["txnMetadata"]["txnId"] == keys))
        return Promise.resolve([def_txns for key in keys])

definitionsbyseqno_loader = DefinitionsbySeqNoLoader()
definitionsbyseqno_loader.load(1).then(lambda definitionsbyseqno: definitionsbyseqno_loader.load(Transaction.seqNo))

class DefinitionsLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # schemas = {schema.id: schema for schema in schema.objects.filter(id__in=keys)}
        # print('defs loader1')
        TXN = DbQuery()
        # def_txns = db.search((TXN['data']['txn']['type'] == "101"))
        # print(def_txns)
        def_txns = db.search((TXN['data']['txn']['type'] == keys))
        return Promise.resolve([def_txns for key in keys])

definitions_loader = DefinitionsLoader()
definitions_loader.load(1).then(lambda definitions: definitions_loader.load(Schema.id))

class TXByIDLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # schemas = {schema.id: schema for schema in schema.objects.filter(id__in=keys)}
        print('txbyid loader loaded')
        TXN = DbQuery()
        # print(keys[0])
        tx =  db.get(TXN['seqNo'] == keys[0])
        # print(tx)
        return Promise.resolve([tx for key in keys])

txbyid_loader = TXByIDLoader()
txbyid_loader.load(1).then(lambda txbyid: txbyid_loader.load())

class TXLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # schemas = {schema.id: schema for schema in schema.objects.filter(id__in=keys)}
        print('tx loader loaded')
        TXN = DbQuery()
        print(keys)
        if keys[0] == 1:
            # return db.all()
            # return Promise.resolve([db.all() for key in keys])
            return Promise.resolve([db.all()])
        else:
            result = db.search(TXN["data"]["txn"]["metadata"]['from'] == keys)
            # print(tx)
            return Promise.resolve([result for key in keys])

tx_loader = TXLoader()
tx_loader.load(1).then(lambda tx: tx_loader.load())

class DIDLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # schemas = {schema.id: schema for schema in schema.objects.filter(id__in=keys)}
        print('did loader loaded')
        TXN = DbQuery()
        print(len(keys))
        if len(keys) == 1:
            print('one key',keys[0])
            result = db.get((TXN['data']['txn']['data']['dest'] == keys[0]) & (TXN['data']['txn']['type'] == "1"))
            # print(result)
        else:
            print('two keys',keys)
            result = db.search((TXN['data']['txn']['data']['dest'] == keys) & (TXN['data']['txn']['type'] == "1"))
            # print(result)

        return Promise.resolve([result for key in keys])

did_loader = DIDLoader()
did_loader.load(1).then(lambda did: did_loader.load(Query.did))

class CreatedDIDLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # schemas = {schema.id: schema for schema in schema.objects.filter(id__in=keys)}
        print('createdid data loader')
        TXN = DbQuery()
        print(keys)
        result = db.search((TXN['data']['txn']['data']['from'] == keys[0]) & (TXN['data']['txn']['type'] == "1"))
        return Promise.resolve([result for key in keys])

createddid_loader = CreatedDIDLoader()
createddid_loader.load(1).then(lambda createddid: createddid_loader.load(Query.did))


class EndorserDIDLoader(DataLoader):
    def batch_load_fn(self, keys):
        # Here we return a promise that will result on the
        # corresponding user for each key in keys
        # schemas = {schema.id: schema for schema in schema.objects.filter(id__in=keys)}
        print('jouma')
        print('did loader loaded')
        print('keylen ',len(keys))
        TXN = DbQuery()
        if len(keys) == 1:
            print('Keys 1=',keys)
            result = db.get((TXN["data"]["txn"]["metadata"]["endorser"] == keys[0]))
            print(result)
        else:
            print(keys)
            result = db.search((TXN["data"]["txn"]["metadata"]["endorser"] == keys))
        return Promise.resolve([result for key in keys])

endorserdid_loader = EndorserDIDLoader()
endorserdid_loader.load(1).then(lambda endorserdid: endorserdid_loader.load(Transaction.endorser))

TinyDB.table_class = SmartCacheTable
db = TinyDB('../ledger_data/indy_mainnet_tinydb.json'
            '', storage=CachingMiddleware(JSONStorage))

class Transaction(Interface):
    class Meta:
        interfaces = (relay.Node, )
    seqNo = ID(required=True)
    reqId = String(required=True)
    txn_type = String()
    endorser = Field(lambda: DID)
    author = Field(lambda: DID)
    txn_time = DateTime()


    def resolve_txn_type(parent, info):
        # return parent["data"]["txn"]["meta"]
        txn_type_int = parent["data"]["txn"]["type"]

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

    @classmethod
    def resolve_type(cls, instance, info):
        type = instance["data"]["txn"]["type"]

        if type == "1":
            return DID
        elif type == "100":
            return Attribute
        elif type == "101":
            return Schema
        elif type == "102":
            return CredDef
        else:
            return BaseTxn

    def resolve_endorser(parent, info):
        # fp = open('test.json', 'a+')
        # fp.write(json.dumps(parent["data"]["txn"]["metadata"]))
        # fp.close()
        if 'endorser' in parent["data"]["txn"]["metadata"]:
            endorser = parent["data"]["txn"]["metadata"]["endorser"]
            # print(endorser)
            # print("Endorser DID", endorser)
            # print('did loader resolve_endorser1')
            if endorser == None:
                print('endorser == None')
                pass
            else:
                # print('endorser is',endorser)
                try:
                    # return CreatedDIDLoader.load(endorser)
                    return EndorserDIDLoader.load('Uvb86cUzmdgZ8AfbN176tc')
                except:
                    # print('fokkit',endorser)
                    # return EndorserDIDLoader.load('Uvb86cUzmdgZ8AfbN176tc')
                    return None
            # return DIDLoader.load(endorser)
            # TXN = DbQuery()
            #
            # return db.get((TXN['data']['txn']['data']['dest'] == endorser))

        # elif 'from' in parent["data"]["txn"]["metadata"]:
        #         # TXN = DbQuery()
        #         # print(parent["data"])
        #         # print(parent["data"]["txn"]["metadata"])
        #         print('parent',parent)
        #         from_did = parent["data"]["txn"]["metadata"]['from']
        #         print('from_did',from_did)
        #         # print(from_did)
        #         print('did loader resolve_endorser2')
        #         test = did_loader.load(from_did)
        #         print(test)
        #         return test
        #         # return did_loader.load(from_did)
        #         # return db.get((TXN['data']['txn']['data']['dest'] == from_did) & (TXN['data']['txn']['type'] == "1"))
        # else:
        #     # TXN = DbQuery()
        #     # print(parent["data"])
        #     # print(parent["data"]["txn"]["metadata"])
        #     print('parent', parent)
        #     dest_did = parent["data"]["txn"]["data"]['dest']
        #     print('from_did', dest_did)
        #     # print(from_did)
        #     print('did loader resolve_endorser2')
        #     test = did_loader.load(dest_did)
        #     print(test)
        #     return test
        #     # return did_loader.load(from_did)
        #     # return db.get((TXN['data']['txn']['data']['dest'] == from_did) & (TXN['data']['txn']['type'] == "1"))

    def resolve_author(parent, info):
        if 'from' in parent["data"]["txn"]["metadata"]:
            TXN = DbQuery()
            from_did = parent["data"]["txn"]["metadata"]['from']
            # print(from_did)
            # print('did loader resolve_author')
            return did_loader.load(from_did)
            # return db.get((TXN['data']['txn']['data']['dest'] == from_did) & (TXN['data']['txn']['type'] == "1"))
        else:
            return None

    def resolve_txn_time(parent, info):
        if 'txnTime' in parent["data"]["txnMetadata"]:
            txn_time_epoch = parent["data"]["txnMetadata"]["txnTime"]
            return datetime.datetime.fromtimestamp(txn_time_epoch)
        else:
            return None

class TransactionConnection(relay.Connection):
    class Meta:
        node = Transaction
    count = Int()

    def resolve_count(root, info):
        return len(root.edges)

class Attribute(ObjectType):
    class Meta:
        interfaces = (relay.Node, Transaction)
    endpoint = String()
    raw = String()
    did = Field(lambda : DID)
    # attrib_txn = Field(lambda: AttribTxn)

    def resolve_did(parent, info):
        print('did loader resolve_did_attrib')
        return did_loader.load(parent["dest"])
        # TXN = DbQuery()
        # result = db.get((TXN['data']['txn']['data']['dest'] == parent["dest"]) & (TXN['data']['txn']['type'] == "1"))
        # return result['data']['txn']['data']

    def resolve_raw(parent, info):
        try:
            return parent["data"]["txn"]["data"]["dest"]["raw"]
        except:
            return None

    def resolve_endpoint(parent, info):
        if "endpoint" in parent["data"]["txn"]["data"]["dest"]:
            return parent["data"]["txn"]["data"]["dest"]["endpoint"]
        else:
            return None

    # def resolve_attrib_txn(parent, info):
    #     TXN = DbQuery()
    #     return db.get(TXN["seqNo"] == parent["seqNo"])

class AttributeConnection(relay.Connection):
    class Meta:
        node = Attribute
    count = Int()

    def resolve_count(root, info):
        return len(root.edges)

class CredDef(ObjectType):
    class Meta:
        interfaces = (relay.Node, Transaction)
    id = ID(required=True)
    ## TODO Maybe model the crypto
    # primary = List(String)
    # revocation = List(String)

    is_revocable = Boolean()

    schema = Field(lambda : Schema)

    def resolve_id(parent, info):
        return parent["data"]["txnMetadata"]["txnId"]


    def resolve_is_revocable(parent, info):
        # print(parent["revocation"])
        return "revocation" in parent["data"]["txn"]["data"]["data"]

    def resolve_schema(parent, info):
        print('schemabyseqno loader resolve')
        return schemabyseqno_loader.load(parent["data"]["txn"]["data"]["ref"])
        # TXN = DbQuery()
        # schema_txn = db.get(TXN["seqNo"] == parent["data"]["txn"]["data"]["ref"])
        # return schema_txn

class CredDefConnection(relay.Connection):
    class Meta:
        node = CredDef

    count = Int()
    def resolve_count(root, info):
        return len(root.edges)

class Schema(ObjectType):
    class Meta:
        interfaces = (relay.Node, Transaction)
    id = ID(required=True)
    # schema_txn = Field(lambda : SchemaTxn)
    attr_names = List(String)
    name = String(required=True)
    version = String(required=True)

    definitions = relay.ConnectionField(CredDefConnection)

    definitions_count = Int()

    # def resolve_schema_txn(parent, info):
    #     TXN = DbQuery()
    #     return db.get(TXN["data"]["txnMetadata"]["txnId"] == parent["id"])

    def resolve_id(parent, info):
        return parent["data"]["txnMetadata"]["txnId"]

    def resolve_name(parent, info):
        return parent["data"]["txn"]["data"]["data"]["name"]

    def resolve_version(parent, info):
        return parent["data"]["txn"]["data"]["data"]["version"]

    def resolve_attr_names(parent, info):
        return parent["data"]["txn"]["data"]["data"]["attr_names"]


    def resolve_definitions(parent, info, **kwargs):
        print('definitions loader resolve')
        print(parent["data"]["txnMetadata"]["txnId"])
        # return definitions_loader.load(parent.id)
        print(parent.id)

        # TXN = DbQuery()
        #
        print('schemabytxid loader resolve')
        schema_txn = schemabytxid_loader.load(parent["data"]["txnMetadata"]["txnId"])
        # schema_txn = db.get(TXN["data"]["txnMetadata"]["txnId"] == parent["data"]["txnMetadata"]["txnId"])
        #
        # cred_def_txns = db.search(TXN["data"]["txn"]["data"]["ref"] == schema_txn["seqNo"])
        print('definitions loader resolve')

        return definitionsbyseqno_loader.load(schema_txn["seqNo"])
        # return cred_def_txns

    def resolve_definitions_count(parent, info):
        # TXN = DbQuery()

        # schema_txn = db.get(TXN["data"]["txnMetadata"]["txnId"] == parent["data"]["txnMetadata"]["txnId"])
        print('schemabytxid loader resolve')

        schema_txn = schemabytxid_loader.load(parent["data"]["txnMetadata"]["txnId"])
        return db.count(TXN["data"]["txn"]["data"]["ref"] == schema_txn["seqNo"])

class SchemaConnection(relay.Connection):
    class Meta:
        node = Schema
    count = Int()

    def resolve_count(root, info):
        return len(root.edges)

class BaseTxn(ObjectType):
    class Meta:
        interfaces = (Transaction, )

    data = String()

    def resolve_data(parent, info):
        return parent['data']

class DID(ObjectType):
    class Meta:
        interfaces = (relay.Node, Transaction)
    did = ID(required=True)
    # id_from = ID()
    # id_dest = ID()
    verkey = String(required=True)
    authored_txns = relay.ConnectionField(TransactionConnection)
    role = String()
    alias = String()
    # schema
    # cred_def
    attributes = relay.ConnectionField(AttributeConnection)

    created_schema = relay.ConnectionField(SchemaConnection)

    created_dids = relay.ConnectionField(lambda : DIDConnection)
    created_dids_count = Int()

    created_definitions = relay.ConnectionField(CredDefConnection)

    created_definitions_count = Int()

    created_schema_count = Int()


    def resolve_role(parent, info):
        try:
            return parent['data']['txn']['data']['role']
        except:
            return None

    def resolve_alias(parent, info):
        try:
            return parent['data']['txn']['data']['alias']
        except:
            return None

    def resolve_verkey(parent, info):
        return parent['data']['txn']['data']["verkey"]

    def resolve_did(parent, info):
        print('parent is', str(parent))
        try:
            print('parent dest is',parent['data']['txn']['data']['dest'])
            return parent['data']['txn']['data']['dest']
        # else:
        #     return None
        except:
            return None

    def resolve_created_dids(parent, info):
        print('created did resolvers')
        return CreatedDIDLoader.load(parent['data']['txn']['data']["dest"])
        # TXN = DbQuery()
        #
        # did_txns = db.search((TXN["data"]["txn"]["metadata"]['from'] == parent['data']['txn']['data']["dest"]) & (TXN["data"]["txn"]["type"] == "1"))
        #
        # return did_txns

    def resolve_created_dids_count(parent, info):
        TXN = DbQuery()

        return db.count((TXN["data"]["txn"]["metadata"]['from'] == parent['data']['txn']['data']["dest"]) & (TXN["data"]["txn"]["type"] == "1"))

    def resolve_created_schema(parent, info, **kwargs):
        TXN = DbQuery()
        schema_txns = db.search((TXN["data"]["txn"]["metadata"]['from'] == parent['data']['txn']['data']["dest"]) & (TXN["data"]["txn"]["type"] == "101"))

        return schema_txns

    def resolve_created_schema_count(parent, info):
        TXN = DbQuery()
        return db.count((TXN["data"]["txn"]["metadata"]['from'] == parent['data']['txn']['data']["dest"]) & (TXN["data"]["txn"]["type"] == "101"))

    def resolve_created_definitions(parent, info):
        TXN = DbQuery()
        cred_def_txns = db.search((TXN["data"]["txn"]["metadata"]['from'] == parent['data']['txn']['data']["dest"]) & (TXN["data"]["txn"]["type"] == "102"))

        return cred_def_txns

    def resolve_created_definitions_count(parent, info):
        TXN = DbQuery()
        return db.count((TXN["data"]["txn"]["metadata"]['from'] == parent['data']['txn']['data']["dest"]) & (TXN["data"]["txn"]["type"] == "102"))


    def resolve_authored_txns(parent, info):
        TXN = DbQuery()
        return db.search(TXN["data"]["txn"]["metadata"]['from'] == parent['data']['txn']['data']["dest"])

    def resolve_attributes(parent, info, **kwargs):
        TXN = DbQuery()
        attr_txns = db.search((TXN["data"]["txn"]["data"]["dest"] == parent['data']['txn']['data']["dest"]) & (TXN["data"]["txn"]["type"] == "100"))

        return attr_txns

class DIDConnection(relay.Connection):
    class Meta:
        node = DID
    count = Int()

    def resolve_count(root, info):
        return len(root.edges)

class Query(ObjectType):
    get_txns = relay.ConnectionField(TransactionConnection, author=String())

    get_txn_by_id = Field(Transaction, seqNo=Int(required=True))

    did = Field(DID, did=String(required=True))

    schema = Field(Schema, id=String())

    definition = Field(CredDef, id=String())

    dids = relay.ConnectionField(DIDConnection, endorser=String())

    schemas = relay.ConnectionField(SchemaConnection, author=String(), endorser=String())

    definitions = relay.ConnectionField(CredDefConnection)

    # nym_by_did = Field(NymTxn, did=String(required=True))

    def resolve_dids(root, info, **kwargs):
        TXN = DbQuery()
        nym_txns = None
        if "endorser" in kwargs:
            nym_txns= db.search((TXN['data']['txn']['type'] == "1") & (TXN["data"]["txn"]["metadata"]["endorser"] == kwargs["endorser"]))
        else:
            nym_txns = db.search((TXN['data']['txn']['type'] == "1"))

        return nym_txns


    def schemas(self, info, **kwargs):
        TXN = DbQuery()
        schema_txns = None
        ## TODO need a better way to handle multiple args into a single query
        # I dont like this approach
        if "endorser" in kwargs and "author" in kwargs:
            schema_txns= db.search((TXN['data']['txn']['type'] == "101") & (TXN["data"]["txn"]["metadata"]["endorser"] == kwargs["endorser"]) & (TXN["data"]["txn"]["metadata"]["from"] == kwargs["author"]))

        elif "endorser" in kwargs:
            schema_txns= db.search((TXN['data']['txn']['type'] == "101") & (TXN["data"]["txn"]["metadata"]["endorser"] == kwargs["endorser"]))
        elif "author" in kwargs:
            schema_txns= db.search((TXN['data']['txn']['type'] == "101") & (TXN["data"]["txn"]["metadata"]["from"] == kwargs["author"]))
        else:
            schema_txns = db.search((TXN['data']['txn']['type'] == "101"))



        return schema_txns

    def definitions(self, info, **kwargs):
        # print('doing it')
        # return definitions_loader.load()
        TXN = DbQuery()
        def_txns = db.search((TXN['data']['txn']['type'] == "101"))


        return def_txns

    def resolve_get_txns(self, info, **kwargs):
        TXN = DbQuery()
        if "author" in kwargs:
            return db.search(TXN["data"]["txn"]["metadata"]['from'] == kwargs["author"])
        else:
            return db.all()

        # print('tx loader resolve')
        # if "author" in kwargs:
        #     print('2')
        #     return tx_loader.load(kwargs["author"])
        # else:
        #     print('3')
        #     return tx_loader.load(0)

    def resolve_get_txn_by_id(self,info, seqNo):
        print('txid loader resolve')
        tx = txbyid_loader.load(seqNo)
        print(tx)
        return tx
        # TXN = DbQuery()
        # return db.get(TXN['seqNo'] == seqNo)

    def resolve_did(self,info, did):
        print('did loader resolve_query_did')
        # TXN = DbQuery()
        # result = db.get((TXN['data']['txn']['data']['dest'] == did) & (TXN['data']['txn']['type'] == "1"))
        # return result
        return did_loader.load(did)

    def resolve_get_schema(self,info, id):
        ## TODO Extract tx time from metadata
        # TXN = DbQuery()
        # result = db.get(TXN["data"]["txnMetadata"]["txnId"] == id)
        # return result
        print('schemabytxid loader resolve')
        return schemabytxid_loader.load(id)

    def resolve_get_definition(self,info, id):
        ## TODO Extract tx time from metadata
        print('definitions loader resolve')
        return definitionsbyseqno_loader.load(id)
        # TXN = DbQuery()
        # result = db.get(TXN["data"]["txnMetadata"]["txnId"] == id)
        #
        # return result

schema = GqSchema(query=Query, types=[BaseTxn, DID, Schema, CredDef, DIDConnection, Attribute, TransactionConnection, SchemaConnection, CredDefConnection])

introspection_dict = schema.introspect()

schema_introspection = introspection_dict
# print(schema_introspection)

# Print the schema in the console
# print(json.dumps(introspection_dict))

# Or save the schema into some file
with open('schema.json', 'w') as fp:
    json.dump(introspection_dict, fp)

with open('schema.graphql', 'w') as fp:
    fp.write(str(schema_introspection))