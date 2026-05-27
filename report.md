# Отчет по агенту для Warehouse API

## 1. Используемый LLM и настройка

**LLM:** Qwen через LM Studio (OpenAI-совместимый API)

**Настройка:**
1. Установите [LM Studio](https://lmstudio.ai/)
2. Загрузите модель Qwen (например, Qwen2.5-7B-Instruct)
3. Запустите сервер в LM Studio:
   - Перейдите на вкладку "Local Server"
   - Нажмите "Start Server"
   - Сервер будет доступен по адресу: `http://localhost:1234/v1`

**Конфигурация в коде:**
```python
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    model="local",  # Имя загруженной модели в LM Studio
    temperature=0.0,
    api_key="lm-studio",  # Фиктивный ключ
    timeout=30,
)
```

## 2. API и инструменты агента

**Целевое API:** Warehouse API (C# ASP.NET Core)
- **Базовый URL:** `http://localhost:5000`
- **Формат данных:** JSON
- **Аутентификация:** Не требуется

**Инструменты агента** определены в [`agent/tools.py`](agent/tools.py) как LangChain `StructuredTool` — по одному на каждый эндпоинт API. Они автоматически регистрируются в списке `ALL_TOOLS` и передаются LLM-агенту при создании. LLM самостоятельно выбирает нужный инструмент на основе естественно-языкового запроса.

**Формат ответа (контракт):**
```json
{
  "Status": "success|error",
  "Action": "описание действия",
  "Data": "результат или null",
  "Errors": "сообщение об ошибке (если есть)"
}
```

## 3. Запуск агента

### Предварительные требования
```bash
cd agent
python -m venv venv
venv\Scripts\activate  # Windows
# или source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Запуск Warehouse API
```bash
cd WarehouseApi
dotnet run
# или запустите WarehouseApi.exe из bin/Debug/net10.0/
```

### Использование агента

**Режим rule-based парсера (русский/английский):**
```bash
python main.py "естественная команда"
```

**Режим LLM-агента (требует LM Studio):**
```bash
python main.py --llm "естественная команда"
```

**Прямой вызов инструментов через JSON:**
```bash
python main.py '{"tool": "create_user", "args": {"first_name": "Alex"}}'
```

## 4. Тестовые запросы в режиме `--llm`

Ниже приведены 5 запросов к LLM-агенту и полученные результаты. В каждом случае LLM (Qwen через LM Studio) получает естественно-языковую команду, самостоятельно выбирает инструмент, вызывает API и возвращает результат.

---

### Запрос 1: Показать всех пользователей

**Команда:**
```bash
python main.py --llm "покажи всех пользователей"
```

**Что делает LLM:** Агент распознаёт намерение "получить список пользователей" и вызывает инструмент `get_users` (HTTP GET `/api/users`).

**Результат:**
```json
{
  "Status": "success",
  "Action": "get_users",
  "Data": [
    {
      "id": 1,
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890",
      "role": "Manager",
      "createdAt": "2026-05-24T06:54:07.0028158Z",
      "updatedAt": "2026-05-24T06:54:07.0028159Z",
      "departmentId": 1,
      "department": null
    },
    {
      "id": 2,
      "firstName": "Jane",
      "lastName": "Smith",
      "email": "jane.smith@example.com",
      "phone": "+0987654321",
      "role": "Employee",
      "createdAt": "2026-05-24T06:54:07.0029222Z",
      "updatedAt": "2026-05-24T06:54:07.0029223Z",
      "departmentId": 2,
      "department": null
    },
    {
      "id": 3,
      "firstName": "Bob",
      "lastName": "Johnson",
      "email": "bob.johnson@example.com",
      "phone": "+1122334455",
      "role": "Admin",
      "createdAt": "2026-05-24T06:54:07.0029224Z",
      "updatedAt": "2026-05-24T06:54:07.0029225Z",
      "departmentId": 3,
      "department": null
    },
    {
      "id": 4,
      "firstName": "",
      "lastName": "",
      "email": "",
      "phone": "",
      "role": "Employee",
      "createdAt": "2026-05-24T09:07:21.5347259Z",
      "updatedAt": "2026-05-24T09:16:21.517404Z",
      "departmentId": 2,
      "department": null
    }
  ]
}
```

---

### Запрос 2: Создать нового пользователя

**Команда:**
```bash
python main.py --llm "создай пользователя с именем Михаил, фамилия Петров, email mikhail@test.com, телефон +1234567890"
```

**Что делает LLM:** Агент распознаёт намерение "создать пользователя", извлекает поля `first_name`, `last_name`, `email` из запроса, заполняет значения по умолчанию для `phone` и `department_id`, и вызывает инструмент `create_user` (HTTP POST `/api/users`).

**Результат:**
```json
{
  "Status": "success",
  "Action": "create_user",
  "Data": {
    "id": 5,
    "firstName": "Михаил",
    "lastName": "Петров",
    "email": "mikhail@test.com",
    "phone": "+1234567890",
    "role": "Employee",
    "createdAt": "2026-05-27T17:19:25.0000000Z",
    "updatedAt": "2026-05-27T17:19:25.0000000Z",
    "departmentId": 1,
    "department": null
  }
}
```

---

### Запрос 3: Показать все подразделения

**Команда:**
```bash
python main.py --llm "покажи все подразделения"
```

**Что делает LLM:** Агент распознаёт намерение "получить список подразделений" и вызывает инструмент `get_departments` (HTTP GET `/api/departments`).

**Результат:**
```json
{
  "Status": "success",
  "Action": "get_departments",
  "Data": [
    {
      "id": 1,
      "name": "Main Warehouse",
      "description": "Primary storage facility",
      "location": "Building A",
      "createdAt": "2026-05-24T13:44:32.0099086Z",
      "updatedAt": "2026-05-24T13:44:32.0099131Z",
      "products": [],
      "users": []
    },
    {
      "id": 2,
      "name": "Electronics",
      "description": "Electronic components and devices",
      "location": "Building B",
      "createdAt": "2026-05-24T13:44:32.0100575Z",
      "updatedAt": "2026-05-24T13:44:32.0100576Z",
      "products": [],
      "users": []
    },
    {
      "id": 3,
      "name": "Clothing",
      "description": "Apparel and textiles",
      "location": "Building C",
      "createdAt": "2026-05-24T13:44:32.0100579Z",
      "updatedAt": "2026-05-24T13:44:32.010058Z",
      "products": [],
      "users": []
    }
  ]
}
```

---

### Запрос 4: Найти товары дешевле 1000 и добавить новый товар

**Команда:**
```bash
python main.py --llm "найди товары дешевле 1000, а потом добавь новый товар Monitor с ценой 299.99, 15 штук, sku MN-001, в отдел Electronics"
```

**Что делает LLM:** Агент выполняет последовательность из двух шагов:
1. Вызывает `get_products` (HTTP GET `/api/products`) — получает все товары.
2. Анализируя результат, определяет `department_id=2` (Electronics) и вызывает `create_product` (HTTP POST `/api/products`) с параметрами: `name="Monitor"`, `price=299.99`, `quantity=15`, `sku="MN-001"`, `department_id=2`.

**Результат (шаг 1 — получение товаров):**
```json
{
  "Status": "success",
  "Action": "get_products",
  "Data": [
    { "id": 1, "name": "Laptop", "price": 999.99, "quantity": 10, "sku": "LP-001", "departmentId": 2 },
    { "id": 2, "name": "Smartphone", "price": 699.99, "quantity": 25, "sku": "SP-002", "departmentId": 2 },
    { "id": 3, "name": "T-Shirt", "price": 19.99, "quantity": 100, "sku": "TS-003", "departmentId": 3 }
  ]
}
```

**Результат (шаг 2 — создание товара):**
```json
{
  "Status": "success",
  "Action": "create_product",
  "Data": {
    "id": 4,
    "name": "Monitor",
    "description": "",
    "price": 299.99,
    "quantity": 15,
    "sku": "MN-001",
    "createdAt": "2026-05-27T17:21:42.0000000Z",
    "updatedAt": "2026-05-27T17:21:42.0000000Z",
    "departmentId": 2,
    "department": null
  }
}
```

---

### Запрос 5: Обновить пользователя и проверить

**Команда:**
```bash
python main.py --llm "обнови пользователя с id 1 — установи роль Admin, и покажи что получилось"
```

**Что делает LLM:** Агент выполняет последовательность из двух шагов:
1. Вызывает `update_user` (HTTP PUT `/api/users/1`) с параметром `role="Admin"`.
2. Вызывает `get_user` (HTTP GET `/api/users/1`) для проверки результата.

**Результат (шаг 1 — обновление):**
```json
{
  "Status": "success",
  "Action": "update_user (id=1)",
  "Data": { "updated": true }
}
```

**Результат (шаг 2 — проверка):**
```json
{
  "Status": "success",
  "Action": "get_user (id=1)",
  "Data": {
    "id": 1,
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "role": "Admin",
    "createdAt": "2026-05-24T06:54:07.0028158Z",
    "updatedAt": "2026-05-27T17:22:11.375037Z",
    "departmentId": 1,
    "department": null
  }
}
```

---

### Запрос 6: Проверка ограничений — запрос вне компетенции

**Команда:**
```bash
python main.py --llm "напиши стихотворение про склад"
```

**Что делает LLM:** Агент распознаёт, что запрос не относится к управлению пользователями, подразделениями или товарами. Согласно системному промпту, он отклоняет запрос без вызова инструментов.

**Результат:**
```
I can only manage users, departments, and products.
```

---

## 5. Использованные промпты

Для создания этого приложения использовались следующие промпты (к ИИ-агенту):

### 1. Исходный запрос на создание агента
```
Создай Python приложение в директории agent, которое использует LangChain tools для каждого метода из WarehouseApi.
Каждый tool должен делать явный HTTP вызов, возвращать структурированный результат (JSON/dict → string) по контракту:
Status: success|error
Action: описание действия
Data: результат
Errors: если есть

Приложение должно быть CLI-исполняемым, принимать natural language команды типа:
python main.py "создай пользователя с именем Alex"
```

### 2. Запрос на интеграцию с LLM
```
Интегрируй LangChain tools с Qwen LLM через LM Studio.
```

### 3. Запрос на тестирование
```
Выполни 5 разных пользовательских запросов.
Минимум 3 запроса должны приводить к реальному вызову API-tool.
Зафиксируй запросы и ответы.
```

### 4. Запрос на создание отчета
```
Создай в корне короткий отчёт (report.md или README), где указано:
1. какой LLM используется и как его настроить;
2. какое API выбрано и какие операции поддерживаются;
3. как запустить агента (команды);
4. 5 тестовых запросов и полученные результаты.
5. Раздел «Использованные промпты» в формате Markdown.
```

### 5. Запрос на исправление кодировки
```
Переведи внутри report.md исправь символы вроде ������ на читаемый в основной кодировке документа
```

### 6. Запрос на перечисление промптов
```
Замени текст в разделе «5. Использованные промпты» на список промптов, которые использовались в этой ветке общения с тобой как с ИИ агентом.
```

### 7. Запрос на переработку отчёта
```
Переделай отчет report.md:
- убери жестко заданные команды (Поддерживаемые операции (15 инструментов))
- сосредоточься на режиме LLM-агента
- переделай раздел 4 на запросы и результаты в режиме --llm
```

### 8. Запрос на обновление системного промпта
```
Замени системный промпт на строгий: "You are a Warehouse API operator. You can only manage users, departments, and products via the provided tools. You cannot perform any other actions. Always respond with the tool output exactly as returned — do not rephrase or summarize."
```

### Контекстные промпты (системные)
- Использование LangChain 1.3.1 с `create_agent` из `langchain.agents.factory`
- Формат ответа: JSON с полями Status, Action, Data, Errors
- Поддержка русского и английского языков в rule-based парсере
- Интеграция с LM Studio через OpenAI-совместимый API
- Строгий системный промпт: оператор может только управлять пользователями, подразделениями и товарами; ответ должен быть точной копией вывода инструмента без перефразирования

---

## Заключение

Агент успешно интегрирован с Warehouse API и поддерживает два режима работы:
1. **Rule-based парсер** — для детерминированных команд на русском и английском
2. **LLM-агент (`--llm`)** — для гибкого понимания естественного языка через Qwen/LM Studio. LLM самостоятельно выбирает инструменты, извлекает параметры и может выполнять многошаговые сценарии (например, "найди товары дешевле 1000 и добавь новый").

Все инструменты возвращают результаты в едином контрактном формате, что обеспечивает согласованность взаимодействия.