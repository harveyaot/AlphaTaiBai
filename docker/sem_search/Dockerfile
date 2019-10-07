FROM tiangolo/uwsgi-nginx:python3.7-alpine3.8
RUN pip install flask
RUN pip install requests
COPY ./app /app
WORKDIR /app
