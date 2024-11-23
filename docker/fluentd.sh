#!/bin/bash
docker run -d -p 24224:24224 -v ./fluentd.conf:/fluentd/etc/fluentd.conf -v ./logs:/fluentd/logs -e FLUENTD_CONF=fluentd.conf fluentd:latest