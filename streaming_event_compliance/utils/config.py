import os

DATABASE_PATH = 'mysql+pymysql://compliancechecker:compliancechecker@localhost/compliancechecker'

AUTOMATA_FILE = 'automata.pdf'
BASE_DIR = os.path.dirname(__file__)
WINDOW_SIZE = [1, 2, 3, 4]


TRAINING_EVENT_LOG_PATH = 'data' + os.sep + '/Example_EventLogForTraining.xes'
MAXIMUN_WINDOW_SIZE = '3'
