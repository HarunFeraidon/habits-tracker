FROM python:3.11

WORKDIR /code/backend

COPY . /code/backend

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install pymysql mysqlclient cryptography

EXPOSE 5000

CMD ["python", "app.py"]
