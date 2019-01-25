FROM python:3.7-alpine
ADD . /app
WORKDIR /app
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev
RUN pip install -r requirements.txt
CMD ["python", "run.py"]

