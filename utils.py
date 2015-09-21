import re

def _view_setlist(temp):
    response = ""
    try:
        p_json = json.loads(temp)
    except Exception as inst:
        raise falcon.HTTPError(falcon.HTTP_753, 'Malformed JSON')


    response += p_json['date']+" "+p_json['sl_type']+" "+p_json['sl_no']+" "+p_json['event']+" @ "+p_json['location']+" "+p_json['sl_size']+" Songs \n"

    for x in p_json['songs']:
        response += x['seq']+". "+x['artiste']+" - "+x['title']+"\n"
        
    return response

def _gen_uuid(date,sl_no,sl_type):
    date = re.sub("/+","",date)
    return date+"_"+sl_type+"_"+sl_no
