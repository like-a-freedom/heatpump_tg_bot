# What is it?

I have a country house that has a wonderful Cooper & Hunter heat pump with a wi-fi control module.

I was found that the standard EWPE Smart app to control this heatpump is almost impossible to use, because the heatpump regularly disconnecting from the app... and you have to reboot the heatpump every time (of course, you can't do it remotely), which means you lose a valuable opportunity to turn on/adjust the temperature of the house. This is especially painful in winter time.

This repository is a very simple telegram bot that is built on the greeclimate library (thanks [cmroche](https://github.com/cmroche/greeclimate) and [tomika](https://github.com/tomikaa87/gree-remote)), I use it instead of the standard app, deployed on orangepi 3, which installed in the country house.

## How to use it?

* Get the telegram token via Bot Father
* Create `.env` file and fill it with your token (see example in `.env.sample`)
* Just run `docker compose up -d`
