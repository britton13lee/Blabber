FROM python:alpine
RUN apk add --no-cache curl
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
ENV FLASK_APP=/app/src/app.py
HEALTHCHECK --interval=15s --timeout=3s CMD curl -f http://localhost:5000/status || exit 1
CMD ["flask", "run", "--host=0.0.0.0"]