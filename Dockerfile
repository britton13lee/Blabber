FROM python:alpine
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ENV FLASK_APP=/app/src/app.py
CMD ["flask", "run", "--host=0.0.0.0"]