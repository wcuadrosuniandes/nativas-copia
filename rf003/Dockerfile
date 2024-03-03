FROM python:3.11.7-alpine

EXPOSE 3005

WORKDIR /code

COPY Pipfile Pipfile.lock /code/

RUN pip install pipenv
RUN pipenv lock && pipenv install --system --deploy

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3005"]