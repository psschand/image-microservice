FROM python:3

ADD . /code
WORKDIR /code

RUN pip install pipenv
RUN pipenv install --system

ENTRYPOINT ["python"]
CMD ["run.py"]
