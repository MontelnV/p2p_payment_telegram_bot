# Онлайн-магазин с P2P-платежами YooMoney
## Описание
Онлайн-магазин, размещенный в телеграм-боте и использующий в качестве платежного решения P2P-операции платежной системы YooMoney.
### Предварительная настройка
Перед запуском магазина вам необходимо настроить кошелек (подтвердить свои данные) и подключить приложение.
Подробная инструкция находится в файле youmoney.py в директории /app
### Запуск
Активируйте виртуальное окружение и установите необходимые библиотеки
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
Запустите бота
```
python run.py
```
### Запуск с помощью Docker
```
docker build . --tag bot
docker run -d bot
```
