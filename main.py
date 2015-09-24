import falcon
import json
import logging
import requests
import setlists


api = application = falcon.API()

c_setlists = setlists.Create()
r_setlists = setlists.Retrieve()
list_setlists = setlists.List()


#api.add_route('/setlists/{artiste}',artiste_songs)
#api.add_route('/setlists/{sl_type}',type_setlists)
api.add_route('/setlists/list', list_setlists)
api.add_route('/setlists/read/{date}/{sl_type}/{sl_no}', r_setlists)
api.add_route('/setlists/{usrid}/create',c_setlists)
