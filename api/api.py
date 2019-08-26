import datetime
from collections import defaultdict

from flask import Flask, jsonify, request, abort
from models.db import session
from models.queries import get_one_citizen_by_unique_pair, get_all_citizens_in_import
from models.citizen_data import Citizen
from models.citizen_data import Gender
from models.imports import Import

from schemas.schemas import ImportSchema, UpdateCitizenSchema

app = Flask(__name__)


@app.route("/imports", methods=['POST'])
def upload_import():
    schema = ImportSchema()
    json_import = request.get_json(force=True)

    errors = schema.validate(json_import)
    if errors:
        print(errors)
        abort(400)

    citizens_list = []

    for node in json_import['citizens']:
        print(node)
        citizens_list.append(Citizen(node))
    new_import = Import(citizens=citizens_list)
    session.add(new_import)
    session.add_all(citizens_list)
    session.commit()

    for node, citizen in zip(json_import['citizens'], citizens_list):
        relatives = node['relatives']
        print(relatives)
        for relative in relatives:
            print(relative)
            relative_citizens = get_one_citizen_by_unique_pair(new_import.id, relative)
            citizen.relatives.append(relative_citizens)
    session.commit()

    response = jsonify({"data": {"import_id": new_import.id}})
    response.status_code = 201
    return response


@app.route("/imports/<import_id>/citizens/<citizen_id>", methods=['PATCH'])
def update_citizen_in_import(import_id, citizen_id):
    schema = UpdateCitizenSchema()
    json_citizen = request.get_json(force=True)
    errors = schema.validate(json_citizen, partial=True)

    if errors or not json_citizen:
        print(errors)
        abort(400)

    citizen = get_one_citizen_by_unique_pair(import_id, citizen_id)

    for key, value in json_citizen.items():
        if key == "relatives":
            if value:
                for node in value:
                    relative = get_one_citizen_by_unique_pair(import_id, node)
                    citizen.relatives.append(relative)
                    relative.relatives.append(citizen)
            else:
                for relative in citizen.relatives:
                    print('RELATIVES BEFORE {}'.format(relative.relatives))
                    new_relatives = list(filter(lambda r: r.citizen_id != citizen.citizen_id, relative.relatives))
                    print('RELATIVES AFTER '.format(new_relatives))
                    relative.relatives = new_relatives
                citizen.relatives = []
        elif key == "birth_date":
            setattr(citizen, key, datetime.datetime.strptime(value, '%d.%m.%Y'))
        elif key == "gender":
            setattr(citizen, key, Gender(value).name)
        else:
            setattr(citizen, key, value)
    session.commit()

    print(citizen.as_dict())

    response = jsonify({"data": citizen.as_dict()})
    response.status_code = 200
    return response


@app.route("/imports/<import_id>/citizens", methods=['GET'])
def get_all_citizens_from_import(import_id):
    citizens = get_all_citizens_in_import(import_id)

    citizens_list = []

    for citizen in citizens:
        citizens_list.append(citizen.as_dict())

    response = jsonify({"data": citizens_list})
    response.status_code = 200
    return response


@app.route("/imports/<import_id>/citizens/birthdays", methods=['GET'])
def get_birthdays_presents_by_month(import_id):
    presents_per_month_all_citizens = {m: [] for m in range(1, 13)}

    citizens = get_all_citizens_in_import(import_id)

    for citizen in citizens:
        presents_per_month_citizen = defaultdict(int)
        print(citizen.relatives)
        for relative in citizen.relatives:
            presents_per_month_citizen[relative.birth_date.month] += 1
        print(presents_per_month_citizen)
        for month, presents_count in presents_per_month_citizen.items():
            data = {"citizen_id": citizen.citizen_id, "presents": presents_count}
            presents_per_month_all_citizens[month].append(data)

    response = jsonify({"data": presents_per_month_all_citizens})
    response.status_code = 200
    return response
