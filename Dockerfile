FROM ubuntu:16.04

LABEL Version="0.1"
LABEL Maintainer="cambalamas@gmail.com"
LABEL Description="A mouse-oriented editor for design statics states and simples components of an UI"

RUN apt-get update && \
	apt-get install -y --no-install-recommends\
		python3 \
		python3-lxml \
		python3-pyqt5 \
		python3-pip \
		python3-setuptools

RUN pip3 install --upgrade pip
RUN pip3 install python-i18n[YAML]
