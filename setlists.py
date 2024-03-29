import sldb
import re
import falcon
import json
from playhouse.shortcuts import *
import utils

#return json
def _get_setlist(uuid):
    try:
        sngs = sldb.Song.select().join(sldb.Setlist).where(sldb.Setlist.uuid == uuid)
        sl = sldb.Setlist.select().where(sldb.Setlist.uuid == uuid)[0]
    except IndexError:
        raise falcon.HTTPError(falcon.HTTP_400, '{"Error":"No records"}')
    sl_json = '{"date":"'+sl.date+'","sl_type":"'+sl.sl_type+'","event":"'+sl.event+'","sl_no":"'+str(sl.sl_no)+'","sl_size":"'+str(sl.sl_size)+'","songs":['
    for s in sngs:
        sl_json+='{"artiste":"'+s.artiste+'","title":"'+s.title+'","seq":"'+str(s.seq)+'"},'
    sl_json = sl_json[:-1] #get rid of extra trailling comma
    sl_json += ']}'
    return sl_json
        


#return list of json
def _get_all_setlists(date,sl_type):
    try:
        sls = sldb.Setlist.select().where(sldb.Setlist.date == date, 
                                          sldb.Setlist.sl_type==sl_type)
    except Exception:
        raise falcon.HTTPError(falcon.HTTP_400, '{"Error":"No records"}')
    slf = []
    for sl in sls:
        slf.append(_get_setlist(sl.uuid))

    return slf


class Create(object):
    def on_get(self,req,resp):
        resp.body = '{"error":"No method"}'
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp,usrid):
        if usrid != 'hiromi':
            raise falcon.HTTPError(falcon.HTTP_753, 'No auth')
        temp = req.stream.read()
        try:
            p_json = json.loads(temp)
        except Exception as inst:
            raise falcon.HTTPError(falcon.HTTP_753, 'Malformed JSON')
        #Save to db
        status = "Not Saved"
        if p_json['event'] == '':
            p_json['event'] = "none"
        try:
            g_uuid = utils._gen_uuid(p_json['date'],
                               p_json['sl_no'],
                               p_json['sl_type'])
            if sldb.Setlist.select().where(sldb.Setlist.uuid == g_uuid).exists() != True:
                sl = sldb.Setlist(date=p_json['date'],
                                  sl_type=p_json['sl_type'],
                                  sl_no=p_json['sl_no'],
                                  location=p_json['location'],
                                  sl_size=p_json['sl_size'],
                                  uuid=g_uuid,
                                  event = p_json['event'])
                sl.save()
                for x in p_json['songs']:
                    s = sldb.Song(seq=x['seq'],
                                  title=x['title'],
                                  artiste=x['artiste'],
                                  setlist=sl)
                    s.save()
                    status = "Saved"
            else:
                status = "Record Exists"
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_400, 'Record Exists')
            status = "Not Saved"
        
        resp.status = falcon.HTTP_202
        pbody = status+"\n"+p_json['date']+" "+p_json['sl_type']+" "+p_json['event']+" "+p_json['sl_no']+" "+p_json['location']+" "+p_json['sl_size']+"\n"
        for x in p_json['songs']:
            pbody += x['seq']+" "+x['artiste']+" "+x['title']+"\n"
        resp.body = pbody

class Retrieve(object):
    def on_get(self,req,resp,date,sl_type,sl_no):
        f_date = date[:2]+"/"+date[2:4]+"/"+date[4:]
        rbody = ''
        if sl_no == "0":
            rbody = ','.join(_get_all_setlists(f_date,sl_type))
        else:
            rbody = _get_setlist(date+"_"+sl_type+"_"+sl_no)
        if rbody == None:
            rbody = '{"Error":"No Records"}'
        resp.body = rbody
        resp.status = falcon.HTTP_200
