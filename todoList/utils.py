import json
import webapp2

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif hasattr(obj, 'email'):
        return obj.email()
    elif hasattr(obj, 'kind') and hasattr(obj, 'urlsafe'):
        return obj.urlsafe()
    else:
        raise TypeError("Unserializable object %s of type %s" % (obj, type(obj)))

    return obj


def data2json(data):
    return json.dumps(
        data,
        default=date_handler,
        indent=2,
        separators=(',', ': '),
        ensure_ascii=False
    )