FROM python:3-alpine

RUN mkdir -p /opt/services/helpdeskapp/src
WORKDIR /opt/services/helpdeskapp/src

RUN pip install gunicorn django

COPY . /opt/services/helpdeskapp/src

EXPOSE 8080

CMD [ "gunicorn", "--chdir", "helpdesk", "--bind", ":8000", "helpdesk.wsgi:application" ]