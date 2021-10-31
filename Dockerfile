FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN apt-get update && apt-get install -y \
  cmake

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir dlib==19.22.1
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app