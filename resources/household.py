from flask.globals import request
from flask_restful import Resource
from sqlalchemy.sql.expression import and_, null
from api.models import HouseHold, FamilyMember
from http import HTTPStatus
import datetime
import dateutil.relativedelta
from sqlalchemy import func
import operator
import itertools


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


class StudentEncouragementBonusResource(Resource):

    def get(self):
        """ List households and qualifying family members for Student Encouragement Bonus
        -Children less than 16 years old
        -Household income less than $150,000
        """
        data = []
        household_list = []
        household_details_dict = {}
        family_member_details_dict = {}
        family_members_list = []

        # Get URL Search Parameters ------ Start
        request_args_dict = request.args.to_dict()
        # get income limit
        if 'income-limit' in request_args_dict:
            income_limit_param = request_args_dict['income-limit']
        else:
            income_limit_param = None

        # get age limit
        if 'age-limit' in request_args_dict:
            age_limit_param = request_args_dict['age-limit']
        else:
            age_limit_param = None
        # Get URL Search Parameteres -------End

        # convert age limit to datetime object
        date_limit = datetime.date.today(
        ) - dateutil.relativedelta.relativedelta(years=int(age_limit_param))

        # query for income limit
        sub_q = FamilyMember.query.with_entities(FamilyMember.household_id, func.sum(
            FamilyMember.annual_income)).group_by(FamilyMember.household_id).having(func.sum(
                FamilyMember.annual_income) < int(income_limit_param)).subquery()

        # get qualifying family members
        query_result = FamilyMember.query.filter(FamilyMember.dob > date_limit).join(
            sub_q, FamilyMember.household_id == sub_q.c.household_id).all()

        for x in query_result:
            dictrect = x.__dict__
            dictrect.pop('_sa_instance_state', None)
            data.append(dictrect)

        # group qualifying members
        data = sorted(data, key=operator.itemgetter("household_id"))
        outputList = []
        for i, g in itertools.groupby(data, key=operator.itemgetter("household_id")):
            outputList.append(list(g))

        for i in range(0, len(outputList)):

            # get household Type
            household_type = HouseHold.query.get(
                outputList[i][0]['household_id']).type

            # populate family member details
            for k in range(0, len(outputList[i])):
                family_member_details_dict = {
                    "Name": outputList[i][k]['name'],
                    "Gender": outputList[i][k]['gender'],
                    "MaritalStatus": outputList[i][k]['marital_status'],
                    **({"Spouse": outputList[i][k]['spouse_name'].title()} if outputList[i][k]['spouse_name'] else {}),
                    "OccupationType": outputList[i][k]['occupation_type'],
                    "AnnualIncome": str(outputList[i][k]['annual_income']),
                    "DOB": str(outputList[i][k]['dob'])
                }
                family_members_list.append(family_member_details_dict)

            household_details_dict = {
                "HouseholdId": outputList[i][0]['household_id'],
                "HouseholdType": household_type,
                "FamilyMembers": family_members_list
            }
            # clear family details in list
            family_members_list = []
            household_list.append(household_details_dict)

        return (
            {
                "data": household_list

            },
            HTTPStatus.OK,
        )


class FamilyTogethernessSchemeResource(Resource):

    def get(self):
        """ List households and qualifying family members for Family Togetherness Bonus
        -Household with husband and wife
        -Has children younger than 18 years old
        """
        family_members_list = []
        data = []

        # Get URL Search Parameters ------ Start
        request_args_dict = request.args.to_dict()

        # get age limit
        if 'age-limit' in request_args_dict:
            age_limit_param = request_args_dict['age-limit']
        else:
            age_limit_param = None

        # get husband & wife
        if 'has-husband-wife' in request_args_dict:
            has_husband_wife_param = request_args_dict['has-husband-wife']
        else:
            has_husband_wife_param = None

        # Get URL Search Parameters ------ End

        # convert age limit to datetime object
        date_limit = datetime.date.today(
        ) - dateutil.relativedelta.relativedelta(years=int(age_limit_param))

        # query for household with husband and wife
        if has_husband_wife_param:
            sub_q = FamilyMember.query.with_entities(FamilyMember.household_id).filter(
                FamilyMember.spouse_name.isnot(None)).group_by(FamilyMember.household_id).having(func.count(FamilyMember.spouse_name) > 1).subquery()

        # get qualifying family members
        query_result = FamilyMember.query.with_entities(FamilyMember.household_id, HouseHold).filter(FamilyMember.dob > date_limit).join(
            sub_q, FamilyMember.household_id == sub_q.c.household_id).group_by(FamilyMember.household_id).join(HouseHold).all()

        if query_result:
            for household in query_result:
                for detail in household[1].family:
                    family_members_list = generateFamilyMembersDict(
                        household[1].family)
                household_details_dict = {
                    "HouseholdId": household[1].id,
                    "HouseholdType": household[1].type,
                    "FamilyMembers": family_members_list
                }
                # clear family details in list
                family_members_list = []
                data.append(household_details_dict)
            return {"data": data}, HTTPStatus.OK
        return {"msg": "no households found"}, HTTPStatus.BAD_REQUEST


class ElderBonusResource(Resource):

    def get(self):
        """ List households and qualifying family members for Elder Bonus
        - HDB Household family members above age of 50
        """
        # Get URL Search Parameters ------ Start
        request_args_dict = request.args.to_dict()

        # get age limit
        if 'age-limit' in request_args_dict:
            age_limit_param = request_args_dict['age-limit']
        else:
            age_limit_param = None

        # get household Type
        if 'household-type' in request_args_dict:
            household_type_param = request_args_dict['household-type']
        else:
            household_type_param = None

        # Get URL Search Parameters ------ End

        # convert age limit to datetime object
        date_limit = datetime.date.today(
        ) - dateutil.relativedelta.relativedelta(years=int(age_limit_param))

        # query households based on household type param
        query = HouseHold.query.filter(
            HouseHold.type == household_type_param.upper())

        print(query.all())
