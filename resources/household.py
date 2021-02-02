from flask.globals import request
from flask_restful import Resource
from api.models import HouseHold
from http import HTTPStatus


class HouseHoldListResource(Resource):
    # list all households
    def get(self):
        household_list = HouseHold.query.all()
        print(household_list)

        if household_list:
            for household in household_list:
                print(household.to_dict())
        #        data.append(household.data())
        return {"data": "test"}, HTTPStatus.OK
        # return {"msg": "no households available"}, HTTPStatus.BAD_REQUEST

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
