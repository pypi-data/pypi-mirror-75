from pip_services3_commons.convert.TypeCode import TypeCode
from pip_services3_commons.validate.ArraySchema import ArraySchema


class ProjectionParamsSchema(ArraySchema):
    def __init__(self):
        super().__init__(TypeCode.String)
