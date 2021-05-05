FROM alpine:latest


ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install requests argparse

COPY ./entrypoint.sh ./nasa_api.py ./requirements.txt  /app/
WORKDIR /app
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT /app/entrypoint.sh $QUERY
