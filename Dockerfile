FROM python:alpine
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
ENV FLASK_APP=/app/src/app.py
CMD ["flask", "run", "--host=0.0.0.0"]