FROM alpine:edge

RUN echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
 && apk add --no-cache dovecot

COPY conf /conf
COPY start.sh /start.sh

EXPOSE 8006/tcp 8007/tcp

CMD /start.sh
