FROM python:3.12.2-alpine3.19

WORKDIR /app

COPY . .


RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

