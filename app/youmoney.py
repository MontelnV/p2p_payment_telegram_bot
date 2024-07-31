from yoomoney import Authorize

# 1. Зарегистрируйте новое приложение по ссылке: https://yoomoney.ru/myservices/new
#    При регистрации приложения ни в коем случае не выбирайте метод аутентификации Oauth2!
# 2. Введите название приложения: "Testing" и после регистрации получите client_id, который вставьте в соответствующее поле в классе Authorize
#    Поставьте параметр redirect_url = ссылку на ваш интернет-магазин/телеграм-бота
# 3. Запустите youmoney.py
#    Перейдите по ссылке, которая появится в терминале "Visit this website and confirm the application authorization request:"
#    Скопируйте URL, который появится у вас после подтверждения доступа приложению и
#    вставьте его в терминал в формате (https://yourredirect_uri?code=XXXXXXXXXXXXX)
# 4. Получите Access Token и вставьте его в параметр PAYMENT_P2P в файле .env
#    Он потребуется для проверки оплаты купленных пользователем товаров

Authorize(
      client_id="your_client_id",
      redirect_uri="https://t.me/your_bot",
      scope=["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
      )