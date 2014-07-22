# Мхундва

Бот-архивариус для авто-подлепры (ура, она женщина!).
Сохраняет на память все видео из странного хобби постов Тусинды и постит их заново, если оригинальные видео удалены.

## Установка

Для установки нужен Python 2.6 или 2.7 и возможность собирать C модули (gcc и все такое).

Создаем виртуальное окружение для Мхундвы:

```virtualenv .env```

Ставим зависимости:

```.env/bin/pip install -r requirements.txt```

Создаем файл с настройками, в котором можно будет перегрузить все настройки по умолчанию из файла `settings.py`:

```touch settings_local.py```

Как минимум, стоит изменить путь до базы данных и авторизационные данные для бота.
По умолчанию Мхундва работает с sqlite, если нужна поддержка других баз данных, не забудьте самостоятельно поставить нужный драйвер.

## Использование

Мхундва умеет делать несколько дел:

1. Парсить индексную страницу авто-подлепры и искать на ней нужные посты;
2. Парсить каждый найденный пост и искать в нем ссылки на YouTube видео;
3. Сохранять копии видео к себе;
4. Заливать видео обратно на YouTube, если оригинальное видео удалено;
5. Ставить плюс комментарию, если у Мхундвы есть копия видео из него;
6. *TODO*: Ставить минус комментарию, если видео из него уже было в предыдущих постах.

### Парсинг индексной страницы

Команда ```$ .env/bin/python manage.py parse_index``` загружает индексную страницу авто-подлепры,
находит все посты с текстом «Странного хобби пост №» и запоминает их номера в базе.

### Парсинг найденных постов

Команда ```$ .env/bin/python manage.py parse_post``` загружает страницу последнего поста,
находит ссылки на YouTube видео и сохраняет их в базу.

### Резервное копирование видео

Команда ```$ .env/bin/python manage.py download``` берет видео из последних двух постов и скачивает их в папку,
путь до которой задается настройкой `DATA_VIDEOS`.
