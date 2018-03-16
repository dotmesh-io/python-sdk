import os
from api.client import DotmeshClient

# let's set up the cluster access:
api_key = os.environ['DOTMESH_APIKEY']
cluster_url = "http://localhost:6969/rpc"
d = DotmeshClient(cluster_url=cluster_url, username="admin", api_key=api_key)

# now let's create a dot called 'test' and query it then:
dotname = "test"
d.createDot(dotname=dotname)
print(d.getDot(dotname=dotname))
