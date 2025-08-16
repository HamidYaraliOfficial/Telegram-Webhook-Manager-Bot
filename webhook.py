# bot.py
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import re
from typing import Optional

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Bot as TGBot,
)
from telegram.constants import ParseMode
from telegram.error import TelegramError, BadRequest, Forbidden, NetworkError, RetryAfter, TimedOut
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# -------------------- تنظیمات --------------------

# توکن همین ربات مدیریت (نه توکن ربات هدف)
BOT_TOKEN = os.getenv("BOT_TOKEN", "PASTE_YOUR_MANAGER_BOT_TOKEN_HERE")

# مسیر فایل بنر برای دکمه «حمایت از ما»
BANNER_PATH = "webhock/static/banner.jpg"

# الگوی اعتبارسنجی توکن ربات‌های تلگرام
TOKEN_REGEX = re.compile(r"^\d+:[A-Za-z0-9_-]{35,}$")

# -------------------- لاگینگ --------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("webhook-manager-bot")

# -------------------- ابزارک‌ها --------------------

def main_menu_markup() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("ست وبهوک", callback_data="set_webhook"),
            InlineKeyboardButton("حذف وبهوک", callback_data="delete_webhook"),
        ],
        [
            InlineKeyboardButton("اطلاعات وبهوک", callback_data="info_webhook"),
        ],
        [
            InlineKeyboardButton("حمایت از ما ❤️", callback_data="support_us"),
            InlineKeyboardButton("درباره ربات 🤖", callback_data="about_bot"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def is_valid_token(token: str) -> bool:
    return bool(TOKEN_REGEX.match(token.strip()))

def is_valid_https_url(url: str) -> bool:
    url = url.strip()
    return url.startswith("https://") and len(url) <= 2048

def get_banner_bytes() -> Optional[bytes]:
    try:
        with open(BANNER_PATH, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

async def send_error(update: Update, text: str) -> None:
    if update.effective_chat:
        await update.effective_chat.send_message(text)

def drop_text_to_bool(s: str) -> Optional[bool]:
    if not s:
        return None
    v = s.strip().lower()
    if v in {"yes", "y", "بله", "آره", "drop"}:
        return True
    if v in {"no", "n", "خیر", "نه"}:
        return False
    return None

# -------------------- هندلرهای منو --------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    text = (
        "سلام! 👋\n"
        "با این ربات می‌تونی وبهوک ربات‌هات رو تنظیم/حذف کنی و اطلاعاتش رو ببینی.\n"
        "یک گزینه رو انتخاب کن:"
    )
    await update.message.reply_text(text, reply_markup=main_menu_markup())

async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    # هر بار از منو شروع کنیم، داده‌های قبلی پاک بشه
    context.user_data.clear()

    if data == "set_webhook":
        context.user_data["state"] = "await_token_set"
        await query.message.reply_text(
            "ست وبهوک | SetWebhook\n"
            "لطفاً توکن ربات هدف را ارسال کنید.\n"
            "فرمت: 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
        )
        return

    if data == "delete_webhook":
        context.user_data["state"] = "await_token_del"
        await query.message.reply_text(
            "حذف وبهوک | DeleteWebhook\n"
            "لطفاً توکن ربات هدف را ارسال کنید."
        )
        return

    if data == "info_webhook":
        context.user_data["state"] = "await_token_info"
        await query.message.reply_text(
            "اطلاعات وبهوک | WebhookInfo\n"
            "لطفاً توکن ربات هدف را ارسال کنید."
        )
        return

    if data == "support_us":
        banner = get_banner_bytes()
        caption = (
            "❤️ حمایت از ما\n"
            "با اشتراک‌گذاری این بنر در کانال/گروه خود از ما حمایت کنید.\n"
            "🌐 mizbanir.com"
        )
        if banner:
            await query.message.reply_photo(photo=banner, caption=caption)
        else:
            await query.message.reply_text(caption + "\n(فایل بنر یافت نشد. مسیر را بررسی کنید.)")
        return

    if data == "about_bot":
        text = (
            "🤖 ربات مدیریت وبهوک\n"
            "با این ربات می‌توانید وبهوک ربات‌های خود را تنظیم یا حذف کنید و وضعیت آن را ببینید.\n"
            "دکمه‌های منو را فشار دهید یا /start را بزنید."
        )
        await query.message.reply_text(text, reply_markup=main_menu_markup())
        return

# -------------------- جریان پیام‌های متنی (مدیریت مرحله‌ای) --------------------

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()
    state = context.user_data.get("state")

    # هیچ مرحله‌ای فعال نیست → نادیده/راهنما
    if not state:
        await update.message.reply_text("برای شروع از منو استفاده کنید یا /start را بزنید.", reply_markup=main_menu_markup())
        return

    # ---------- ست وبهوک ----------
    if state == "await_token_set":
        if not is_valid_token(text):
            await update.message.reply_text("❌ توکن نامعتبر است. لطفاً با فرمت صحیح ارسال کنید.")
            return
        context.user_data["token"] = text
        context.user_data["state"] = "await_url_set"
        await update.message.reply_text("✅ توکن دریافت شد.\nحالا آدرس وبهوک HTTPS را ارسال کنید (مثلاً https://example.com/telegram/webhook).")
        return

    if state == "await_url_set":
        if not is_valid_https_url(text):
            await update.message.reply_text("❌ URL نامعتبر است. لطفاً یک آدرس HTTPS معتبر ارسال کنید.")
            return
        context.user_data["url"] = text
        context.user_data["state"] = "await_drop_set"
        await update.message.reply_text("آیا می‌خواهید صف به‌روزرسانی‌های معلق پاک شود؟\nیکی از موارد را بفرستید: yes | no | drop")
        return

    if state == "await_drop_set":
        drop = drop_text_to_bool(text)
        if drop is None:
            await update.message.reply_text("لطفاً یکی از موارد معتبر ارسال کنید: yes | no | drop")
            return

        token = context.user_data.get("token")
        url = context.user_data.get("url")
        bot = TGBot(token=token)

        try:
            await bot.set_webhook(url=url, drop_pending_updates=drop)
            info = await bot.get_webhook_info()
            msg = (
                "✅ وبهوک با موفقیت تنظیم شد.\n"
                f"- URL: {info.url or url}\n"
                f"- Has custom cert: {getattr(info, 'has_custom_certificate', False)}\n"
                f"- Pending updates: {getattr(info, 'pending_update_count', 0)}\n"
            )
            await update.message.reply_text(msg, reply_markup=main_menu_markup())
        except RetryAfter as e:
            await update.message.reply_text(f"⏳ لطفاً {int(e.retry_after)} ثانیه صبر کنید و مجدد تلاش کنید.")
        except (BadRequest, Forbidden) as e:
            await update.message.reply_text(f"❌ خطا در تنظیم وبهوک: {e}")
        except (NetworkError, TimedOut) as e:
            await update.message.reply_text(f"⚠️ خطای شبکه/تایم‌اوت: {e}")
        except TelegramError as e:
            await update.message.reply_text(f"❌ خطای تلگرام: {e}")
        finally:
            context.user_data.clear()
        return

    # ---------- حذف وبهوک ----------
    if state == "await_token_del":
        if not is_valid_token(text):
            await update.message.reply_text("❌ توکن نامعتبر است. لطفاً با فرمت صحیح ارسال کنید.")
            return
        context.user_data["token"] = text
        context.user_data["state"] = "await_drop_del"
        await update.message.reply_text("آیا می‌خواهید صف به‌روزرسانی‌های معلق پاک شود؟\nیکی از موارد را بفرستید: yes | no | drop")
        return

    if state == "await_drop_del":
        drop = drop_text_to_bool(text)
        if drop is None:
            await update.message.reply_text("لطفاً یکی از موارد معتبر ارسال کنید: yes | no | drop")
            return

        token = context.user_data.get("token")
        bot = TGBot(token=token)

        try:
            ok = await bot.delete_webhook(drop_pending_updates=drop)
            info = await bot.get_webhook_info()
            msg = (
                ("✅ وبهوک حذف شد.\n" if ok else "ℹ️ درخواست حذف ارسال شد.\n") +
                f"- URL فعلی: {info.url or '—'}\n"
                f"- Pending updates: {getattr(info, 'pending_update_count', 0)}\n"
            )
            await update.message.reply_text(msg, reply_markup=main_menu_markup())
        except RetryAfter as e:
            await update.message.reply_text(f"⏳ لطفاً {int(e.retry_after)} ثانیه صبر کنید و مجدد تلاش کنید.")
        except (BadRequest, Forbidden) as e:
            await update.message.reply_text(f"❌ خطا در حذف وبهوک: {e}")
        except (NetworkError, TimedOut) as e:
            await update.message.reply_text(f"⚠️ خطای شبکه/تایم‌اوت: {e}")
        except TelegramError as e:
            await update.message.reply_text(f"❌ خطای تلگرام: {e}")
        finally:
            context.user_data.clear()
        return

    # ---------- اطلاعات وبهوک ----------
    if state == "await_token_info":
        if not is_valid_token(text):
            await update.message.reply_text("❌ توکن نامعتبر است. لطفاً با فرمت صحیح ارسال کنید.")
            return

        bot = TGBot(token=text)
        try:
            info = await bot.get_webhook_info()
            # ساخت متن اطلاعات
            lines = [
                "ℹ️ اطلاعات وبهوک:",
                f"- URL: {info.url or '—'}",
                f"- Has custom cert: {getattr(info, 'has_custom_certificate', False)}",
                f"- Pending updates: {getattr(info, 'pending_update_count', 0)}",
            ]
            if getattr(info, "last_error_date", None):
                lines.append(f"- آخرین خطا: {info.last_error_message} (epoch: {info.last_error_date})")
            await update.message.reply_text("\n".join(lines), reply_markup=main_menu_markup())
        except RetryAfter as e:
            await update.message.reply_text(f"⏳ لطفاً {int(e.retry_after)} ثانیه صبر کنید و مجدد تلاش کنید.")
        except (BadRequest, Forbidden) as e:
            await update.message.reply_text(f"❌ خطا در دریافت اطلاعات: {e}")
        except (NetworkError, TimedOut) as e:
            await update.message.reply_text(f"⚠️ خطای شبکه/تایم‌اوت: {e}")
        except TelegramError as e:
            await update.message.reply_text(f"❌ خطای تلگرام: {e}")
        finally:
            context.user_data.clear()
        return

    # اگر به اینجا رسید یعنی state ناشناس است
    context.user_data.clear()
    await update.message.reply_text("وضعیت نامشخص. از ابتدا شروع کنید.", reply_markup=main_menu_markup())

# -------------------- سایر هندلرها --------------------

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    await update.message.reply_text("انصراف انجام شد. از منو انتخاب کنید.", reply_markup=main_menu_markup())

async def errors_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.exception("Unhandled exception: %s", context.error)

# -------------------- اجرا --------------------

def main() -> None:
    if not BOT_TOKEN or "PASTE_YOUR" in BOT_TOKEN:
        raise RuntimeError("لطفاً BOT_TOKEN را در کد یا متغیر محیطی تنظیم کنید.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    app.add_error_handler(errors_handler)

    log.info("Bot is running...")
    app.run_polling()  # نیازی به allowed_updates نیست

if __name__ == "__main__":
    main()
