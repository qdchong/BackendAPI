from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from api.models import db
from api.config import env_config
from resources.household import HouseHoldListResource
from resources.family_member import FamilyMemberResource

api = Api()


def create_app(config_name):

    import resources

    app = Flask(__name__)

    app.config.from_object(env_config[config_name])

    db.init_app(app)

    Migrate(app, db)

    api.init_app(app)

    return app


# register url
api.add_resource(HouseHoldListResource, "/api/v1/households",
                 endpoint="households")

api.add_resource(FamilyMemberResource,
                 "/api/v1/households/<int:household_id>/family-members", endpoint="family-members")
