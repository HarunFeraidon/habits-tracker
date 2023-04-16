FROM python:3.11

WORKDIR /code/backend

COPY . /code/backend

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
# CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "4"]
# CMD ["uvicorn", "code.backend.app:app", "--host", "0.0.0.0", "--port", "80"]
