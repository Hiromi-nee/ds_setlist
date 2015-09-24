import sldb
import re
import falcon
import json
from playhouse.shortcuts import *
import utils

class ArtisteView(object):
    pass

class SetlistTypeView(object):
    pass

class ListArtiste(object):
    def on_get(self,req,resp):
        a = sldb.Song.select(sldb.Song.artiste).distinct()
        artistes = []
        for sl in a:
            artistes.append(sl.artiste)
        rbody = "Available Artistes ("+str(len(artistes))+"):\n"
        artistes.sort()
        rbody += '\n'.join(artistes)
        resp.body = rbody
        resp.status = falcon.HTTP_200

class ListSLType(object):
    def on_get(self,req,resp):
        a = sldb.Setlist.select(sldb.Setlist.sl_type).distinct()
        sl_types = []
        for sltype in a:
            sl_types.append(sltype.sl_type)
        rbody = "Available Setlist Types ("+str(len(sl_types))+"):\n"
        sl_types.sort()
        rbody += '\n'.join(sl_types)
        resp.body = rbody
        resp.status = falcon.HTTP_200
    
class List(object):
    def on_get(self,req,resp):
        a = sldb.Setlist.select()
        rbody = 'Available Setlists:\n'
        sls = []
        for x in a:
             sls.append(x.uuid)
             #sls.sort()      
        rbody = "Available Setlists ("+str(len(sls))+"):\n"
        rbody += '\n'.join(sls)
        resp.body = rbody
        resp.status = falcon.HTTP_200
