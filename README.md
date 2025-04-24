
# 1.Активация виртуального окружения проекта
source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
# 2.Установка зависимостей
pip install -r requirements.txt

# 3. Запуск теста с логами "INFO"
pytest -v --log-cli-level=INFO

# 4. Запуск теста без логов
pytest test_yandex_market_scenario.py