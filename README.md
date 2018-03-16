# Datadots API—Python

## Install


## Use

```python
d = DotmeshClient("localhost", username, apiKey)
dot = d.getDot(dotName)
branch = dot.getBranch("master")
branch.commit(commitMessage)
newBranch = branch.branch(newBranch)
```


## Testing

Locally, you can test the API like so, given [http](https://httpie.org/) (or alternatively you can use `curl`) is installed and Docker is running:

```bash
$ dm cluster init
$ DOTMESH_APIKEY=$(cat ~/.dotmesh/config | jq -r .Remotes.local.ApiKey)
$ http -a admin:$DOTMESH_APIKEY POST http://localhost:6969/rpc < test/ping.json
```