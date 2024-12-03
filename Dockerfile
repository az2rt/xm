FROM python:3.7.13-alpine3.16

RUN apk --no-cache add \
    git \
    openjdk8-jre \
    && rm -rf /var/cache/apk/* \

ENV VERSION 2.32.0
RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.32.0/allure-commandline-2.32.0.tgz
RUN tar -zxf allure-commandline-2.32.0.tgz
RUN rm allure-commandline-2.32.0.tgz
ENV PATH="/allure-2.32.0/bin:${PATH}"

ENV PATH="/app/venv/bin:$PATH"
WORKDIR /app
