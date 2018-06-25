from json import loads
from json.decoder import JSONDecodeError

from django.http import JsonResponse


class JSONResponseMixin:

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(context, **response_kwargs)

    def render_to_json_success_response(self, **data):
        return self.render_to_json_response({
            'status': 'ok',
            **data
        })

    def render_to_json_error_response(self, message='Bad request', status=200):
        return self.render_to_json_response(
            {
                'status': 'error',
                'message': message
            },
            status=status,
        )


class JSONDecodeMixin(JSONResponseMixin):

    def dispatch(self, request, *args, **kwargs):
        try:
            self._json = loads(request.body.decode('utf-8'))
        except JSONDecodeError:
            return self.render_to_json_error_response(
                message='Request decoding error', status=400
            )
        return super().dispatch(request, *args, **kwargs)
