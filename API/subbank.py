import MySQLdb
from . import getDB


def subbank_add(data):
    r"""
            :param data: a tuple of data consists of all 支行 columns
    """
    db = getDB()
    try:
        cur = db.cursor()

        cur.callproc('subbank_add', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def subbank_delete(data):
    r"""
            :param data: a tuple of data just consists of subbank name
    """
    db = getDB()
    try:
        cur = db.cursor()

        cur.callproc('subbank_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def subbank_update(data):
    r"""
            :param data: a tuple of data just consists of all 支行 columns
    """
    db = getDB()
    try:
        cur = db.cursor()

        cur.callproc('subbank_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

