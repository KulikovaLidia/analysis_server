from models.citizen_data import Citizen
from models.db import session


def get_one_citizen_by_unique_pair(import_id, citizen_id):
    return (session.query(Citizen).filter(Citizen.import_id == import_id).filter(
        Citizen.citizen_id == citizen_id)).one()


def get_all_citizens_in_import(import_id):
    return session.query(Citizen).filter(Citizen.import_id == import_id).all()
