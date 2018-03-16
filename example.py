import os
import time
from api.client import DotmeshClient

# let's set up the cluster access:
api_key = os.environ['DOTMESH_APIKEY']
cluster_url = "http://localhost:6969/rpc"
dmclient = DotmeshClient(cluster_url=cluster_url, username="admin", api_key=api_key)

# now let's create a dot called 'test' and work in a branch called 'master':
dotname = "test"
branchname= "master"
dot = dmclient.createDot(dotname=dotname)
# alternatively, if a dot already exists,
# you can do the following:
# dot = dmclient.getDot(dotname=dotname)
print("Dot: ID={0}, name={1}".format(dot.id, dot.name))

# get a branch to work on:
branch = dot.getBranch(branchname)
print("Branch: {0}".format(branch.name))

# now let's clean up:
dmclient.deleteDot(dotname=dotname)
