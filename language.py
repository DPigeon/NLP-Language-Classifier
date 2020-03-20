from enum import Enum

""" Method that transforms the enum to dictionary for potential key => value"""


def to_dict(smoothing=0):
    dict_to_return = {}
    for i in iter(Language):
        dict_to_return[i] = smoothing   # Initializing
    return dict_to_return


class Language(Enum):
    BASQUE = 'eu'
    CATALAN = 'ca'
    GALICAN = 'gl'
    SPANISH = 'es'
    ENGLISH = 'en'
    PORTUGUESE = 'pt'
