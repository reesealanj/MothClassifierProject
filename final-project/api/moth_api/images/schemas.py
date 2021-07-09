from drf_yasg.inspectors import SwaggerAutoSchema


class ZipAutoSchema(SwaggerAutoSchema):
    def get_produces(self):
        return ['application/zip']

    def get_consumes(self):
        return ['application/zip']
