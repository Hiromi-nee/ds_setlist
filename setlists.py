import sldb
import re
import falcon
import json
from playhouse.shortcuts import *

#return json
def _get_setlist(uuid):
    try:
        sngs = sldb.Song.select().join(sldb.Setlist).where(sldb.Setlist.uuid == uuid)
        sl = sldb.Setlist.select().where(sldb.Setlist.uuid == uuid)[0]
    except IndexError:
        raise falcon.HTTPError(falcon.HTTP_753, '{"Error":"No records"}')
    sl_json = '{"date":"'+sl.date+'","sl_type":"'+sl.sl_type+'","sl_no":"'+str(sl.sl_no)+'","songs":['
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
        raise falcon.HTTPError(falcon.HTTP_753, '{"Error":"No records"}')
    slf = []
    for sl in sls:
        slf.append(_get_setlist(sl.uuid))

    return slf

def _gen_uuid(date,sl_no,sl_type):
    date = re.sub("/+","",date)
    return date+"_"+sl_type+"_"+sl_no

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
        #Save to db
        status = "Not Saved"
        try:
            g_uuid = _gen_uuid(p_json['date'],
                               p_json['sl_no'],
                               p_json['sl_type'])

            sl = sldb.Setlist(date=p_json['date'],
                              sl_type=p_json['sl_type'],
                              sl_no=p_json['sl_no'],
                              location=p_json['location'],
                              uuid=g_uuid)
            sl.save()
            for x in p_json['songs']:
                s = sldb.Song(seq=x['seq'],
                              title=x['title'],
                              artiste=x['artiste'],
                              setlist=sl)
                s.save()
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_753, 'DB ERROR')
            status = "Not Saved"
        
        resp.status = falcon.HTTP_202
        status = "Saved"
        pbody = status+"\n"+p_json['date']+" "+p_json['sl_type']+" "+p_json['sl_no']+" "+p_json['location']+"\n"
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

class List(object):
    def on_get(self,req,resp):
        a = sldb.Setlist.select()
        rbody = 'Available Setlists:\n'
        sls = []
        for x in a:
             sls.append(x.uuid)
        sls.sort()
        rbody += '\n'.join(sls)
        resp.body = rbody
        resp.status = falcon.HTTP_200
