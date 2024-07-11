from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "200",
            "currency": "TWD"
        }

    # 成功案例
    def test_create_valid_order(self):
        response = self.client.post(
            reverse('order'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # 失敗案例 - 名稱包含非英文字符
    def test_create_order_with_non_english_name(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['name'] = "Melody 旅館"
        response = self.client.post(
            reverse('order'),
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Name contains non-English characters")
    
    # 失敗案例 - 名稱不是首字母大寫
    def test_create_order_with_name_not_capitalized(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['name'] = "melody holiday inn"
        response = self.client.post(
            reverse('order'),
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Name is not capitalized")
    
    # 失敗案例 - 價格超過2000
    def test_create_order_with_price_over_2000(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['price'] = "3000"
        response = self.client.post(
            reverse('order'),
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Price is over 2000")
    
    # 失敗案例 - 貨幣格式錯誤
    def test_create_order_with_wrong_currency_format(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['currency'] = "EUR"
        response = self.client.post(
            reverse('order'),
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Currency format is wrong")
    
    # 成功案例 - 貨幣為USD時，轉換價格並修改貨幣為TWD
    def test_create_order_with_usd_currency(self):
        valid_payload = self.valid_payload.copy()
        valid_payload['currency'] = "USD"
        valid_payload['price'] = "100"
        response = self.client.post(
            reverse('order'),
            data=valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['price'], '3100.00')
        self.assertEqual(response.data['currency'], "TWD")
