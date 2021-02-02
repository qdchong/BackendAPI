from flask.globals import request
from flask_restful import Resource
from api.models import FamilyMember
import datetime
from http import HTTPStatus


class FamilyMemberResource(Resource):
    def put(self, household_id):
        # convert dob to datetime object
        dob_converted = date_time_obj = datetime.datetime.strptime(
            request.json['dob'], '%Y-%m-%d')
        new_member = FamilyMember(
            name=request.json['name'],
            gender=request.json['gender'],
            marital_status=request.json['maritalStatus'],
            spouse_name=request.json['spouseName'],
            occupation_type=request.json['occupationType'],
            annual_income=request.json['annualIncome'],
            dob=dob_converted,
            household_id=household_id
        )
        new_member.save()
        return (
            {
                "msg": "successfully created family member"

            },
            HTTPStatus.CREATED,
        )
