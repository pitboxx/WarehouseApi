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

## 2. API и поддерживаемые операции

**Целевое API:** Warehouse API (C# ASP.NET Core)
- **Базовый URL:** `http://localhost:5000`
- **Формат данных:** JSON
- **Аутентификация:** Не требуется

**Поддерживаемые операции (15 инструментов):**

### Пользователи (Users)
1. `get_users` - Получить всех пользователей
2. `get_user` - Получить пользователя по ID
3. `create_user` - Создать нового пользователя
4. `update_user` - Обновить пользователя
5. `delete_user` - Удалить пользователя

### Подразделения (Departments)
6. `get_departments` - Получить все подразделения
7. `get_department` - Получить подразделение по ID
8. `create_department` - Создать новое подразделение
9. `update_department` - Обновить подразделение
10. `delete_department` - Удалить подразделение

### Товары (Products)
11. `get_products` - Получить все товары
12. `get_product` - Получить товар по ID
13. `create_product` - Создать новый товар
14. `update_product` - Обновить товар
15. `delete_product` - Удалить товар

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

## 4. 5 тестовых запросов и результаты

### Запрос 1: Показать всех пользователей
**Команда:** `python main.py "покажи пользователей"`
**Результат:**
```json
{
  "Status": "success",
  "Action": "get_users",
  "Data": [
    {
      "id": 1,
      "firstName": "",
      "lastName": "",
      "email": "",
      "phone": "",
      "role": "Employee",
      "createdAt": "2026-05-24T13:44:32.0294622Z",
      "updatedAt": "2026-05-24T13:46:19.3389097Z",
      "departmentId": 2,
      "department": null
    },
    {
      "id": 2,
      "firstName": "Jane",
      "lastName": "Smith",
      "email": "jane.smith@example.com",
      "phone": "+0987654321",
      "role": "Employee",
      "createdAt": "2026-05-24T13:44:32.0295684Z",
      "updatedAt": "2026-05-24T13:44:32.0295684Z",
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
      "createdAt": "2026-05-24T13:44:32.0295686Z",
      "updatedAt": "2026-05-24T13:44:32.0295686Z",
      "departmentId": 3,
      "department": null
    }
  ]
}
```

### Запрос 2: Создать нового пользователя
**Команда:** `python main.py "создай пользователя с именем Михаил"`
**Результат:**
```json
{
  "Status": "success",
  "Action": "create_user",
  "Data": {
    "id": 4,
    "firstName": "Михаил",
    "lastName": "Doe",
    "email": "михаил@example.com",
    "phone": "+1234567890",
    "role": "Employee",
    "createdAt": "2026-05-24T13:59:07.3830681Z",
    "updatedAt": "2026-05-24T13:59:07.3830684Z",
    "departmentId": 1,
    "department": null
  }
}
```

### Запрос 3: Показать все подразделения
**Команда:** `python main.py "show departments"`
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

### Запрос 4: Показать все товары
**Команда:** `python main.py "show products"`
**Результат:**
```json
{
  "Status": "success",
  "Action": "get_products",
  "Data": [
    {
      "id": 1,
      "name": "Laptop",
      "description": "High-performance laptop",
      "price": 999.99,
      "quantity": 10,
      "sku": "LP-001",
      "createdAt": "2026-05-24T13:44:32.0277287Z",
      "updatedAt": "2026-05-24T13:44:32.0277288Z",
      "departmentId": 2,
      "department": null
    },
    {
      "id": 2,
      "name": "Smartphone",
      "description": "Latest smartphone model",
      "price": 699.99,
      "quantity": 25,
      "sku": "SP-002",
      "createdAt": "2026-05-24T13:44:32.0278716Z",
      "updatedAt": "2026-05-24T13:44:32.0278717Z",
      "departmentId": 2,
      "department": null
    },
    {
      "id": 3,
      "name": "T-Shirt",
      "description": "Cotton t-shirt",
      "price": 19.99,
      "quantity": 100,
      "sku": "TS-003",
      "createdAt": "2026-05-24T13:44:32.0278718Z",
      "updatedAt": "2026-05-24T13:44:32.0278719Z",
      "departmentId": 3,
      "department": null
    }
  ]
}
```

### Запрос 5: Показать справку
**Команда:** `python main.py`
**Результат:**
```
Warehouse API Agent CLI.
Usage:
  python main.py "natural language command"           # rule-based parser
  python main.py --llm "natural language command"     # LLM agent (requires LM Studio)

Example:
  python main.py "создай пользователя с именем Alex"
  python main.py --llm "create a user named Alex"
```

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

### Контекстные промпты (системные)
- Использование LangChain 1.3.1 с `create_agent` из `langchain.agents.factory`
- Формат ответа: JSON с полями Status, Action, Data, Errors
- Поддержка русского и английского языков в rule-based парсере
- Интеграция с LM Studio через OpenAI-совместимый API

---

## Заключение

Агент успешно интегрирован с Warehouse API и поддерживает два режима работы:
1. **Rule-based парсер** - для детерминированных команд на русском и английском
2. **LLM-агент** - для гибкого понимания естественного языка через Qwen/LM Studio

Все инструменты возвращают результаты в едином контрактном формате, что обеспечивает согласованность взаимодействия.