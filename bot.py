#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════╗
║     NEXT PUFF BOT — @next_puff_bot       ║
║   Магазин электронных сигарет            ║
╚══════════════════════════════════════════╝
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters, ConversationHandler,
)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN   = os.environ.get("TELEGRAM_BOT_TOKEN", "")
MANAGER = "@Crypto_inspectorp"

CHOOSE_CITY, ENTER_CITY, MAIN_MENU = range(3)

CITIES = ["🏙 Москва", "🌊 Санкт-Петербург", "🌅 Хабаровск", "⚓ Владивосток", "✏️ Другой город"]

CATALOG = {
    "disposable": {
        "name": "💨 Одноразки",
        "items": [
            {"name":"Lost Mary BM5000",        "retail":1199,"wholesale":290,  "desc":"5000 тяг"},
            {"name":"Lost Mary MO5000",         "retail":440, "wholesale":250,  "desc":"5000 тяг"},
            {"name":"Lost Mary Combo 20000",    "retail":949, "wholesale":450,  "desc":"20000 тяг"},
            {"name":"Lost Mary OS4000",         "retail":949, "wholesale":570,  "desc":"4000 тяг"},
            {"name":"Lost Mary MT15000",        "retail":1049,"wholesale":690,  "desc":"15000 тяг"},
            {"name":"Lost Mary MO 20000",       "retail":1199,"wholesale":1030, "desc":"20000 тяг"},
            {"name":"Lost Mary MO 30000",       "retail":1199,"wholesale":680,  "desc":"30000 тяг"},
            {"name":"Lost Mary MO10000 LUNA",   "retail":1199,"wholesale":740,  "desc":"10000 тяг"},
            {"name":"HQD Cuvie 300",            "retail":449, "wholesale":120,  "desc":"300 тяг"},
            {"name":"HQD TITAN 7000",           "retail":1199,"wholesale":780,  "desc":"7000 тяг"},
            {"name":"HQD Cuvie Bar 7000",       "retail":1099,"wholesale":780,  "desc":"7000 тяг"},
            {"name":"Funky Lands Ci5000",       "retail":610, "wholesale":370,  "desc":"5000 тяг"},
            {"name":"Elf Bar 2000",             "retail":749, "wholesale":290,  "desc":"2000 тяг"},
            {"name":"Elf Bar Lux 1500",         "retail":749, "wholesale":360,  "desc":"1500 тяг"},
            {"name":"Elf Bar CR5000",           "retail":799, "wholesale":330,  "desc":"5000 тяг"},
            {"name":"Elf Bar BC4000 EN",        "retail":899, "wholesale":290,  "desc":"4000 тяг"},
            {"name":"Elf Bar BC 5000 Ultra",    "retail":949, "wholesale":600,  "desc":"5000 тяг"},
            {"name":"Elf Bar GH33000",          "retail":1199,"wholesale":790,  "desc":"33000 тяг"},
            {"name":"Elf Bar Ice King 30000",   "retail":1049,"wholesale":690,  "desc":"30000 тяг"},
            {"name":"Elf Bar Moonnight 25000",  "retail":1149,"wholesale":680,  "desc":"25000 тяг"},
            {"name":"Elf Bar Sour King 30000",  "retail":1099,"wholesale":690,  "desc":"30000 тяг"},
            {"name":"iJOY LIO COMMA 5500",      "retail":749, "wholesale":320,  "desc":"5500 тяг"},
            {"name":"iJOY LIO BOOM 3500",       "retail":749, "wholesale":360,  "desc":"3500 тяг"},
            {"name":"UDN BOX 5000",             "retail":799, "wholesale":320,  "desc":"5000 тяг"},
            {"name":"UDN BAR 6000",             "retail":899, "wholesale":490,  "desc":"6000 тяг"},
            {"name":"UDN AIR BAR PRO 3500",     "retail":680, "wholesale":480,  "desc":"3500 тяг"},
            {"name":"Brusko Vini 1400 🔥",       "retail":699, "wholesale":99,   "desc":"1400 тяг | РАСПРОДАЖА"},
            {"name":"Brusko Split L 5000",      "retail":899, "wholesale":240,  "desc":"5000 тяг"},
            {"name":"Vapengin MARS 4000",       "retail":649, "wholesale":280,  "desc":"4000 тяг"},
            {"name":"Puffmi DY4500",            "retail":949, "wholesale":510,  "desc":"4500 тяг"},
            {"name":"Husky Cyber 10000",        "retail":1199,"wholesale":570,  "desc":"10000 тяг"},
            {"name":"Inflave MAX 4000",         "retail":949, "wholesale":470,  "desc":"4000 тяг"},
            {"name":"Plonq Roqy M 10000",       "retail":899, "wholesale":520,  "desc":"10000 тяг"},
        ],
    },
    "liquid": {
        "name": "💧 Жижи",
        "items": [
            {"name":"DUALL"},{"name":"HOTSPOT"},{"name":"MAXWELLS"},
            {"name":"POD ONKI"},{"name":"ANGRY VAPE"},{"name":"BOSHKI"},
            {"name":"BRUSKO"},{"name":"CHAPPMAN"},{"name":"COSMONAUT"},
            {"name":"DABBLER"},{"name":"ELECTRO JAM"},{"name":"GANG"},
            {"name":"HORNY FLAVA"},{"name":"HUSKY"},{"name":"INFLAVE"},
            {"name":"JAMGO"},{"name":"KILO"},{"name":"LAVVA"},
            {"name":"LOST MARY"},{"name":"MEW"},{"name":"MONSTERVAPOR"},
            {"name":"NICVAPE"},{"name":"NITROS COLD BREW"},{"name":"OGGO"},
            {"name":"ПЕРЕДОЗ"},{"name":"PRIDE VAPE"},{"name":"RELL"},
            {"name":"RONIN"},{"name":"PLONQ"},{"name":"SALT"},
            {"name":"SKALA"},{"name":"SKL"},{"name":"SMOKE KITCHEN"},
            {"name":"SNEGOVIK"},{"name":"THE SCANDALIST"},{"name":"TOYZ SALT"},
            {"name":"VAPE DIRECT"},{"name":"VLAGA"},{"name":"VOODOO"},
            {"name":"YOVO"},{"name":"ГОПРА"},{"name":"ДЯДЯ ВОВА"},
        ],
    },
    "liquid_pod": {
        "name": "🧪 Жидкости для пода",
        "items": [
            {"name":"Жидкости для пода — большой выбор", "desc":"Все бренды в наличии. Уточняйте у менеджера"},
        ],
    },
    "pods": {
        "name": "🔋 Подики",
        "items": [
            {"name":"Vaporesso VIBE 1100mAh",           "retail":1799,"wholesale":610,  "desc":"1100 mAh Pod Kit"},
            {"name":"Vaporesso XROS 4 1000mAh",         "retail":1999,"wholesale":1300, "desc":"1000 mAh Pod Kit"},
            {"name":"Vaporesso XROS 4 NANO 1350mAh",    "retail":2399,"wholesale":1450, "desc":"1350 mAh Pod Kit"},
            {"name":"Vaporesso XROS 5 1500mAh",         "retail":2199,"wholesale":1400, "desc":"1500 mAh Pod Kit"},
            {"name":"Vaporesso XROS 5 MINI 1500mAh",    "retail":1599,"wholesale":900,  "desc":"1500 mAh Mini Pod Kit"},
            {"name":"Vaporesso XROS 5 NANO 1600mAh",    "retail":2799,"wholesale":1950, "desc":"1600 mAh Nano Pod Kit"},
            {"name":"Vaporesso APEX 2000mAh",           "retail":2499,"wholesale":1590, "desc":"2000 mAh Pod Kit"},
            {"name":"Vaporesso LUXE X2 2000mAh",        "retail":3099,"wholesale":1100, "desc":"2000 mAh"},
            {"name":"Vaporesso LUXE X3 2600mAh",        "retail":2090,"wholesale":1530, "desc":"2600 mAh"},
            {"name":"Vaporesso LUXE XR Max 2",          "retail":3099,"wholesale":2180, "desc":"Pod Kit"},
            {"name":"Vaporesso GEN MAX 220W",           "retail":4799,"wholesale":3540, "desc":"220W Mod Kit"},
            {"name":"Vaporesso ARMOUR GS",              "retail":2899,"wholesale":1980, "desc":"80W Pod Kit"},
            {"name":"Voopoo VMATE i3 1500mAh",          "retail":1499,"wholesale":850,  "desc":"1500 mAh"},
            {"name":"Voopoo VMATE PRO 2 1500mAh",       "retail":2099,"wholesale":1210, "desc":"1500 mAh"},
            {"name":"Voopoo VMATE MINI 1000mAh",        "retail":1290,"wholesale":780,  "desc":"1000 mAh | 4 картриджа"},
            {"name":"Voopoo ARGUS E40 1800mAh",         "retail":1999,"wholesale":1210, "desc":"1800 mAh"},
            {"name":"Voopoo Argus Pro 2 80W 3000mAh",   "retail":3099,"wholesale":1980, "desc":"3000 mAh 80W"},
            {"name":"Voopoo DRAG X3 80W",               "retail":2690,"wholesale":1880, "desc":"80W Pod Kit"},
            {"name":"Voopoo DRAG S3 3000mAh",           "retail":2690,"wholesale":1880, "desc":"3000 mAh Pod Mod"},
            {"name":"Voopoo DRAG 5 177W Mod Kit",       "retail":5299,"wholesale":3680, "desc":"177W Mod Kit"},
            {"name":"Geek Vape Aegis Boost 3 3000mAh",  "retail":2990,"wholesale":2080, "desc":"3000 mAh"},
            {"name":"Geek Vape Obelisk 65 FC 🔥",        "retail":2099,"wholesale":1500, "desc":"2×1100 mAh | РАСПРОДАЖА"},
            {"name":"Geek Vape Aegis Boost E100 100W",  "retail":4699,"wholesale":3390, "desc":"100W Pod Kit"},
            {"name":"Geek Vape Aegis Boost Pro 2 B100", "retail":3399,"wholesale":2240, "desc":"100W Kit"},
            {"name":"Geek Vape Aegis Hero 2 H45 1400mAh","retail":2299,"wholesale":1780,"desc":"1400 mAh Classic"},
            {"name":"Geek Vape Aegis Hero 5 2000mAh",   "retail":2590,"wholesale":1780, "desc":"2000 mAh"},
            {"name":"Geek Vape Aegis Legend III 200W",  "retail":4699,"wholesale":3480, "desc":"200W Kit"},
            {"name":"Geek Vape Aegis Legend 5 200W",    "retail":4690,"wholesale":3380, "desc":"200W Kit"},
            {"name":"Geek Vape Aegis Force 80W",        "retail":3099,"wholesale":2040, "desc":"80W Pod Kit"},
            {"name":"Smoant Knight 40 Pod Kit 1500mAh", "retail":2099,"wholesale":1000, "desc":"1500 mAh"},
            {"name":"Smoant Pasito Pro Pod Kit 1500mAh","retail":2349,"wholesale":1290, "desc":"1500 mAh"},
            {"name":"Smoant Pasito 3 Pod Kit",          "retail":3290,"wholesale":2480, "desc":"Pod Kit"},
            {"name":"Smoant Knight AIO 90W Kit",        "retail":3499,"wholesale":2240, "desc":"90W AIO Kit"},
            {"name":"Rincoe Manto Aio Plus 80W",        "retail":1949,"wholesale":1380, "desc":"80W Pod Kit"},
            {"name":"Brusko Minican 5 Pro 1400mAh",     "retail":2599,"wholesale":1830, "desc":"1400 mAh"},
            {"name":"Plonq Meta LITE",                  "retail":1950,"wholesale":1070, "desc":"Pod Kit"},
            {"name":"Elf Bar ELFX PRO 1200mAh",         "retail":1190,"wholesale":490,  "desc":"Refillable Dual Mesh"},
        ],
    },
    "accessories": {
        "name": "🔧 Комплектующие для подов",
        "items": [
            {"name":"⚡ Аккумуляторы", "desc":"Цена и наличие — уточняйте у менеджера"},
            {"name":"🫙 Баки",         "desc":"Цена и наличие — уточняйте у менеджера"},
            {"name":"🌀 Испарители",   "desc":"Цена и наличие — уточняйте у менеджера"},
            {"name":"💾 Картриджи",    "desc":"Цена и наличие — уточняйте у менеджера"},
        ],
    },
}


