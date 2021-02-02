from flask.globals import request
from flask_restful import Resource
from api.models import FamilyMember
import datetime
from http import HTTPStatus


class FamilyMemberResource(Resource):
    # create family member
    def put(self, household_id):
        # convert dob to datetime object
        dob_converted = date_time_obj = datetime.datetime.strptime(
            request.json['dob'], '%Y-%m-%d')

        if 'annualIncome' in request.json:
            annualIncome = request.json['annualIncome']
        else:
            annualIncome = 0
        if 'spouseName' in request.json:
            spouseName = request.json['spouseName']
        else:
            spouseName = None
        new_member = FamilyMember(
            name=request.json['name'],
            gender=request.json['gender'],
            marital_status=request.json['maritalStatus'],
            spouse_name=spouseName,
            occupation_type=request.json['occupationType'],
            annual_income=annualIncome,
            dob=dob_converted,
            household_id=household_id
        )
        result_status = new_member.save()
        if result_status is not None:
            return {"msg": result_status}, HTTPStatus.BAD_REQUEST

        return (
            {
                'msg': 'successfully created family member'

            },
            HTTPStatus.CREATED,
        )
