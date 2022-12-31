FROM python:3.10

WORKDIR /apis

COPY . .
RUN pip install -r req.txt

#VOLUME /drf_src
RUN chmod +x ./run.sh
EXPOSE 8080

CMD ["run.sh"]