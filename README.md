# YaMDb оценка и рейтинг произведений
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
cd api_yamdb/
python -m venv venv
source venv/Scripts/activate
```

Установите зависимости из файла requirements.txt:

```sh
pip install -r requirements.txt
```

Примените миграции:

```sh
python api_yamdb/manage.py migrate
```

Запустите проект:

```sh
python api_yamdb/manage.py runserver
```

заполните тестовые данные:

```sh
python api_yamdb/manage.py import_csv
```
##### Примеры нескольких запросов к нашему API:
Получение пользователя по username
```sh
http://127.0.0.1:8000/api/v1/users/{username}/
```
```sh
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
Добавление новой категории
```sh
http://127.0.0.1:8000/api/v1/categories/
```
```sh
{
  "name": "string",
  "slug": "string"
}
```
Удаление жанра
```sh
http://127.0.0.1:8000/api/v1/genres/{slug}/
```
Получение списка всех произведений
```sh
http://127.0.0.1:8000/api/v1/titles/
```
```sh
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```
Добавление нового отзыва
```sh
http://127.0.0.1:8000/api/v1/genres/{slug}/
```
```sh
{
  "text": "string",
  "score": 1
}
```
Частичное обновление комментария к отзыву
```sh
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
```sh
{
  "text": "string"
}
```

#### Все запросы к этому API хранятся в документации, которая станет доступна после запуска проекта по  адресу:


```sh
http://127.0.0.1:8000/redoc/
```


   [df1]: <https://github.com/KuzenkovAG>
   [df2]: <https://github.com/NASTY-SMIT>
   [df3]: <https://github.com/olegsinyuk>
