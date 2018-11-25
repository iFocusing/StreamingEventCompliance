from flask_sqlalchemy import SQLAlchemy
from streaming_event_compliance.objects.automata import automata
from streaming_event_compliance.objects.automata import alertlog
from streaming_event_compliance.utils.config import WINDOW_SIZE
from streaming_event_compliance.objects.exceptions.exception import NoUserError

db = SQLAlchemy()


def init_database():
    # db.create_all()
    from streaming_event_compliance.objects.automata.alertlog import db as alter_log_db
    alter_log_db.create_all()
    alter_log_db.session.commit()
    from streaming_event_compliance.objects.automata.automata import db as automata_db
    automata_db.create_all()
    automata_db.session.commit()


def empty_tables():
    db.session.query(automata.Connection).delete()
    db.session.query(automata.Node).delete()
    db.session.query(alertlog.AlertRecord).delete()
    db.session.query(alertlog.User).delete()
    db.session.commit()


def insert_node_and_connection(autos):
    for auto in autos.values():
        for node, degree in auto.nodes.items():
            source_node = automata.Node(node, degree)
            db.session.add(source_node)
        for conn in auto.connections:
            db.session.add(conn)
    db.session.commit()


def insert_alert_log(alogs):
    for alog in alogs.values():
        for alert in alog.alert_log:
            db.session.add(alert)
    db.session.commit()


def create_user(uuid):
    user = alertlog.User.query.filter_by(user_name=uuid).first()
    if user is None:
        user = alertlog.User(uuid)
        db.session.add(user)
        db.session.commit()


def check_user_status(uuid):
    user = alertlog.User.query.filter_by(user_name=uuid).first()
    if user is not None:
        return user.status
    else:
        raise NoUserError


def update_user_status(uuid, status):
    user = alertlog.User.query.filter_by(user_name=uuid).first()
    if user is not None:
        user.status = status
        db.session.commit()
    else:
        raise NoUserError


def init_automata():
    conns = automata.Connection.query.all()
    autos = {}
    for ws in WINDOW_SIZE:
        auto = automata.Automata(ws)
        autos[ws] = auto
    for conn in conns:
        ws = len(conn.source_node)
        auto = autos[ws]
        auto.add_connection(conn)
        auto.update_node(conn.source_node)


def init_alert_log(uuid, autos):
    records = alertlog.AlertRecord.query.filter_by(user_id=uuid).all()
    alogs = {}
    for ws in WINDOW_SIZE:
        alog = alertlog.AlertLog(uuid, ws, autos[ws])
        alogs[ws] = alog
    for record in records:
        ws = len(alog.source_node)
        alog = alogs[ws]
        alog.add_alert_record(record)


def delete_alert(uuid):
    records = alertlog.AlertRecord.query.filter_by(user_id=uuid).all()
    for record in records:
        db.session.delete(record)
    db.session.commit()