def city_keyboard():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(c, callback_data=f"city_{c}")] for c in CITIES]
    )

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💨 Одноразки",               callback_data="cat_disposable")],
        [InlineKeyboardButton("💧 Жижи",                    callback_data="cat_liquid")],
        [InlineKeyboardButton("🧪 Жидкости для пода",       callback_data="cat_liquid_pod")],
        [InlineKeyboardButton("🔋 Подики",                  callback_data="cat_pods")],
        [InlineKeyboardButton("🔧 Комплектующие для подов", callback_data="cat_accessories")],
        [InlineKeyboardButton("📞 Связаться с менеджером",  callback_data="manager")],
    ])

def back_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("◀️ Назад в меню", callback_data="back_menu"),
        InlineKeyboardButton("📞 Менеджер",     callback_data="manager"),
    ]])


def fmt_price(item):
    retail = item.get("retail")
    wholesale = item.get("wholesale")
    if retail is None:
        return "💬 Цена уточняется у менеджера"
    return f"🏷 Розница: <b>{retail} ₽</b>\n📦 Опт (от 800 тыс.₽): <b>{wholesale} ₽</b>"


def item_card(item):
    desc = item.get("desc", "")
    price = fmt_price(item)
    return (
        f"<b>{item['name']}</b>\n"
        f"{'─' * 22}\n"
        + (f"📋 {desc}\n\n" if desc else "\n")
        + price
        + f"\n\n📞 Заказ: {MANAGER}"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Добро пожаловать в <b>Next Puff</b>!\n\n"
        "🛒 Электронные сигареты, одноразки, жижи, поды\n"
        "📦 Опт и розница | 🚚 Доставка по всей России\n\n"
        "Выберите ваш город:",
        reply_markup=city_keyboard(),
        parse_mode="HTML",
    )
    return CHOOSE_CITY


