from flask_restful import Resource
from api.models import HouseHold, FamilyMember
from http import HTTPStatus
import datetime
import dateutil.relativedelta
from sqlalchemy import func
import operator
import itertools
from webargs.flaskparser import use_args
from webargs import fields


def generateHouseholdsDict(household_obj):

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


def generateFamilyMembersDict(members_list):
    """
    Return a list of family members and households group into specific households
    """

    family_members_list = []
    household_list = []
    for i in range(0, len(members_list)):

        # get household Type
        household_type = HouseHold.query.get(
            members_list[i][0]['household_id']).type

        # populate family member details
        for k in range(0, len(members_list[i])):
            family_member_details_dict = {
                "Name": members_list[i][k]['name'],
                "Gender": members_list[i][k]['gender'],
                "MaritalStatus": members_list[i][k]['marital_status'],
                **({"Spouse": members_list[i][k]['spouse_name'].title()} if members_list[i][k]['spouse_name'] else {}),
                "OccupationType": members_list[i][k]['occupation_type'],
                "AnnualIncome": str(members_list[i][k]['annual_income']),
                "DOB": str(members_list[i][k]['dob'])
            }
            family_members_list.append(family_member_details_dict)

        household_details_dict = {
            "HouseholdId": members_list[i][0]['household_id'],
            "HouseholdType": household_type,
            "FamilyMembers": family_members_list
        }
        # clear family details in list
        family_members_list = []
        household_list.append(household_details_dict)
    return household_list


class StudentEncouragementBonusResource(Resource):

    grant_args = {
        'income_limit': fields.Decimal(required=True),
        'age_limit': fields.Int(required=True),
    }

    @use_args(grant_args, location="query")
    def get(self, args):
        """ List households and qualifying family members for Student Encouragement Bonus
        -Children less than 16 years old
        -Household income less than $150,000
        """
        data = []
        household_list = []
        household_details_dict = {}
        family_member_details_dict = {}
        family_members_list = []

        age_limit_param = args['age_limit']
        income_limit_param = args['income_limit']
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
            result_dict = x.__dict__
            result_dict.pop('_sa_instance_state', None)
            data.append(result_dict)

        # group qualifying members
        data = sorted(data, key=operator.itemgetter("household_id"))
        outputList = []
        for i, g in itertools.groupby(data, key=operator.itemgetter("household_id")):
            outputList.append(list(g))

        household_list = generateFamilyMembersDict(outputList)

        return (
            {
                "data": household_list

            },
            HTTPStatus.OK,
        )


class FamilyTogethernessSchemeResource(Resource):

    grant_args = {
        'has_husband_wife': fields.Bool(required=True),
        'age_limit': fields.Int(required=True),
    }

    @use_args(grant_args, location='query')
    def get(self, args):
        """ List households and qualifying family members for Family Togetherness Bonus
        -Household with husband and wife
        -Has children younger than 18 years old
        """
        family_members_list = []
        data = []

        age_limit_param = args['age_limit']
        has_husband_wife = args['has_husband_wife']

        # convert age limit to datetime object
        date_limit = datetime.date.today(
        ) - dateutil.relativedelta.relativedelta(years=int(age_limit_param))

        # query to select members below age limit
        children_sub_q = FamilyMember.query.with_entities(FamilyMember.household_id).filter(
            FamilyMember.dob > date_limit).group_by(FamilyMember.household_id)

        # query to select husband and wife
        spouse_sub_q = FamilyMember.query.with_entities(FamilyMember.household_id).filter(
            FamilyMember.spouse_name != None).group_by(FamilyMember.household_id).having(func.count(
                FamilyMember.spouse_name) > 1)

        # query to exclude non-married members older than age limit
        older_sub_q = FamilyMember.query.with_entities(
            FamilyMember.name).filter((FamilyMember.dob <= date_limit) & FamilyMember.spouse_name == None)

        if has_husband_wife:
            query_result = FamilyMember.query.filter(
                FamilyMember.household_id.in_(children_sub_q) & FamilyMember.household_id.in_(spouse_sub_q) & ~FamilyMember.name.in_(older_sub_q))

        for x in query_result:
            result_dict = x.__dict__
            result_dict.pop('_sa_instance_state', None)
            data.append(result_dict)

        # group qualifying members based on household id
        data = sorted(data, key=operator.itemgetter("household_id"))
        outputList = []
        for i, g in itertools.groupby(data, key=operator.itemgetter("household_id")):
            outputList.append(list(g))

        household_list = generateFamilyMembersDict(outputList)

        return (
            {
                "data": household_list

            },
            HTTPStatus.OK,
        )


