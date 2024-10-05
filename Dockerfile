FROM python:3.11.5

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /work
COPY . /work
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
CMD flask --app main run -h 0.0.0.0
