# -*- coding: utf-8 -*-
"""
This module implements the Dotmesh client.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2018-03-16
@status: init
"""

from jsonrpcclient.http_client import HTTPClient
from jsonrpcclient.request import Request

class DotmeshClient(object):
    """
    The Dotmesh client.
    :param cluster_url: the dotmesh cluster URL, for example: `http://localhost:6969/rpc`
    :param username: the HTTP Basic auth user name, such as `admin`
    :param api_key: the HTTP Basic auth password as an API Key 
    """

    def __init__(self, cluster_url, username, api_key):
        """
        Creates the Dotmesh client.
        """
        self.cluster_url = cluster_url
        self.client = HTTPClient(cluster_url)
        self.client.session.auth = (username, api_key)

    def ping(self):
        """
        Pings the cluster.
        """
        return self.client.request("DotmeshRPC.Ping")

    def getDot(self, dotname):
        """
        Looks up an existing dot by name. 

        :param dotname: the name of the dot
        :return: a Dot object
        """
        id = self.client.request("DotmeshRPC.Lookup", Namespace="admin", Name=dotname, Branch="")
        return Dot(client=self.client, id=id, name=dotname)

    def createDot(self, dotname):
        """
        Creates a dot by name.

        :param dotname: the name of the dot
        :return: a Dot object
        """
        self.client.request("DotmeshRPC.Create", Namespace="admin", Name=dotname)
        return self.getDot(dotname)

    def deleteDot(self, dotname):
        """
        Deletes a dot by name.

        :param dotname: the name of the dot
        """
        return self.client.request("DotmeshRPC.Delete", Namespace="admin", Name=dotname)

class Dot(object):
    """
    A data dot.
    :param client: the Dotmesh client to use
    :param id: the ID of the dot
    :param name: the name of the dot
    """
    def __init__(self, client, id, name):
        """
        Creates an instance of a data dot.       
        """
        self.client = client
        self.id = id
        self.name = name

    def getBranch(self, branchname):
        """
        Get a branch of a dot.

        :param branchname: the name of the branch
        :return: a Branch object
        """
        bname = branchname
        if branchname == "master":
            bname = ""
        self.client.request("DotmeshRPC.Lookup", Namespace="admin",Name=self.name, Branch=bname)
        return Branch(dot=self, name=branchname)

class Branch(object):
    """
    A branch in a dot.
    :param dot: the Dot this branch belongs to
    :param name: the name of the branch
    """
    def __init__(self, dot, name):
        """
        Creates an instance of a branch in a dot.
        """
        self.dot = dot
        self.name = name

    def commit(self, msg):
        """
        Commits the branch.

        :param msg: the commit message to use
        """
        bname = self.name
        if self.name == "master":
            bname = ""
        return self.dot.client.request("DotmeshRPC.Commit", Namespace="admin", Name=self.dot.name, Branch=bname, Message=msg)

    def log(self):
        """
        Shows the commit log.
        """
        bname = self.name
        if self.name == "master":
            bname = ""
        return self.dot.client.request("DotmeshRPC.Commits", Namespace="admin", Name=self.dot.name, Branch=bname)

    def createBranch(self, newbranchname, srcbranchname, commit_id=""):
        """
        Create a branch based on an existing (source) branch.
        If no commit ID is provided, uses the ID of the most recent commit.

        :param newbranchname: the name of the new branch to create
        :param srcbranchname: the name of the branch to start the new branch off
        :param commit_id: if set, use this commit ID otherwise use most recent
        :return: a Branch object
        """
        if commit_id == "":  # use the most recent commit ID
            commitlog = self.log()
            commit_id = commitlog[-1]["Id"]  
        self.dot.client.request("DotmeshRPC.Branch",
                                Namespace="admin", Name=self.dot.name, SourceBranch=srcbranchname, NewBranchName=newbranchname, SourceCommitId=commit_id)
        return Branch(dot=self.dot, name=newbranchname)
