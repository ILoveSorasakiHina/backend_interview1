import json
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from .views import OrderView
from .services import FormValidator, ContentValidator, SimpleOrderConverter, OrderProcessor


class OrderViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = OrderView.as_view()

        self.form_validator = FormValidator()
        self.content_validator = ContentValidator()
        self.order_converter = SimpleOrderConverter()
        self.order_processor = OrderProcessor([self.form_validator, self.content_validator], self.order_converter)

    def test_valid_order(self):
        order_data = {
            'id': 'A123',
            'name': 'John Doe',
            'address': {
                'city': 'Taipei',
                'district': 'Zhongzheng',
                'street': 'Xinyi Road'
            },
            'price': '1000',
            'currency': 'USD'
        }
        request = self.factory.post('/api/orders', data=json.dumps(order_data), content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['price'], '31000')

    def test_invalid_order_missing_field(self):
        order_data = {
            'id': 'A123',
            'name': 'John Doe',
            'address': {
                'city': 'Taipei',
                'district': 'Zhongzheng'
                # Missing 'street'
            },
            'price': '1000',
            'currency': 'USD'
        }
        request = self.factory.post('/api/orders', data=json.dumps(order_data), content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], '地址缺少必要欄位: street')

    def test_invalid_order_invalid_price(self):
        order_data = {
            'id': 'A123',
            'name': 'John Doe',
            'address': {
                'city': 'Taipei',
                'district': 'Zhongzheng',
                'street': 'Xinyi Road'
            },
            'price': 'invalid_price',
            'currency': 'USD'
        }
        request = self.factory.post('/api/orders', data=json.dumps(order_data), content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], '400-Price format is wrong')

    def test_invalid_order_invalid_currency(self):
        order_data = {
            'id': 'A123',
            'name': 'John Doe',
            'address': {
                'city': 'Taipei',
                'district': 'Zhongzheng',
                'street': 'Xinyi Road'
            },
            'price': '1000',
            'currency': 'EUR'
        }
        request = self.factory.post('/api/orders', data=json.dumps(order_data), content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], '400-Currency format is wrong')

    def test_invalid_order_invalid_name(self):
        order_data = {
            'id': 'A123',
            'name': 'john doe',  # Lowercase name
            'address': {
                'city': 'Taipei',
                'district': 'Zhongzheng',
                'street': 'Xinyi Road'
            },
            'price': '1000',
            'currency': 'USD'
        }
        request = self.factory.post('/api/orders', data=json.dumps(order_data), content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], '400-Name contains non English characters')

    def test_invalid_order_with_extra_fields(self):
        order_data = {
            'id': 'A123',
            'name': 'John Doe',
            'address': {
                'city': 'Taipei',
                'district': 'Zhongzheng',
                'street': 'Xinyi Road'
            },
            'price': '1000',
            'currency': 'USD',
            'extra_field': 'extra_value'
        }
        request = self.factory.post('/api/orders', data=json.dumps(order_data), content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['price'], '31000')
