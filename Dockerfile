FROM python:3.12-slim

WORKDIR /src

COPY . /src

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash"]