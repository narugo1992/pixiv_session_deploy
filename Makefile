.PHONY: makeup

PYTHON ?= $(shell which python)

SESSION_DIR  ?= ./pixiv_session
SESSION_REPO ?= https://huggingface.co/datasets/narugo/pixiv_session
SESSION_FILE ?= ${SESSION_DIR}/session.json

CURRENT_DIR ?= $(shell pwd)

PIXIV_USERNAME ?= username
PIXIV_PASSWORD ?= password

GIT_NAME  ?= robot
GIT_EMAIL ?= robot@gmail.com

FAST_TYPE ?=
HEADLESS  ?=

makeup:
	if [ ! -d "${SESSION_DIR}" ]; then \
	  git clone "${SESSION_REPO}" "${SESSION_DIR}" && \
	  cd "${SESSION_DIR}" && \
	  git config user.name "${GIT_NAME}" && \
	  git config user.email "${GIT_EMAIL}" && \
	  cd ${CURRENT_DIR}; \
	else \
	  cd "${SESSION_DIR}" && git pull && cd ${CURRENT_DIR}; \
	fi
	$(PYTHON) -m pixiv login \
	  --username "${PIXIV_USERNAME}" \
	  --password "${PIXIV_PASSWORD}" \
	  --output "${SESSION_FILE}" \
	  $(if ${HEADLESS},,--no-headless) \
	  $(if ${FAST_TYPE},,--slow-type)
	cd "${SESSION_DIR}" && \
	  git add -A && \
	  git commit -a -m "dev(narugo): auto sync $(shell date -R)" && \
	  git push && \
	  cd ${CURRENT_DIR}
