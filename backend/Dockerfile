FROM python:3.12-alpine3.22

RUN adduser -D efm

WORKDIR /app

COPY app.py /app/

USER efm

EXPOSE 8080

CMD [ "python", "app.py" ]