class ElderBonusResource(Resource):

    grant_args = {
        'household_type': fields.Str(required=True),
        'age_limit': fields.Int(required=True),
    }

    @ use_args(grant_args, location='query')
    def get(self, args):
        """ List households and qualifying family members for Elder Bonus
        - HDB Household family members above age of 50
        """

        data = []
        household_list = []

        age_limit_param = args['age_limit']
        household_type_param = args['household_type']

        # convert age limit to datetime object
        date_limit = datetime.date.today(
        ) - dateutil.relativedelta.relativedelta(years=int(age_limit_param))

        # query households based on household type param
        sub_q = HouseHold.query.with_entities(HouseHold.id).filter(
            HouseHold.type == household_type_param.upper()).subquery()

        # get qualifying family members
        query_result = FamilyMember.query.filter(FamilyMember.dob <= date_limit).join(
            sub_q, FamilyMember.household_id == sub_q.c.id).group_by(FamilyMember.name, FamilyMember.household_id).all()

        for x in query_result:
            result_dict = x.__dict__
            result_dict.pop('_sa_instance_state', None)
            data.append(result_dict)

        # group qualifying members based on household id
        data = sorted(data, key=operator.itemgetter("household_id"))
        outputList = []
        for i, g in itertools.groupby(data, key=operator.itemgetter("household_id")):
            outputList.append(list(g))

        household_list = generateFamilyMembersDict(outputList)

        return (
            {
                "data": household_list

            },
            HTTPStatus.OK,
        )


class BabySunshineGrantResource(Resource):

    grant_args = {
        'age_limit': fields.Int(required=True),
    }

    @ use_args(grant_args, location='query')
    def get(self, args):
        """ List households and qualifying family members for Baby Sunshine Grant
        - with young children younger than 5
        """
        data = []
        household_list = []

        age_limit_param = args['age_limit']

        # convert age limit to datetime object
        date_limit = datetime.date.today(
        ) - dateutil.relativedelta.relativedelta(years=int(age_limit_param))

        # get qualifying family members
        query_result = FamilyMember.query.filter(FamilyMember.dob > date_limit).group_by(
            FamilyMember.name, FamilyMember.household_id).all()
        if query_result:
            for x in query_result:
                result_dict = x.__dict__
                result_dict.pop('_sa_instance_state', None)
                data.append(result_dict)

            # group qualifying members based on household id
            data = sorted(data, key=operator.itemgetter("household_id"))
            outputList = []
            for i, g in itertools.groupby(data, key=operator.itemgetter("household_id")):
                outputList.append(list(g))

            household_list = generateFamilyMembersDict(outputList)

            return (
                {
                    "data": household_list

                },
                HTTPStatus.OK,
            )
        return {"msg": "no households found"}, HTTPStatus.BAD_REQUEST


class YOLOGSTGrantResource(Resource):

    grant_args = {
        'household_type': fields.Str(required=True),
        'income_limit': fields.Decimal(required=True),
    }

    @ use_args(grant_args, location='query')
    def get(self, args):
        """ List households and qualifying family members for YOLO GST Grant
        - HDB with annual income less than $100,000
        """

        data = []
        family_members_list = []
        household_details_dict = []
        income_limit_param = args['income_limit']
        household_type_param = args['household_type']

        # query households based on household type param
        sub_q = HouseHold.query.with_entities(HouseHold.id).filter(
            HouseHold.type == household_type_param).subquery()

        # query for income limit
        query_result = FamilyMember.query.with_entities(FamilyMember.id, HouseHold).group_by(FamilyMember.household_id).having(func.sum(
            FamilyMember.annual_income) < int(income_limit_param)).join(sub_q, FamilyMember.household_id == sub_q.c.id).join(HouseHold).all()
        if query_result:
            for household in query_result:
                family_members_list = generateHouseholdsDict(
                    household[1].family)
                household_details_dict = {
                    "HouseholdId": household[1].id,
                    "HouseholdType": household[1].type,
                    "FamilyMembers": family_members_list
                }
                data.append(household_details_dict)

            return {"data": data}, HTTPStatus.OK
        return {"msg": "no households found"}, HTTPStatus.BAD_REQUEST
