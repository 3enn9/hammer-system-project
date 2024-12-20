# Hammer System

## Описание

**Hammer System** — это веб-приложение для аутентификации пользователей через телефонный номер с использованием кода подтверждения (SMS). Проект включает регистрацию и авторизацию, а также возможность активации инвайт-кодов и просмотра профиля.

---

## Основной функционал

### 1. Регистрация и авторизация

- Пользователь вводит свой номер телефона.
- Система отправляет код подтверждения.
- Пользователь вводит код и либо регистрируется, либо авторизуется.

### 2. Подтверждение через SMS

- Генерация и отправка кода подтверждения.
- Код отправляется на указанный номер телефона.
- Реализация отправки SMS зависит от выбранного сервиса (в примере код `1234`).

### 3. Инвайт-коды

- Пользователи могут активировать инвайт-код для получения дополнительных возможностей.
- Инвайт-код позволяет привязать одного пользователя к другому, создавая систему рефералов.

### 4. API-интерфейс

- Приложение предоставляет API для управления профилем пользователя.
- Возможность отправлять коды подтверждения и получать информацию о текущем пользователе.

---

## Основные компоненты

### 1. **Функции регистрации и подтверждения кода**
   - **send_code_view**: Генерация и отправка кода подтверждения.
   - **verify_code_view**: Проверка введенного кода и аутентификация пользователя.

### 2. **Личный кабинет пользователя**
   - **profile_view**: Пользователь может просмотреть информацию о своем профиле.
   - Возможность активации инвайт-кода для привязки реферала.

### 3. **API-контроллеры**
   - **SendCodeView**: Обработка запросов для отправки кодов подтверждения.
   - **ProfileView**: Получение данных о текущем пользователе через API.

---

## Основные файлы

- **`views.py`**: Содержит логику обработки запросов и управления пользователями.
- **`models.py`**: Определяет модель пользователя (`CustomUser`), включая поля для номера телефона и инвайт-кода.
- **`serializers.py`**: Обеспечивает сериализацию данных для API.

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <url-репозитория>
cd <папка-с-репозиторием>
```
### 2. Запуск с помощью Docker

Для запуска приложения с помощью Docker используйте команду:

```bash
docker-compose up --build
```
3. Проблемы с базой данных при старте
После запуска Docker Compose может возникнуть ошибка, связанная с тем, что Django пытается подключиться к базе данных, прежде чем она будет готова. Чтобы исправить это:

Перейдите в контейнер веб-приложения:

```bash
docker exec -it <имя-контейнера-web> /bin/bash
```
Выполните миграции вручную:

```bash
python manage.py makemigrations
python manage.py migrate
```
После этого приложение должно запуститься корректно.
