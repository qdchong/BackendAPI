from flask.globals import request
from flask_restful import Resource
from api.models import HouseHold
from http import HTTPStatus


class HouseHoldListResource(Resource):
    # list all households
    def get(self):
        household_details_dict = {}
        family_member_details_dict = {}
        family_members_list = []
        data = []
        query_result = HouseHold.query.all()
        if query_result:
            for household in query_result:
                for detail in household.family:
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

                household_details_dict = {
                    "HouseholdType": household.type,
                    "FamilyMembers": family_members_list
                }
                # clear family details in list
                family_members_list = []
                data.append(household_details_dict)
            return {"data": data}, HTTPStatus.OK
        return {"msg": "no households found"}, HTTPStatus.BAD_REQUEST

    # create a household
    def post(self):
        new_household = HouseHold(
            type=request.json['housingType']
        )
        new_household.save()
        return (
            {
                "msg": "successfully created household"

            },
            HTTPStatus.CREATED,
        )
