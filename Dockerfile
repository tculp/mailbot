FROM python:3.5
WORKDIR /root
COPY mailbot mailbot
COPY setup.py setup.py
RUN python setup.py install
RUN rm -r mailbot
ENTRYPOINT ["mailbot"]
