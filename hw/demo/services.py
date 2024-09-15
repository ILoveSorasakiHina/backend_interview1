import re
from abc import ABC, abstractmethod


class OrderValidator(ABC):
    @abstractmethod
    def validate(self, order_data):
        pass


class FormValidator(OrderValidator):
    def validate(self, order_data):
        required_fields = ['id', 'name', 'address', 'price', 'currency']
        address_required_fields = ['city', 'district', 'street']

        for field in required_fields:
            if field not in order_data:
                raise ValueError(f"缺少必要欄位: {field}")

        if not isinstance(order_data['id'], str):
            raise ValueError("訂單 ID 格式錯誤，必須是字串")

        if not isinstance(order_data['name'], str):
            raise ValueError("訂單名稱格式錯誤，必須是字串")

        if not isinstance(order_data['address'], dict):
            raise ValueError("地址格式錯誤，必須是物件")

        for field in address_required_fields:
            if field not in order_data['address']:
                raise ValueError(f"地址缺少必要欄位: {field}")
            if not isinstance(order_data['address'][field], str):
                raise ValueError(f"地址欄位 {field} 格式錯誤，必須是字串")

        if not isinstance(order_data['price'], str):
            raise ValueError("價格格式錯誤，必須是字串")

        if not isinstance(order_data['currency'], str):
            raise ValueError("貨幣格式錯誤，必須是字串")

        return True


class ContentValidator(OrderValidator):
    def validate(self, order_data):
        if not order_data['name'][0].isupper():
            raise ValueError("400-Name contains non English characters")
        if not bool(re.search(r'[^a-zA-Z]', order_data['name'])):
            raise ValueError("400-Name is not capitalized")

        try:
            price = int(order_data['price'])
            if price > 2000:
                raise ValueError("400-Price is over 2000")
        except ValueError:
            raise ValueError("400-Price format is wrong")

        if order_data['currency'] not in ["TWD", "USD"]:
            raise ValueError("400-Currency format is wrong")

        return True


class OrderConverter(ABC):
    @abstractmethod
    def convert(self, order_data):
        pass


class SimpleOrderConverter(OrderConverter):
    def convert(self, order_data):
        if order_data['currency'] == "USD":
            try:
                order_data['price'] = str(int(order_data['price']) * 31)
            except ValueError:
                raise ValueError("價格轉換失敗")
        return order_data


class OrderProcessor:
    def __init__(self, validators: list[OrderValidator], converter: OrderConverter):
        self.validators = validators
        self.converter = converter

    def process(self, order_data):
        for validator in self.validators:
            validator.validate(order_data)
        return self.converter.convert(order_data)
