FROM python:3


RUN apt-get update \
&&apt-get install -y sqlite3

RUN mkdir /var/run/gwei

COPY requirements.txt /var/run/gwei

RUN pip install -r /var/run/gwei/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

RUN mkdir /var/run/data

COPY *.py /var/run/gwei

COPY config.json /var/run/gwei

COPY run.sh /var/run/gwei

WORKDIR /var/run/gwei


CMD ["/bin/bash","/var/run/gwei/run.sh"]
