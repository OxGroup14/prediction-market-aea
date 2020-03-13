FROM python:3.7
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -yq gcc protobuf-compiler cmake
RUN curl -sSL https://get.docker.com/ | sh
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN git clone https://github.com/fetchai/oef-sdk-python.git --recursive
RUN cd oef-sdk-python && python3 setup.py install
COPY quickstart.sh .
COPY aea_client.py .
COPY aea_server.py .
CMD sh ./quickstart.sh
