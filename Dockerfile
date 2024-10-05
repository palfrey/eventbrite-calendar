FROM python:3.11.5

WORKDIR /work
COPY uv /work
RUN ./uv --version
COPY requirements.txt /work
RUN ./uv pip sync --system requirements.txt
WORKDIR /work
COPY . /work
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
CMD gunicorn main:app -b 0.0.0.0:5000
