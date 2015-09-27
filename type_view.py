# -*- coding: utf-8 -*-
import sldb
import re
import falcon
import json
from playhouse.shortcuts import *
import utils

class ArtisteView(object):
    def on_get(self,req,resp,artiste):
        a = sldb.Song.select(sldb.Song.title).where(sldb.Song.artiste == artiste).distinct()
        songs = []
        for sng in a:
            songs.append(sng.title)
        rbody = u"持ち曲 ("+str(len(songs))+"):\n"
        songs.sort()
        rbody += u'\u000A'.join(songs)
        resp.body = rbody
        resp.status=falcon.HTTP_200

class SetlistTypeView(object):
    def on_get(self,req,resp,sl_type):
        a = sldb.Setlist.select(sldb.Setlist.uuid).where(sldb.Setlist.sl_type == sl_type).distinct()
        sls = []
        for sl in a:
            sls.append(sl.uuid)
        rbody = sl_type+" Setlists ("+str(len(sls))+"):\n"
        rbody += '\n'.join(sls)
        resp.body = rbody
        resp.status=falcon.HTTP_200

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
