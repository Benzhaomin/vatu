import os


def get_filepath(filename):
    return os.path.join(os.path.dirname(__file__), 'files', filename)
