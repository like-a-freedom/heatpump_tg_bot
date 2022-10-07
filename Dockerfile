FROM python:3.10.7-slim-buster

RUN apt-get -y update
RUN apt-get install gcc musl-dev -y
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools

COPY ./src /opt/heatpump_telegram_bot
WORKDIR /opt/heatpump_telegram_bot

RUN pip3 install -r requirements.txt
RUN touch /opt/heatpump_telegram_bot/heatpump_telegram_bot.log
RUN ln -sf /dev/stdout /opt/heatpump_telegram_bot/heatpump_telegram_bot.log \
    && ln -sf /dev/stderr /opt/heatpump_telegram_bot/heatpump_telegram_bot.log

CMD ["python3", "bot.py"]