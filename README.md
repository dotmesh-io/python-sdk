# Datadots API for Python

STATUS: This WIP!

This is the Datadots API for Python, allowing you to access and manipulate dots against any Dotmesh cluster. Note that only Python 3 is supported.

- [Install](#install)
- [Use](#use)
    - [Create a dot](#create-a-dot)
    - [Look up a dot by name](#look-up-a-dot-by-name)
    - [Commit to branch, show log](#commit-to-a-branch-and-show-the-log)
    - [End-to-end example](#end-to-end-example)
- [Test](#test)

## Install

TBD: register via https://pypi.python.org/pypi

## Use

Some usage examples below.

### Create a dot

```python
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
dot = dmclient.createDot(dotname="test")
```

### Look up a dot by name

```python
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
print(d.getDot(dotname="test"))
```

### Commit to a branch and show the log

```python
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
dot = dmclient.createDot(dotname="test")
branch = dot.getBranch("master")
branch.commit("just a test commit")
print(branch.log())
```

### End-to-end example

You can see this API in action, for a local setup with Docker running and after you've created a cluster using `dm cluster init`, by running the following [example](example.py):

```bash
$ DOTMESH_APIKEY=$(cat ~/.dotmesh/config | jq -r .Remotes.local.ApiKey)
$ DOTMESH_APIKEY=$DOTMESH_APIKEY python3 example.py
== Create dot:
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Create", "params": {"Namespace": "admin", "Name": "test"}, "id": 1}
<-- {"jsonrpc":"2.0","result":true,"id":1} (200 OK)
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Lookup", "params": {"Namespace": "admin", "Name": "test", "Branch": ""}, "id": 2}
<-- {"jsonrpc":"2.0","result":"4e037388-7056-455d-6bc2-5db1e4cba176","id":2} (200 OK)

ID=4e037388-7056-455d-6bc2-5db1e4cba176, name=test

== Get master branch:
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Lookup", "params": {"Namespace": "admin", "Name": "test", "Branch": ""}, "id": 3}
<-- {"jsonrpc":"2.0","result":"4e037388-7056-455d-6bc2-5db1e4cba176","id":3} (200 OK)

master

== Do some commit and show log:
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Commit", "params": {"Namespace": "admin", "Name": "test", "Branch": "", "Message": "just a test commit"}, "id": 4}
<-- {"jsonrpc":"2.0","result":true,"id":4} (200 OK)
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Commit", "params": {"Namespace": "admin", "Name": "test", "Branch": "", "Message": "and another commit, who would have thought"}, "id": 5}
<-- {"jsonrpc":"2.0","result":true,"id":5} (200 OK)
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Commits", "params": {"Namespace": "admin", "Name": "test", "Branch": ""}, "id": 6}
<-- {"jsonrpc":"2.0","result":[{"Id":"59006545-7988-44e5-4b6d-1bfa7ef0b273","Metadata":{"author":"admin","message":"just a test commit","timestamp":"1521200357517891900"}},{"Id":"91b599f2-4413-453a-63d9-6c7921a0ed79","Metadata":{"author":"admin","message":"and another commit, who would have thought","timestamp":"1521200357640439200"}}],"id":6} (200 OK)


1521200357517891900: just a test commit
1521200357640439200: and another commit, who would have thought

== Clean-up:
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Delete", "params": {"Namespace": "admin", "Name": "test"}, "id": 7}
<-- {"jsonrpc":"2.0","result":true,"id":7} (200 OK)
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