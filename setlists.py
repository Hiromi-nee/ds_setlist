import sldb
import re
import falcon
import json

def _get_setlist(uuid):
    pass

def _get_all_setlists(date):
    pass

def _gen_uuid(date,sl_no):
    date = re.sub("/+","",date)
    return date+sl_no

class Create(object):
    def on_get(self,req,resp):
        resp.body = '{"error":"No method"}'
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        temp = req.stream.read()
        try:
            p_json = json.loads(temp)
        except Exception as inst:
            raise falcon.HTTPError(falcon.HTTP_753, 'Malformed JSON')
        resp.status = falcon.HTTP_202
        pbody = p_json['date']+" "+p_json['sl_type']+" "+p_json['sl_no']+" "+p_json['location']+"\n"
        for x in p_json['songs']:
            pbody += x['seq']+" "+x['artiste']+" "+x['title']+"\n"
        resp.body = pbody

class Retrieve(object):
    def on_get(self,req,resp,date,sl_no):
        f_date = date[:2]+"/"+date[2:4]+"/"+date[4:]
        if sl_no == "0":
            _get_all_setlists(f_date)
        else:
            _get_setlist(date+"_"+sl_no)
        resp.body = '{"error":"No method"}'
        resp.status = falcon.HTTP_200