async def city_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "city_✏️ Другой город":
        await q.edit_message_text("✏️ Напишите название вашего города:")
        return ENTER_CITY
    city = q.data.replace("city_", "")
    context.user_data["city"] = city
    await q.edit_message_text(
        f"📍 Ваш город: <b>{city}</b>\n\nВыберите категорию:",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    return MAIN_MENU


async def city_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    context.user_data["city"] = city
    await update.message.reply_text(
        f"📍 Ваш город: <b>{city}</b>\n\nВыберите категорию:",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    return MAIN_MENU


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    city = context.user_data.get("city", "—")
    await q.edit_message_text(
        f"📍 Город: <b>{city}</b>\n\nВыберите категорию:",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    return MAIN_MENU


async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cat_key = q.data.replace("cat_", "")
    cat = CATALOG.get(cat_key)
    if not cat:
        return MAIN_MENU

    city = context.user_data.get("city", "")
    items = cat["items"]

    if cat_key in ("liquid", "liquid_pod", "accessories"):
        await q.edit_message_text(
            f"📍 {city} | {cat['name']}\n\nФормирую список...",
            parse_mode="HTML",
        )

        if cat_key == "liquid":
            brands = [f"• {it['name']}" for it in items]
            header = (
                f"💧 <b>Жижи — наши бренды:</b>\n\n"
                + "\n".join(brands)
                + f"\n\n📞 Наличие и цены уточняйте у менеджера:\n<b>{MANAGER}</b>"
            )
            await q.message.reply_text(header, parse_mode="HTML", reply_markup=back_keyboard())

        else:
            for item in items:
                text = item_card(item)
                await q.message.reply_text(text, parse_mode="HTML")
            await q.message.reply_text(
                f"✅ Раздел «{cat['name']}»\n\nПо всем позициям обращайтесь: {MANAGER}",
                reply_markup=back_keyboard(),
            )
        return MAIN_MENU

    await q.edit_message_text(
        f"📍 {city} | {cat['name']}\n\n"
        f"Товаров: <b>{len(items)}</b>\nОтправляю каталог... ⏳",
        parse_mode="HTML",
    )

    for item in items:
        caption = item_card(item)
        await q.message.reply_text(caption, parse_mode="HTML")

    await q.message.reply_text(
        f"✅ Показаны все {len(items)} товаров раздела «{cat['name']}»",
        reply_markup=back_keyboard(),
    )
    return MAIN_MENU


async def manager_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(
        f"📞 Менеджер: <b>{MANAGER}</b>\n\n"
        "Принимает заказы и отвечает на вопросы по:\n"
        "• Наличию товаров\n"
        "• Ценам на жидкости и комплектующие\n"
        "• Условиям опта\n"
        "• Доставке",
        parse_mode="HTML",
        reply_markup=back_keyboard(),
    )
    return MAIN_MENU


def main():
    if not TOKEN:
        print("❌ Ошибка: токен не задан! Установите переменную окружения TELEGRAM_BOT_TOKEN")
        return

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_CITY: [CallbackQueryHandler(city_chosen, pattern="^city_")],
            ENTER_CITY:  [MessageHandler(filters.TEXT & ~filters.COMMAND, city_entered)],
            MAIN_MENU: [
                CallbackQueryHandler(show_category,   pattern="^cat_"),
                CallbackQueryHandler(back_to_menu,    pattern="^back_menu$"),
                CallbackQueryHandler(manager_contact, pattern="^manager$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(conv)

    print("=" * 45)
    print("  🚀 NEXT PUFF BOT запущен!")
    print(f"  🤖 t.me/next_puff_bot")
    print(f"  📞 Менеджер: {MANAGER}")
    print("=" * 45)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
