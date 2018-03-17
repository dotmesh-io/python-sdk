# Datadots API for Python

[![PyPI](https://img.shields.io/pypi/v/nine.svg)](https://pypi.org/project/datadots-api/)


**STATUS: What you currently see here is WIP, do not use in production!** 

This is the Datadots API for Python, allowing you to access and manipulate dots against any Dotmesh cluster. Note that only Python 3 is supported.

- [Install](#install)
- [Use](#use)
    - [Create a dot](#create-a-dot)
    - [Look up a dot by name](#look-up-a-dot-by-name)
    - [Commit to branch, show log](#commit-to-a-branch-and-show-the-log)
    - [Create new branch based on latest master](#create-new-branch-based-on-latest-master)
    - [End-to-end example](#end-to-end-example)
- [Test](#test)

## Install

You must have Python 3 installed, this is the only version supported.
Then do:

```bash
$ pip3 install datadots-api==0.1.2
```

## Use

Some usage examples below.

### Create a dot

```python
from dotmesh.client import DotmeshClient
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
dot = dmclient.createDot(dotname="test")
```

### Look up a dot by name

```python
from dotmesh.client import DotmeshClient
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
print(d.getDot(dotname="test"))
```

### Commit to a branch and show the log

```python
from dotmesh.client import DotmeshClient
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
dot = dmclient.createDot(dotname="test")
branch = dot.getBranch("master")
branch.commit("just a test commit")
print(branch.log())
```

### Create new branch based on latest master

```python
from dotmesh.client import DotmeshClient
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
dot = dmclient.createDot(dotname="test")
branch = dot.getBranch("master")
branch.commit("just a test commit")
mybranch = branch.createBranch("mybranch", "master")
mybranch.commit("the first commit in my branch")
print(mybranch.log())
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
<-- {"jsonrpc":"2.0","result":"32965cef-4310-4291-6f36-c86106655d10","id":2} (200 OK)

ID=32965cef-4310-4291-6f36-c86106655d10, name=test

== Get master branch:
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Lookup", "params": {"Namespace": "admin", "Name": "test", "Branch": ""}, "id": 3}
<-- {"jsonrpc":"2.0","result":"32965cef-4310-4291-6f36-c86106655d10","id":3} (200 OK)

master

== Do some commit and show log:
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Commit", "params": {"Namespace": "admin", "Name": "test", "Branch": "", "Message": "just a test commit"}, "id": 4}
<-- {"jsonrpc":"2.0","result":true,"id":4} (200 OK)
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Commit", "params": {"Namespace": "admin", "Name": "test", "Branch": "", "Message": "and another commit, who would have thought"}, "id": 5}
<-- {"jsonrpc":"2.0","result":true,"id":5} (200 OK)
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Commits", "params": {"Namespace": "admin", "Name": "test", "Branch": ""}, "id": 6}
<-- {"jsonrpc":"2.0","result":[{"Id":"1007db99-11cb-4bd7-747e-1d121bb9b11a","Metadata":{"author":"admin","message":"just a test commit","timestamp":"1521214312285694689"}},{"Id":"67bb6184-430b-46d7-4337-b858ee85eb1c","Metadata":{"author":"admin","message":"and another commit, who would have thought","timestamp":"1521214312418429042"}}],"id":6} (200 OK)


1521214312285694689: just a test commit
1521214312418429042: and another commit, who would have thought

== Create new branch, commit and show log:
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Commits", "params": {"Namespace": "admin", "Name": "test", "Branch": ""}, "id": 7}
<-- {"jsonrpc":"2.0","result":[{"Id":"1007db99-11cb-4bd7-747e-1d121bb9b11a","Metadata":{"author":"admin","message":"just a test commit","timestamp":"1521214312285694689"}},{"Id":"67bb6184-430b-46d7-4337-b858ee85eb1c","Metadata":{"author":"admin","message":"and another commit, who would have thought","timestamp":"1521214312418429042"}}],"id":7} (200 OK)
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Branch", "params": {"Namespace": "admin", "Name": "test", "SourceBranch": "master", "NewBranchName": "mybranch", "SourceCommitId": "67bb6184-430b-46d7-4337-b858ee85eb1c"}, "id": 8}
<-- {"jsonrpc":"2.0","result":true,"id":8} (200 OK)
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Commit", "params": {"Namespace": "admin", "Name": "test", "Branch": "mybranch", "Message": "the first commit in my branch"}, "id": 9}
<-- {"jsonrpc":"2.0","result":true,"id":9} (200 OK)
--> {"jsonrpc": "2.0", "method": "DotmeshRPC.Commits", "params": {"Namespace": "admin", "Name": "test", "Branch": "mybranch"}, "id": 10}
<-- {"jsonrpc":"2.0","result":[{"Id":"565b04ab-abae-476a-75bd-203bce2a56b2","Metadata":{"author":"admin","message":"the first commit in my branch","timestamp":"1521214312967840418"}}],"id":10} (200 OK)


1521214312967840418: the first commit in my branch
```

Note that the default behavior of the example above is to leave the dot in place, that is, if you do a `dm dot show test` you should see both the `master` branch and `mybranch` with the commits. If you want to automatically clean up, execute it as follows: `python3 example.py cleanup`:

```bash
$ dm list
Current remote: local (use 'dm remote -v' to list and 'dm remote switch' to switch)

  DOT   BRANCH  SERVER            CONTAINERS  SIZE      COMMITS  DIRTY
* test  master  995e5c821c38e7f5              1.00 kiB  1        -

$ dm dot show test
Dot admin/test:
Master branch ID: 7f4a4d67-5bc7-47aa-7829-31d5a02ff70f
Dot is current.
Dot size: 1.00 kiB (all clean)
Branches:
* master
  mybranch

$ dm checkout mybranch && dm log
commit 565b04ab-abae-476a-75bd-203bce2a56b2
Author: admin
Date: 1521214312967840418

    the first commit in my branch
```

## Test

Locally, you can test the Dotmesh JSON-RPC API like shown in the following. It assumes you've got [http](https://httpie.org/) installed (or alternatively you can use `curl`) as well as that Docker is running (note: tested on v18.03):

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