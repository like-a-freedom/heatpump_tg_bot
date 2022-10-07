from telebot.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def main_menu() -> ReplyKeyboardMarkup:
    main_menu = ReplyKeyboardMarkup(True, True)
    main_menu.row("Current status")
    main_menu.row("Power management")
    main_menu.row("Set temperature")
    main_menu.row("Set mode")
    main_menu.row("Set speed")
    return main_menu


def power_state_menu() -> InlineKeyboardMarkup:
    power_state = InlineKeyboardMarkup()
    power_state.row_width = 1
    power_state.add(
        InlineKeyboardButton("Power on", callback_data="power_state_on"),
        InlineKeyboardButton("Power off", callback_data="power_state_off"),
    )
    return power_state


def set_temperature_menu() -> ReplyKeyboardMarkup:
    set_temperature = ReplyKeyboardMarkup(True, True)
    set_temperature.row("Back to main menu")
    return set_temperature


def set_mode_menu() -> InlineKeyboardMarkup:
    set_mode = InlineKeyboardMarkup()
    set_mode.row_width = 1
    set_mode.add(
        InlineKeyboardButton("Auto", callback_data="mode_auto"),
        InlineKeyboardButton("Cool", callback_data="mode_cool"),
        InlineKeyboardButton("Heat", callback_data="mode_heat"),
        InlineKeyboardButton("Fan", callback_data="mode_fan"),
        InlineKeyboardButton("Dry", callback_data="mode_dry"),
    )
    return set_mode


def set_speed_menu() -> InlineKeyboardMarkup:
    set_speed = InlineKeyboardMarkup()
    set_speed.row_width = 1
    set_speed.add(
        InlineKeyboardButton("Auto", callback_data="speed_auto"),
        InlineKeyboardButton("Quiet", callback_data="speed_quiet"),
        InlineKeyboardButton("Low", callback_data="speed_low"),
        InlineKeyboardButton("Medium low", callback_data="speed_medium_low"),
        InlineKeyboardButton("Medium", callback_data="speed_medium"),
        InlineKeyboardButton("Medium high", callback_data="speed_medium_high"),
        InlineKeyboardButton("High", callback_data="speed_high"),
    )
    return set_speed


def heatpump_state_menu() -> ReplyKeyboardMarkup:
    heatpump_state = ReplyKeyboardMarkup(True, True)
    heatpump_state.row("Back to main menu")
    return heatpump_state
