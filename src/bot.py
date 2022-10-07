import os
import sys
import time
import asyncio
import menus
import logging
import heatpump_manager
from typing import Optional
from telebot.async_telebot import AsyncTeleBot
from greeclimate.device import FanSpeed, Mode
from requests.exceptions import ConnectionError, ReadTimeout


TOKEN: str | None = os.getenv("TG_API_TOKEN", None)
bot: AsyncTeleBot = AsyncTeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=["start"])
async def show_main_menu(message):
    await bot.send_message(
        message.from_user.id, "Heatpump management", reply_markup=menus.main_menu()
    )


@bot.message_handler(content_types=["text"])
async def handle_text(message):
    match message.text:
        case "Current status":
            await device.update_state()
            if device.power:
                await bot.send_message(
                    message.from_user.id,
                    f"Current status: power on, temperature is {device.target_temperature}, mode is {device.mode}",
                    reply_markup=menus.heatpump_state_menu(),
                )
            else:
                await bot.send_message(
                    message.from_user.id,
                    "Heatpump is powered down",
                    reply_markup=menus.heatpump_state_menu(),
                )
        case "Power management":
            await bot.send_message(
                message.from_user.id,
                "Enable or disable heatpump",
                reply_markup=menus.power_state_menu(),
            )
        case "Set temperature":
            await bot.send_message(
                message.from_user.id,
                "Enter temperature (8-30)",
                reply_markup=menus.set_temperature_menu(),
            )
        case "Set mode":
            await bot.send_message(
                message.from_user.id, "Select mode", reply_markup=menus.set_mode_menu()
            )
        case "Set speed":
            await bot.send_message(
                message.from_user.id,
                "Select speed",
                reply_markup=menus.set_speed_menu(),
            )
        case "Back to main menu":
            await bot.send_message(
                message.from_user.id,
                "Heatpump management",
                reply_markup=menus.main_menu(),
            )
        case _:
            if message.text.isdigit():
                try:
                    device.target_temperature = int(message.text)
                    await device.push_state_update()
                    await bot.reply_to(message, f"Temperature set to {message.text}")
                except Exception as e:
                    await bot.reply_to(message, str(e))


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    match call.data:
        case "mode_auto":
            device.mode = Mode.Auto
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Mode set to Auto")
        case "mode_cool":
            device.mode = Mode.Cool
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Mode set to Cool")
        case "mode_heat":
            device.mode = Mode.Heat
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Mode set to Heat")
        case "mode_fan":
            device.mode = Mode.Fan
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Mode set to Fan")
        case "mode_dry":
            device.mode = Mode.Dry
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Mode set to Fan")
        case "power_state_on":
            device.power = True
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "On")
        case "power_state_off":
            device.power = False
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Off")
        case "speed_auto":
            device.fan_speed = FanSpeed.Auto
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Speed set to Auto")
        case "speed_quiet":
            device.quiet = True
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Speed set to Quiet")
        case "speed_low":
            device.fan_speed = FanSpeed.Low
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Speed set to Low")
        case "speed_medium_low":
            device.fan_speed = FanSpeed.MediumLow
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Speed set to Medium low")
        case "speed_medium":
            device.fan_speed = FanSpeed.Medium
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Speed set to Medium")
        case "speed_medium_high":
            device.fan_speed = FanSpeed.MediumHigh
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Speed set to Medium high")
        case "speed_high":
            device.fan_speed = FanSpeed.High
            await device.push_state_update()
            await bot.answer_callback_query(call.id, "Speed set to High")


def log_event(module_name: str, log_level=logging.INFO) -> Optional[logging.Logger]:
    """
    Write meesages into log file
    """
    logger = logging.getLogger(
        module_name
    )  # another approach is to use `logger.propagate = False`
    if not len(logger.handlers):
        handler = logging.FileHandler("heatpump_telegram_bot.log")
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s: %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(log_level)
        return logger
    else:
        return logger


device = heatpump_manager.get_device()
logger = log_event(__file__)


if __name__ == "__main__":
    try:
        asyncio.run(bot.infinity_polling(timeout=60, request_timeout=60, interval=1))
    except (ConnectionError, ReadTimeout) as e:
        logger.error(e)
        print(e)
        time.sleep(15)
        sys.stdout.flush()
        os.execv(sys.argv[0], sys.argv)
    else:
        asyncio.run(bot.infinity_polling(timeout=60, request_timeout=60, interval=1))
