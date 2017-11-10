# -*- coding: utf-8 -*-
import datetime
import json
import os

from vatu.model.run import Run


class DB:
    """ Persists Run objects
    """

    PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

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
        return os.path.join(DB.PATH, uuid + '.json')


os.makedirs(DB.PATH, exist_ok=True)


class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.dict_to_object, **kwargs)

    def dict_to_object(self, json_dict):
        for (key, value) in json_dict.items():
            try:
                json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            except Exception:
                pass
        return json_dict


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
