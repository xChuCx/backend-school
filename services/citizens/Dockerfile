# base image
FROM python:3.7-alpine

# set working directory
WORKDIR /usr/src/app

RUN apk --update add build-base

RUN apk add libcouchbase-dev

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app

# run server
CMD ["/usr/src/app/entrypoint.sh"]
