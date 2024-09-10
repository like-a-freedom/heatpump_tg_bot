FROM python:3.12-slim AS build
RUN apt -y update && apt install -y gcc
RUN python3 -m pip install --upgrade pip setuptools
COPY ./src/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

FROM python:3.12-slim
WORKDIR /opt/heatpump_telegram_bot
COPY --from=build /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY ./src /opt/heatpump_telegram_bot
RUN touch ./heatpump_telegram_bot.log
RUN ln -sf /dev/stdout ./heatpump_telegram_bot.log \
    && ln -sf /dev/stderr ./heatpump_telegram_bot.log
CMD ["python3", "bot.py"]