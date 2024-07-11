from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
import re

class OrderView(APIView):
    def post(self, request):
        data = request.data
        
        # 檢查name是否包含非英文字符
        if re.search('[^a-zA-Z ]', data.get('name', '')):
            return Response({"error": "Name contains non-English characters"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查name是否首字母大寫
        if not data.get('name', '').istitle():
            return Response({"error": "Name is not capitalized"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查currency格式
        if data.get('currency') not in ['TWD', 'USD']:
            return Response({"error": "Currency format is wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查price是否超過2000
        if float(data.get('price', 0)) > 2000:
            return Response({"error": "Price is over 2000"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 當貨幣為USD時，將price乘以31並修改currency為TWD
        if data.get('currency') == 'USD':
            data['price'] = float(data['price']) * 31
            data['currency'] = 'TWD'
        
        for t in data['address'].keys():
            data[t] = data['address'][t]

        data.pop('address')
        
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
