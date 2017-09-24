# -*- coding: utf-8 -*-
import json
import datetime
import os

from vatu.run import Run

DBPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

os.makedirs(DBPATH, exist_ok=True)


class DB:
    """ Persists Run objects
    """

    @staticmethod
    def save(run):
        """ Persists a Run
        """
        with open(DB._path_for_uuid(run['uuid']), 'w') as fp:
            json.dump(run, fp, cls=DateTimeEncoder)

    @staticmethod
    def load(uuid):
        """ Returns a Run loaded by its uuid
        """
        with open(DB._path_for_uuid(uuid)) as fp:
            return Run(json.load(fp, cls=DateTimeDecoder))

    @staticmethod
    def delete(run):
        """ Deletes a persisted Run
        """
        os.remove(DB._path_for_uuid(run['uuid']))

    @staticmethod
    def _path_for_uuid(uuid):
        """ Returns an absolute file path to a Run file based on its uuid
        """
        uuid = os.path.basename(uuid)  # no directory traversal plz
        return os.path.join(DBPATH, uuid + '.json')


# JSON dates encoder and decoder from https://gist.github.com/abhinav-upadhyay/5300137

class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.dict_to_object, **kwargs)

    def dict_to_object(self, d):
        if '__type__' not in d:
            return d

        _type = d.pop('__type__')
        try:
            dateobj = datetime.datetime(**d)
            return dateobj
        except:
            d['__type__'] = _type
            return d


class DateTimeEncoder(json.JSONEncoder):
    """ Instead of letting the default encoder convert datetime to string,
        convert datetime objects into a dict, which can be decoded by the
        DateTimeDecoder
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {
                '__type__': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
                'microsecond': obj.microsecond,
            }
        else:
            return json.JSONEncoder.default(self, obj)
