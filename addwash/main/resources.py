from import_export import resources
from .models import Request


class RequestResource(resources.ModelResource):
    class Meta:
        model = Request
