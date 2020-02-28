FROM python:alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development
CMD ["flask", "run", "--host=0.0.0.0"]