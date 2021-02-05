from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from api.models import db
from api.config import env_config
from webargs.flaskparser import abort, parser
from resources.household import HouseHoldListResource, HouseHoldResource
from resources.family_member import FamilyMemberResource
from resources.grant import StudentEncouragementBonusResource, \
    FamilyTogethernessSchemeResource, ElderBonusResource, BabySunshineGrantResource, YOLOGSTGrantResource

api = Api()


def create_app(config_name):

    import resources

    app = Flask(__name__)

    app.config.from_object(env_config[config_name])

    db.init_app(app)

    Migrate(app, db, render_as_batch=True)

    api.init_app(app)

    @parser.error_handler
    def handle_request_parsing_error(err, req, schema, *, error_status_code,
                                     error_headers):
        """webargs error handler that uses Flask-RESTful's abort function to   
        return
        a JSON error response to the client.
        """
        abort(error_status_code, errors=err.messages)

    return app


# register url
api.add_resource(HouseHoldListResource, "/api/v1/households",
                 endpoint="households_list")

api.add_resource(HouseHoldResource,
                 "/api/v1/households/<int:household_id>", endpoint="households")

api.add_resource(FamilyMemberResource,
                 "/api/v1/households/<int:household_id>/family_members", endpoint="family_members")

api.add_resource(StudentEncouragementBonusResource,
                 "/api/v1/households/grants/student_encouragement_bonus", endpoint="student_bonus")

api.add_resource(FamilyTogethernessSchemeResource,
                 "/api/v1/households/grants/family_together_scheme", endpoint="family_scheme")

api.add_resource(ElderBonusResource,
                 "/api/v1/households/grants/elder_bonus", endpoint="elder_bonus")
api.add_resource(BabySunshineGrantResource,
                 "/api/v1/households/grants/baby_sunshine_grant", endpoint="baby_grant")
api.add_resource(YOLOGSTGrantResource,
                 "/api/v1/households/grants/yolo_gst_grant", endpoint="yolo_grant")
