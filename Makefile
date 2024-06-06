.PHONY: makeup

PYTHON ?= $(shell which python)

SESSION_REPO ?= narugo/pixiv_session

CURRENT_DIR ?= $(shell pwd)

PIXIV_USERNAME ?= username
PIXIV_PASSWORD ?= password

GIT_NAME  ?= robot
GIT_EMAIL ?= robot@gmail.com

FAST_TYPE ?=
HEADLESS  ?=

makeup:
	$(PYTHON) -m pixiv login \
	  --username "${PIXIV_USERNAME}" \
	  --password "${PIXIV_PASSWORD}" \
	  $(if ${HEADLESS},,--no-headless) \
	  $(if ${FAST_TYPE},,--slow-type)

batch:
	$(PYTHON) -m pixiv batch \
	  $(if ${HEADLESS},,--no-headless) \
	  $(if ${FAST_TYPE},,--slow-type)
