# -*- coding: utf-8 -*-
"""
This module implements the Dotmesh client.

@author: Michael Hausenblas, http://mhausenblas.info/#i and Luke Marsden
    https://lukemarsden.net
@since: 2018-03-16
@status: init
"""

from jsonrpcclient.clients.http_client import HTTPClient

class InvalidNamespaceAndName(Exception):
    pass

class DotName(object):
    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name

    @classmethod
    def fromDotNameWithOptionalNamespace(cls, identifier):
        """
        Accept dot names in the form:

        - frob
          In which case 'frob' is the dot name and the namespace defaults to
          'admin'.

        - foo/frob
          In which case 'foo' is the namespace (e.g. a user's username) and
          'frob' is the dot name.
        """
        if "/" in identifier:
            shrap = identifier.split("/", 1)
            return cls(namespace=shrap[0], name=shrap[1])
        else:
            return cls(namespace="admin", name=identifier)

    @classmethod
    def fromDotNamespaceAndName(cls, identifier):
        """
        Like fromDotNameWithOptionalNamespace but only accept the form with the
        namespace delimitor.

        - foo/frob
          In which case 'foo' is the namespace (e.g. a user's username) and
          'frob' is the dot name.
        """
        parts = identifier.split("/")
        if len(parts) == 2:
           return cls(namespace=parts[0], name=parts[1])
        else:
           raise InvalidNamespaceAndName(
               "Invalid dot name %s - %r" % (identifier, parts),
           )

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

    def getDot(self, dotname, ns="admin"):
        """
        Looks up an existing dot by name. 

        :param dotname: the name of the dot, as a string or a DotName
        :param ns: the namespace to operate in (if dotname isn't a Dotname), defaults to 'admin'
        :return: a Dot object
        """
        if isinstance(dotname, DotName):
            ns = dotname.namespace
            dotname = dotname.name

        id = self.client.request("DotmeshRPC.Lookup", Namespace=ns, Name=dotname, Branch="")
        return Dot(client=self.client, id=id, name=dotname, ns=ns)

    def createDot(self, dotname, ns="admin"):
        """
        Creates a dot by name.

        :param dotname: the name of the dot
        :param ns: the namespace to operate in, defaults to 'admin'
        :return: a Dot object
        """
        if isinstance(dotname, DotName):
            ns = dotname.namespace
            dotname = dotname.name

        self.client.request("DotmeshRPC.Create", Namespace=ns, Name=dotname)
        return self.getDot(dotname, ns)

    def deleteDot(self, dotname, ns="admin"):
        """
        Deletes a dot by name.

        :param dotname: the name of the dot
        :param ns: the namespace to operate in, defaults to 'admin'
        """
        if isinstance(dotname, DotName):
            ns = dotname.namespace
            dotname = dotname.name

        return self.client.request("DotmeshRPC.Delete", Namespace=ns, Name=dotname)

class Dot(object):
    """
    A data dot.
    :param client: the Dotmesh client to use
    :param id: the ID of the dot
    :param name: the name of the dot
    """
    def __init__(self, client, id, name, ns="admin"):
        """
        Creates an instance of a data dot.       
        """
        self.client = client
        self.id = id
        self.name = name
        self.ns = ns

    def getBranch(self, branchname):
        """
        Get a branch of a dot.

        :param branchname: the name of the branch
        :return: a Branch object
        """
        bname = branchname
        if branchname == "master":
            bname = ""
        self.client.request("DotmeshRPC.Lookup", Namespace=self.ns,Name=self.name, Branch=bname)
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

    def commit(self, msg, metadata={}):
        """
        Commits the branch.

        :param msg: the commit message to use
        :param metadata: a dict of metadata key/value pairs to add to the commit
        """
        bname = self.name
        if self.name == "master":
            bname = ""
        return self.dot.client.request("DotmeshRPC.Commit", Namespace=self.dot.ns, Name=self.dot.name, Branch=bname, Message=msg, Metadata=metadata)

    def log(self):
        """
        Shows the commit log.
        """
        bname = self.name
        if self.name == "master":
            bname = ""
        return self.dot.client.request("DotmeshRPC.Commits", Namespace=self.dot.ns, Name=self.dot.name, Branch=bname)

    def createBranch(self, newbranchname, srcbranchname, commit_id=""):
        """
        Create a branch based on an existing (source) branch.
        If no commit ID is provided, uses the ID of the most recent commit.

        :param newbranchname: the name of the new branch to create
        :param srcbranchname: the name of the branch to start the new branch off
        :param commit_id: if set, use this commit ID otherwise use most recent one
        :return: a Branch object
        """
        if commit_id == "":  # use the most recent commit ID
            commitlog = self.log()
            commit_id = commitlog[-1]["Id"]  
        self.dot.client.request("DotmeshRPC.Branch",
                                Namespace=self.dot.ns,
                                Name=self.dot.name,
                                SourceBranch=srcbranchname,
                                NewBranchName=newbranchname,
                                SourceCommitId=commit_id)
        return Branch(dot=self.dot, name=newbranchname)
