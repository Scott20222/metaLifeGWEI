FROM python:3.6.4


RUN apt-get update \
&&apt-get install -y sqlite3

RUN mkdir /var/run/gwei

COPY *.py /var/run/gwei

COPY config.json /var/run/gwei

COPY run.sh /var/run/gwei

WORKDIR /var/run/gwei

COPY requirements.txt /var/run/gwei

RUN pip3 install -r /var/run/dao/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

CMD ["/bin/bash","/var/run/gwei/run.sh"]
