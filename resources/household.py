from flask.globals import request
from flask_restful import Resource
from api.models import HouseHold
from http import HTTPStatus


def generateFamilyMembersDict(household_obj):

    family_member_details_dict = {}
    family_members_list = []
    for detail in household_obj:
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
    return family_members_list


class HouseHoldListResource(Resource):

    def get(self):
        """ List All Household
        """
        household_details_dict = {}
        family_member_details_dict = {}
        family_members_list = []
        data = []
        query_result = HouseHold.query.all()
        if query_result:
            for household in query_result:
                family_members_list = generateFamilyMembersDict(
                    household.family)
                household_details_dict = {
                    "HouseholdId": household.id,
                    "HouseholdType": household.type,
                    "FamilyMembers": family_members_list
                }
                data.append(household_details_dict)
            return {"data": data}, HTTPStatus.OK
        return {"msg": "no households found"}, HTTPStatus.BAD_REQUEST

    def post(self):
        """Create a Household
        """
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


class HouseHoldResource(Resource):

    def get(self, household_id):
        """
        Get details of a household
        """
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

    def delete(self, household_id):
        """
        delete a household
        """
        # get household by id
        household = HouseHold.get_by_id(household_id)

        # check if household exist
        if household is None:
            return {"msg": "Household not found"}, HTTPStatus.NOT_FOUND

        household.delete()

        return {"msg": "Household has been deleted"}, HTTPStatus.OK
