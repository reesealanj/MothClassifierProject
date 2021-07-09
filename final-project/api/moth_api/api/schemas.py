import os

from drf_yasg.generators import OpenAPISchemaGenerator


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=True):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.basePath = os.path.join(schema.basePath, 'api/v1')
        return schema
