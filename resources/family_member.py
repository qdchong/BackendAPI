from flask.globals import request
from flask_restful import Resource
from api.models import FamilyMember, HouseHold
import datetime
from http import HTTPStatus


class FamilyMemberResource(Resource):

    def put(self, household_id):
        """
        create a family member
        """

        # check if household exist
        household = HouseHold.get_by_id(household_id)
        if household is None:
            return {"msg": "Household not found. Please create a new household"}, HTTPStatus.NOT_FOUND

        # convert dob to datetime object
        dob_converted = date_time_obj = datetime.datetime.strptime(
            request.json['dob'], '%Y-%m-%d')

        if 'annualIncome' in request.json:
            annualIncome = request.json['annualIncome']
        else:
            annualIncome = 0
        if 'spouseName' in request.json:
            spouseName = request.json['spouseName'].title()
        else:
            spouseName = None

        new_member = FamilyMember(
            name=request.json['name'].title(),
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

    def delete(self, household_id):
        """
        delete a family member
        """
        # check if household exist
        household = HouseHold.get_by_id(household_id)
        if household is None:
            return {"msg": "Household not found"}, HTTPStatus.NOT_FOUND

        member_name = request.json['name'].title()

        family_member = FamilyMember.get_by_name(member_name)

        if family_member is None:
            return {"msg": "Family Member not found"}, HTTPStatus.NOT_FOUND

        family_member.delete()

        return {"msg": "{} from Household {}  has been deleted".format(member_name, household_id)}, HTTPStatus.OK
