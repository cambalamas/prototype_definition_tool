FROM ubuntu:16.04

LABEL Version="0.0.1"
LABEL Maintainer="cambalamas@gmail.com"
LABEL Description="A mouse-oriented editor to generate a xml definition of an \
interactive prototype."

RUN apt-get update && \
	apt-get install -y --no-install-recommends\
		python3 \
		python3-lxml \
		python3-pyqt5

RUN pip install python-i18n[YAML]
