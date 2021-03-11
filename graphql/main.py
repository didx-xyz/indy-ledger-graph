from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.graphql import GraphQLApp
from schema import schema, schema_introspection
import graphene
import json

app = FastAPI()

app.add_route('/graphql', GraphQLApp(schema=schema))

@app.get('/')
def ping():
    return {'API': '/graphql', 'SCHEMA INTROSPECTION': '/schema_introspection', 'SCHEMA JSON': '/schema_json'}

@app.get('/schema_introspection')
def schema():
    return {'schema_str': schema_introspection}

@app.get('/schema_json')
def schema():
    # json_data = jsonable_encoder(schema_json)
    # return JSONResponse(content=json_data)
    return Response(content=json.dumps(schema_introspection), media_type="application/json")
