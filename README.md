<h1>E-Wallet</h1>
<h2>REST приложение для работы с электронными кошельками на DjangoRestFramework</h2>
<h3>Реализовано:</h3>
<p>Эндпоинт GET api/v1/wallets/ возвращает данные о всех имеющихся кошельках.</p>
<p>Эндпоинт GET api/v1/wallets/{WALLET_UUID} возвращает данные о балансе конкретного кошелька.</p>
<p>Эндпоинт POST api/v1/wallets/<WALLET_UUID>/operation принимает запросы типа
{operation_type: “DEPOSIT” or “WITHDRAW”, amount: 1000}. Проверяет возможность проведения транзакции и проводит ее, при этом блокируя данную запись в БД для остальных потоков. В DRF входящие потоки по-умолчанию обрабатываются многопоточно (конкурентно).</p>
<p>Сервер проверен утилитой Apache24 ab.exe. При обработке 100 запросов на изменение баланса 1 кошелька в 10 потоков баланс изменяется корректно, конфликтов не возникает.</p>
<p>Для контролллеров написаны базовые юниттесты. Запускаются через docker-compose run bank-drf python manage.py runtest.</p>

  ## Запуск на локальной машине
Клонируем репозиторий:
```
git clone https://github.com/NailKalimov/JavaCodeTestCase.git
```

Далее переходим в папку с проектом
```
сd JavaCodeTestCase
```

Поднимаем приложение через Docker-Compose. При первом запуске используем docker-compose_firststart.yml
```
docker compose -f docker-compose_firststart.yml up
```
<p>При этом автоматически пройдут миграции в БД, создастся Django-superuser с учетными данными из .env-файла и запустится сервер на 8000 порту</p>

# Адресные пути
- [Документация к API базе данных](http://127.0.0.1:8000/swagger/)
- [Админ-панель базы данных](http://127.0.0.1:8000/admin)
