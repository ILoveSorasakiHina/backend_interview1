import json
from django.http import JsonResponse
from django.views import View
from .services import FormValidator, ContentValidator, SimpleOrderConverter, OrderProcessor

form_validator = FormValidator()
content_validator = ContentValidator()
order_converter = SimpleOrderConverter()
order_processor = OrderProcessor([form_validator, content_validator], order_converter)


class OrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            order_data = json.loads(request.body.decode('utf-8'))

            processed_order = order_processor.process(order_data)

            return JsonResponse(processed_order, status=200)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': '500-' + str(e)}, status=500)
