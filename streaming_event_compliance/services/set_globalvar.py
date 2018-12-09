from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services import globalvar


def change_autos(key, value):
    globalvar.autos[key] = value


def get_autos():
    return globalvar.autos, globalvar.status


def call_buildautos():
    build_automata.build_automata()
    # running the below two lines to get automata to memory for compliance checking
    globalvar.init()
    autos, status = get_autos()


def clear_globelvar():
    globalvar.T.dictionary_threads = {}
    globalvar.C.dictionary_cases = {}
    globalvar.C.lock_List = {}




