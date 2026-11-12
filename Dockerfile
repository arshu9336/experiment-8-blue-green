FROM python:3.12-slim

WORKDIR /app

COPY app.py .

ENV COLOR=BLUE
ENV APP_VERSION=1.0
ENV BUILD_NUMBER=local

EXPOSE 8080

CMD ["python", "-u", "app.py"]
