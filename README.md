# QRKot
Приложение благотворительного фонда поддержки котиков

### Описание:
QRKot - это API для сбора средств, разработанное для поддержки различных целевых проектов, в том числе направленных на помощь популяции кошек. 

Фонд может одновременно вести несколько целевых проектов. У каждого проекта есть название, описание и целевая сумма для сбора. Проекты финансируются по очереди, когда проект набирает необходимую сумму и закрывается, пожертвования начинают поступать в следующий проект.

Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.


### Стек технологий 

![](https://img.shields.io/badge/Python-3.9-black?style=flat&logo=python) 
![](https://img.shields.io/badge/FastAPI-0.78.0-black?style=flat&logo=fastapi)
![](https://img.shields.io/badge/Pydantic-1.9.1-black?style=flat)
![](https://img.shields.io/badge/SQLAlchemy-1.4.29-black?style=flat)

### Запуск проекта

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Theivlev/cat_charity_fund.git
```

```
cd cat_charity_fund
```

2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Для Linux/macOS

    ```
    source venv/bin/activate
    ```

* Для Windows

    ```
    source venv/scripts/activate
    ```

3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
alembic upgrade head
```

5. Запустить приложение:

```
uvicorn app.main:app
```