# Datadots API for Python

STATUS: This WIP!

This is the Datadots API for Python, allowing you to access and manipulate dots against any Dotmesh cluster. Note that only Python 3 is supported.

## Install

TBD. Once this repo is public, register via https://pypi.python.org/pypi

## Use

Look up a dot by name:

```python
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
print(d.getDot(dotname="test"))
```

Full example:

```python
d = DotmeshClient(cluster_url=cluster_url, username=user, api_key=api_key)
dot = d.getDot(dotname="test")
branch = dot.getBranch("master")
branch.commit(commitMessage)
newBranch = branch.branch(newBranch)
```

For example, for a local setup with Docker running and after you've created a cluster using `dm cluster init`, you can run the following [example](example.py):

```bash
$ DOTMESH_APIKEY=$(cat ~/.dotmesh/config | jq -r .Remotes.local.ApiKey)
$ DOTMESH_APIKEY=$DOTMESH_APIKEY python3 example.py
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