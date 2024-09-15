# 訂單處理 API

## 概述

此專案實現了一個訂單格式驗證與轉換的 REST API，它提供了一個 `/api/orders` 的端點，用於接收 POST 請求並處理訂單數據。該 API 對訂單數據進行驗證、處理並返回結果。專案使用了 Django 和 Docker。

## 端點

### POST /api/orders

**請求範例：**

```json
{
    "id": "123",
    "name": "John Doe",
    "address": {
        "city": "Taipei",
        "district": "Xinyi",
        "street": "123 Main St"
    },
    "price": "1500",
    "currency": "USD"
}

```

**成功回應範例：**



```json

{
    "id": "123",
    "name": "John Doe",
    "address": {
        "city": "Taipei",
        "district": "Xinyi",
        "street": "123 Main St"
    },
    "price": "46500",
    "currency": "TWD"
}

```
## 設計與架構

**SOLID 原則**

1. **單一職責原則 (SRP: Single Responsibility Principle)**

   **解釋**: 每個類別應該只有一個改變的原因，即只有一種職責。換句話說，類別應該只有一個功能。

   **在此專案中的應用**:
   - `FormValidator` 只負責驗證訂單的表單字段是否符合要求。
   - `ContentValidator` 只負責驗證訂單內容的正確性。
   - `SimpleOrderConverter` 只負責將訂單的價格從美元轉換為台幣。

   **為什麼重要**: 將職責分開可以讓每個類別變得更簡單、更專注，這樣也使得類別更容易測試和維護。

2. **開放封閉原則 (OCP: Open/Closed Principle)**

   **解釋**: 程式碼應該對擴展開放，對修改封閉。這意味著你應該能夠擴展系統的功能，而不需要改變現有的代碼。

   **在此專案中的應用**:
   - 如果需要新增其他的驗證方式或轉換方式，可以通過繼承和實現新的 `OrderValidator` 或 `OrderConverter` 類別來達成，而無需修改 `OrderProcessor` 類別。

   **為什麼重要**: 遵循這個原則能夠讓系統更靈活，並且減少對現有代碼的破壞性改動。

3. **里氏替換原則 (LSP: Liskov Substitution Principle)**

   **解釋**: 派生類別應該能夠替換掉它們的父類而不會影響程序的正確性。這意味著子類別應該能夠在任何需要父類的地方被替代。

   **在此專案中的應用**:
   - `FormValidator` 和 `ContentValidator` 可以替換 `OrderValidator` 父類，`SimpleOrderConverter` 可以替換 `OrderConverter` 父類，並且 `OrderProcessor` 可以正常工作而不會出現錯誤。

   **為什麼重要**: 確保派生類別遵守父類的協議，使得系統更容易擴展和維護。

4. **接口隔離原則 (ISP: Interface Segregation Principle)**

   **解釋**: 不應該強迫類別依賴於它們不需要的接口。換句話說，應該把大接口拆分成多個小接口，每個接口專注於一個功能。

   **在此專案中的應用**:
   - `OrderValidator` 和 `OrderConverter` 分別定義了驗證和轉換的方法。這樣 `OrderProcessor` 只需要依賴於這些接口，而不需要知道它們的具體實現細節。

   **為什麼重要**: 確保類別只實現它們實際需要的方法，避免過度依賴不需要的功能，減少類別之間的耦合度。

5. **依賴反轉原則 (DIP: Dependency Inversion Principle)**

   **解釋**: 解除高階模組與低階模組的耦合關係，高階模組不應該依賴於低階模組，兩者都該依賴抽象。抽象不應該依賴於具體實作方式，具體實作方式則應該依賴抽象。

   **在此專案中的應用**:
   - `OrderProcessor` 類別依賴於 `OrderValidator` 和 `OrderConverter` 的接口，而不是具體的實現類別。這樣可以在不改變 `OrderProcessor` 類別的情況下替換或新增驗證器和轉換器。

   **為什麼重要**: 使系統的高層模組和低層模組之間的依賴關係變得更靈活，減少了修改一部分代碼對其他部分的影響。

**設計模式**

1. **策略模式 (Strategy Pattern)**

   **解釋**: 定義一系列的演算法，並且把這些算法，用接口封裝到有公共接口的策略類中，使他們可以互相替換。

   **在此專案中的應用**:
   - `OrderProcessor` 使用策略模式來選擇和應用不同的驗證和轉換策略。你可以在 `OrderProcessor` 中輕鬆替換或新增驗證器和轉換器，而不需要修改 `OrderProcessor` 的實現。

   **為什麼重要**: 提供了一種靈活的方式來切換和擴展算法，並且使系統的功能更具可擴展性。

2. **抽象工廠模式 (Abstract Factory Pattern)**

   **解釋**: 抽象工廠模式提供了一個接口，用於創建一系列相關或依賴的對象，而不需要指定它們的具體類別。

   **在此專案中的應用**:
   - `OrderProcessor` 依賴於 `OrderValidator` 和 `OrderConverter` 的抽象類別，這樣可以創建和使用具體的驗證器和轉換器實現，而不需要關心其具體類別。

   **為什麼重要**: 確保可以靈活地創建和使用一組相關對象，並且使系統能夠應對未來的擴展和變更。

## 設置與安裝

### 先決條件

- Docker
- Docker Compose

### 安裝步驟

1. **克隆儲存庫**

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **構建 Docker 映像檔**

    ```bash
    docker build -t order-processing-api -f test.Dockerfile .
    ```

3. **運行 Docker 容器**

    ```bash
    docker run -p 8000:8000 order-processing-api
    ```

4. **訪問 API**

    API 將在 [http://localhost:8000/api/orders](http://localhost:8000/api/orders) 可用。

### 測試

要運行測試，請確保您在虛擬環境中，然後使用：

```bash
coverage run --source='.' manage.py test
coverage report

```

## 資料庫題目

1. 

    ```SQL

        SELECT
            b.id AS bnb_id,
            b.name AS bnb_name,
            SUM(o.amount) AS may_amount
        FROM
            orders o
        JOIN
            bnbs b ON o.bnb_id = b.id
        WHERE
            o.currency = 'TWD'
            AND o.created_at BETWEEN '2023-05-01' AND '2023-05-31'
        GROUP BY
            b.id, b.name
        ORDER BY
            may_amount DESC
        LIMIT 10;

    ```

2. 可以分成兩個問題:
    1. 如何確認是否優化?
        這問題其實就是如何確認運行時間，我們可以使用EXPLAIN ANALYZE。
        ```SQL
            EXPLAIN ANALYZE
            SELECT
                b.id AS bnb_id,
                b.name AS bnb_name,
                SUM(o.amount) AS may_amount
            FROM
                orders o
            JOIN
                bnbs b ON o.bnb_id = b.id
            WHERE
                o.currency = 'TWD'
                AND o.created_at BETWEEN '2023-05-01' AND '2023-05-31'
            GROUP BY
                b.id, b.name
            ORDER BY
                may_amount DESC
            LIMIT 10;
        ```

    2. 如何優化:    
        1. 建立索引，避免全表掃描
        
        ```SQL
            CREATE INDEX idx_orders_currency_created_at ON orders(currency, created_at);
            CREATE INDEX idx_orders_bnb_id ON orders(bnb_id);
        ```
        2. 分區表:就年份或月份對order分區，加快查找速度。









