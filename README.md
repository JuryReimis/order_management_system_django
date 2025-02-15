

# Order Management System

## Описание:
- Проект реализует систему управления заказами в кафе

- ### Блюда
  - **Добавление блюда:** На странице пользователь вводит наименование блюда и его цену. Запись сохраняется в базе данных с уникальным id.
  - **Просмотр всех блюд:** На странице выводятся все, присутствующие в меню блюда.
  - **Редактирование блюда:** На странице пользователь может отредактировать название и цену блюда. Система сама делает дополнительную запись в базе данных о времени изменения цены.
  - **Удаление блюда:** Удаление записи в базе данных. Система автоматически почистит связанные данные. Например, упоминания в заказах, данные обновления цен и т.п.

- ### Заказы
  - **Добавление заказа:** Через специальную страницу пользователь вводит номер заказа, а также выбирает блюда и их количество. Система автоматически формирует заказ (если у выбранного стола уже нет неоплаченного заказа), создает уникальный id, помещает в базу данных заказ со статусом "В ожидании"
  - **Просмотр заказов:** На странице можно отобразить как все заказы, так и выборки, согласно следующим фильтрам: Номер стола, статус заказа. Возможно отсортировать данные.
  - **Детальная информация о заказе:** Страница отображает детальные данные: ID заказа, номер стола, полный список блюд в заказе, их количество и цена, полная стоимость заказа и статус, в котором находится заказ на данный момент. Кнопки изменения статуса позволяют пользователю выбрать новый статус заказа.
  - **Изменение состава заказа:** Если заказ имеет статус В ожидании, то пользователь может изменить список блюд, входящих в состав заказа. На странице необходимо выбрать те блюда, которые пользователь хочет включить в заказ и выбрать количество. Система автоматически изменит дату обновления заказа, общую стоимость и состав.
  - **Удаление заказа:** Полностью удалить заказ. Система сама очистит связанные записи.
  - **Получение информации за период:** На странице пользователь должен выбрать период, за который хочет получить информацию и система выдаст ему общее количество заказов со статусом Оплачено, сумму их цен и среднюю цену на заказ.


## Инструменты:
- Python 3.12
- Django 5.1.6
- Django REST Framework 3.15.2

## Подготовка к запуску:
- Создайте новое окружение
- Клонируйте в него репозиторий
- Перейдите в директорию приложения
  ```bash
  cd order_management_system_django
  ```
- Подготовьте файл .env со следующей структурой:
  ```.dotenv
  SECRET_KEY=ВАШ_СЕКРЕТНЫЙ_КЛЮЧ
  
  DEBUG=TRUE
  
  ALLOWED_HOSTS=localhost,127.0.0.1
  
  INTERNAL_IPS=127.0.0.1,
  ```
- Установите все зависимости:
  ```bash
  pip install -r requirements.txt
  ```
- Выполните миграции:
  ```bash
  py manage.py makemigrations
  py manage.py migrate
  ```
- Запустите проект:
  ```bash
  py manage.py runserver
  ```