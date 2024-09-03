FROM python:3.12.5
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./migrations /code/migrations
COPY alembic.ini /code/alembic.ini
RUN chmod +x /code/app/run.sh
CMD ["/code/app/run.sh"]