import falcon
import json
import logging
import requests
import setlists
import type_view


api = application = falcon.API()

c_setlists = setlists.Create()
r_setlists = setlists.Retrieve()
list_setlists = type_view.List()
artiste_view = type_view.ArtisteView()
sl_type_view = type_view.SetlistTypeView()
list_artiste = type_view.ListArtiste()
list_sl_type = type_view.ListSLType()

api.add_route('/setlists/list', list_setlists)
api.add_route('/setlists/list/artiste', list_artiste)
api.add_route('/setlists/list/type', list_sl_type)
api.add_route('/setlists/list/artiste/{artiste}', artiste_view)
api.add_route('/setlists/list/type/{sl_type}', sl_type_view)
api.add_route('/setlists/view/{date}/{sl_type}/{sl_no}', r_setlists)
api.add_route('/setlists/{usrid}/create',c_setlists)
