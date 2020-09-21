import random
import sql
import config
import exceptions


def add_word_pair(word_pair):
    try:
        lat, ru = word_pair.lower().split()
    except ValueError:
        return False

    db_worker = sql.SQLiter(config.database)
    db_worker.insert(lat, ru)
    db_worker.close()
    return True


def get_random_pair():
    db_worker = sql.SQLiter(config.database)
    try:
        random_row = random.randint(1, db_worker.count_rows())
        row = db_worker.select_single(random_row)
        return row[1:]
    except exceptions.GetFromDbError:
        pass
    finally:
        db_worker.close()


def clean_database():
    db_worker = sql.SQLiter(config.database)
    try:
        db_worker.clr()
        return True
    except exceptions.ClrError:
        return False
    finally:
        db_worker.close()
