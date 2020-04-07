#!/bin/bash

set -e
set -x

FILENAME=$1
WIRECARD_PLUGIN_FILES=$(find . -name "${FILENAME}" -not -path "*./extension-payment-method-config-provider/*")
DEFAULT_PLUGIN_FILES=$(find extension-payment-method-config-provider/ -name "${FILENAME}")

if [[ "${DEFAULT_PLUGIN_FILES}" == *"wirecard"* ]]; then
  DEFAULT_REPO="extension-payment-method-config-provider/wirecard/${FILENAME}"
fi

cmp --silent "${DEFAULT_REPO}" "${WIRECARD_PLUGIN_FILES}" && export CREDENTIALS_CHANGED=0 || export CREDENTIALS_CHANGED=1

if [[ ${CREDENTIALS_CHANGED}  == "1" ]]; then
  echo ::set-env name=CREDENTIALS_CHANGED::1
  cp "${DEFAULT_REPO}" "${WIRECARD_PLUGIN_FILES}"
else
  echo ::set-env name=CREDENTIALS_CHANGED::0
fi

rm -rf extension-payment-method-config-provider/
