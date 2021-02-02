from flask_restful import Api, Resource


class DefaultResource(Resource):

    def get(self):
        return {
            "status": "success",
            "data": {
                "msg": "Take Home Assignment"
            }
        }
