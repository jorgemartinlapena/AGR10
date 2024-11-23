FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    iproute2 \
    procps \
    iputils-ping \
    frr \
    netcat \
    curl \
    traceroute

# CMD ["sleep", "infinity"]
CMD ["echo", "Hola fluentd!!"]
