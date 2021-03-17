# Simple Example Project

Simple project demonstrating the use of [pydgraph], the official python client for Dgraph for `Hyperledger Indy`.

[pydgraph]:https://github.com/dgraph-io/pydgraph

## Running

### Start Dgraph

Start dgraph from the command line with docker as below:
`docker run -it -p 5080:5080 -p 6080:6080 -p 8080:8080 -p 9080:9080 -p 8000:8000 -v ~/dgraph:/dgraph --name dgraph dgraph/standalone:v20.11.0`

Once you exit the docker command you need to remove the containers to run the command again with the command below:
`docker stop dgraph`

## Install the Dependencies

```sh
pip install -r requirements.txt
```

## Create the Schema
Run the following command to install the schema into the dgraph docker image
`curl -X POST localhost:8080/admin/schema --data-binary '@schema.graphql'`

## Run the Sample Code

```sh
python simple.py
```

You can explore the source code in the `simple.py` file.

`docker rm dgraph`
`curl -X POST localhost:8080/admin/schema --data-binary '@schema.graphql'`
`curl -X POST localhost:8080/alter -d '{"drop_all": true}'`
`curl -X POST localhost:8080/alter -d '{"drop_op": "DATA"}'`
