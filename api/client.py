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
    """

    def __init__(self, cluster_url, username, api_key):
        """
        Creates an instance of the Dotmesh client.
        
        :Parameters:
           - `cluster_url`: the dotmesh cluster URL, for example: `http://localhost:6969/rpc`
           - `username`: the HTTP Basic auth user name, such as `admin`
           - `api_key`: the HTTP Basic auth password as an API Key 
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
        Gets handle to a dot.

        :Parameters:
           - `dotname`: the name of the dot
        """
        return self.client.request("DotmeshRPC.Lookup", Namespace="admin", Name=dotname, Branch="")

    def createDot(self, dotname):
        """
        Creates a dot.

        :Parameters:
           - `dotname`: the name of the dot
        """
        return self.client.request("DotmeshRPC.Create", Namespace="admin", Name=dotname)
