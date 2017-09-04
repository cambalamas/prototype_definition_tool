FROM ubuntu:16.04

LABEL Version="0.1"
LABEL Maintainer="cambalamas@gmail.com"
LABEL Description="A mouse-oriented editor for design statics states and simples components of an UI"

RUN apt-get update && \
	apt-get install -y --no-install-recommends\
		dbus\
		python3 \
		python3-lxml \
		python3-pyqt5 \
		python3-pip \
		python3-setuptools

RUN pip3 install --upgrade pip
RUN pip3 install python-i18n[YAML]

RUN sed -i "s/^#\ es_ES/es_ES/g" /etc/locale.gen
RUN DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales

ENV LANG es_ES.ISO-8859-1
ENV LC_ALL es_ES.ISO-8859-1
ENV LANGUAGE es_ES.ISO-8859-1
