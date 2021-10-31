FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN apt-get update && apt-get install -y \
  cmake libgl1-mesa-glx

RUN pip install dlib==19.22.1
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip cache purge

COPY ./app /app

# RUN apt-get install -y opencv-python-headless