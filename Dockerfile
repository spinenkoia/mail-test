FROM python:3.7-stretch as build

WORKDIR /build

RUN pip3 install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache -r requirements.txt

COPY backend ./backend
COPY tests ./tests
COPY setup.py .
RUN python3 setup.py test
RUN python3 setup.py sdist --dist-dir .

FROM python:3.7-stretch
WORKDIR /app

RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install --no-cache -r requirements.txt

COPY --from=build /build/convertator*.tar.gz .
RUN pip install convertator*.tar.gz

EXPOSE 8080

ENTRYPOINT ["convertator", "--debug"]
