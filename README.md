# Групповой проект Яндекс Практикум (Спринт 10)
## _Выполнили:_
### _[Кузенков Алексей][df1] - разработчик 1-Teamlead_
### _[Синюк Олег][df3] - разработчик 2_
### _[Шмидт Анастасия][df2] - разработчик 3_

## Описание
- Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 

- Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В каждой категории есть произведения: книги, фильмы или музыка.

- Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор.

- Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
#### Технологии:
> Python 3.7
> Django 2.2.28
> DRF
> JWT

## Запуск проекта.

Склонируйте репозиторий:

```sh
git clone git@github.com:KuzenkovAG/api_yamdb.git
```

Установите и активируйте виртуальное окружение:

```sh
python -m venv venv
source venv/Scripts/activate
```

Установите зависимости из файла requirements.txt:

```sh
pip install -r requirements.txt
```

Примените миграции:

```sh
python manage.py migrate
```

Запустите проект:

```sh
python manage.py runserver
```

заполните тестовые данные:

```sh
python manage.py import_csv
```

#### Все запросы к этому API хранятся в документации, которая станет доступна после запуска проекта по  адресу:


```sh
http://127.0.0.1:8000/redoc/
```

**Учебный проект**

   [df1]: <https://github.com/KuzenkovAG>
   [df2]: <https://github.com/NASTY-SMIT>
   [df3]: <https://github.com/olegsinyuk>
