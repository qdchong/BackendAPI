from flask.globals import request
from flask_restful import Resource
from api.models import FamilyMember, HouseHold
import datetime
from http import HTTPStatus


class FamilyMemberResource(Resource):
    # get family members details
    def get(self, household_id):
        family_members_list = []
        query_result = HouseHold.query.get(household_id)
        if query_result:
            household_type = query_result.type
            household_id = query_result.id
            for detail in query_result.family:
                family_member_details_dict = {
                    "Name": detail.name.title(),
                    "Gender": detail.gender,
                    "MaritalStatus": detail.marital_status,
                    **({"Spouse": detail.spouse_name.title()} if detail.spouse_name else {}),
                    "OccupationType": detail.occupation_type,
                    "AnnualIncome": str(detail.annual_income),
                    "DOB": str(detail.dob)
                }
                family_members_list.append(family_member_details_dict)
            data = {
                "HouseholdId": household_id,
                "HouseholdType": household_type,
                "FamilyMembers": family_members_list
            }

            return (
                {
                    'data': data
                },
                HTTPStatus.OK,
            )

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
