# Order Checker API
## 介紹
這是一個基於Django框架的API專案，用於檢查和轉換訂單格式。API包含一個POST endpoint **/api/orders**，該端點接收特定格式的JSON輸入，並根據預定義的檢查和轉換規則進行處理。
## 特性
- 檢查訂單名稱是否包含非英文字符並首字母大寫
- 檢查訂單價格是否超過2000
- 檢查貨幣格式是否正確，並在需要時進行轉換
- 包含詳細的單元測試
- 使用Docker封裝環境，方便部署
## 設計原則與設計模式
### SOLID 原則
- 單一職責原則 (Single Responsibility Principle, SRP)：
  每個類別或模組只有一個變更的原因。OrderSerializer和OrderView各自處理特定的任務：序列化和反序列化數據，以及處理HTTP請求。
## 使用方法
### 環境設置
1. Clone repository
2. 建立並啟動Docker容器
```bash
docker-compose up --build
```
3. 運行單元測試
```bash
docker-compose run web python manage.py test
```