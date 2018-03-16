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
print("== Create dot:")
dot = dmclient.createDot(dotname=dotname)
# alternatively, if a dot already exists,
# you can do the following:
# dot = dmclient.getDot(dotname=dotname)
print("\nID={0}, name={1}".format(dot.id, dot.name))

# get a branch to work on:
print("\n== Get master branch:")
branch = dot.getBranch(branchname)
print("\n{0}".format(branch.name))

# now let's do a commit:
print("\n== Do some commit and show log:")
branch.commit("just a test commit")
branch.commit("and another commit, who would have thought")
log = branch.log()
print("\n")
for entry in log:
    msg = entry["Metadata"]["message"]
    ctime = entry["Metadata"]["timestamp"]
    print("{0}: {1}".format(ctime, msg))

# now let's clean up by deleting the dot (and all the commits)
print("\n== Clean-up:")
dmclient.deleteDot(dotname=dotname)
