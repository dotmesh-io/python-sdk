# Datadots API for Python

STATUS: This WIP!

This is the Datadots API for Python, allowing you to access and manipulate dots against any Dotmesh cluster. Note that only Python 3 is supported.

## Install

TBD: register via https://pypi.python.org/pypi

## Use

Look up a dot by name:

```python
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
print(d.getDot(dotname="test"))
```

You can see this API in action, for a local setup with Docker running and after you've created a cluster using `dm cluster init`, by running the following [example](example.py):

```bash
$ DOTMESH_APIKEY=$(cat ~/.dotmesh/config | jq -r .Remotes.local.ApiKey)
$ DOTMESH_APIKEY=$DOTMESH_APIKEY python3 example.py
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Create", "params": {"Namespace": "admin", "Name": "test"}, "id": 1}
<-- {"jsonrpc":"2.0","result":true,"id":1} (200 OK)
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Lookup", "params": {"Namespace": "admin", "Name": "test", "Branch": ""}, "id": 2}
<-- {"jsonrpc":"2.0","result":"10116ebc-0a02-4704-5919-0a731da74c4b","id":2} (200 OK)
Dot: ID=10116ebc-0a02-4704-5919-0a731da74c4b, name=test
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Lookup", "params": {"Namespace": "admin", "Name": "test", "Branch": ""}, "id": 3}
<-- {"jsonrpc":"2.0","result":"10116ebc-0a02-4704-5919-0a731da74c4b","id":3} (200 OK)
Branch: master
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Delete", "params": {"Namespace": "admin", "Name": "test"}, "id": 4}
<-- {"jsonrpc":"2.0","result":true,"id":4} (200 OK)
```

## Test

Locally, you can test the API like so, given [http](https://httpie.org/) (or alternatively you can use `curl`) is installed and Docker is running:

```bash
$ dm cluster init
$ DOTMESH_CLUSTERURL=http://localhost:6969/rpc
$ DOTMESH_APIKEY=$(cat ~/.dotmesh/config | jq -r .Remotes.local.ApiKey)
$ http -a admin:$DOTMESH_APIKEY POST $DOTMESH_CLUSTERURL < test/ping.json
HTTP/1.1 200 OK
Content-Length: 57
Content-Type: application/json; charset=utf-8
Date: Fri, 16 Mar 2018 07:06:44 GMT
X-Content-Type-Options: nosniff

{
    "id": 6129484611666146000,
    "jsonrpc": "2.0",
    "result": true
}
```