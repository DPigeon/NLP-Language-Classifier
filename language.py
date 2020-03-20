from enum import Enum

""" Method that transforms the enum to dictionary for potential key => value"""


def to_dict():
    dict_to_return = {}
    for i in iter(Language):
        dict_to_return[i] = 0
    return dict_to_return


class Language(Enum):
    BASQUE = 'eu'
    CATALAN = 'ca'
    GALICAN = 'gl'
    SPANISH = 'es'
    ENGLISH = 'en'
    PORTUGUESE = 'pt'
