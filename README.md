# Telegram Webhook Manager Bot

This is a Python-based Telegram bot designed to manage webhooks for other Telegram bots. Built using the `python-telegram-bot` library, it allows users to set, delete, and retrieve webhook information for their bots with a simple interface.

## Features
- Set webhooks for Telegram bots with customizable options (e.g., drop pending updates).
- Delete existing webhooks with the option to clear pending updates.
- Retrieve detailed webhook information, including URL, certificate status, pending updates, and last error details.
- User-friendly inline keyboard menu for easy navigation.
- Support for a banner image to promote the bot (optional, requires a local file).
- Comprehensive error handling for Telegram API issues (e.g., network errors, invalid tokens).
- Multi-language support with Persian as the primary language for user interaction.

## Requirements
- Python 3.7+
- `python-telegram-bot` library (`pip install python-telegram-bot`)
- A valid Telegram Bot API token for the manager bot.
- Optional: A banner image file (`webhock/static/banner.jpg`) for the "Support Us" feature.

## Setup
1. Replace `BOT_TOKEN` in the code with your Telegram Bot API token obtained from [BotFather](https://t.me/BotFather), or set it as an environment variable (`BOT_TOKEN`).
2. Optionally, place a banner image at `webhock/static/banner.jpg` for the "Support Us" feature.
3. Install dependencies using `pip install -r requirements.txt` (create a `requirements.txt` with `python-telegram-bot`).
4. Run the bot with `python bot.py`.

## Usage
- Start the bot with `/start` to access the main menu.
- Use the inline keyboard to select options:
  - **Set Webhook**: Provide a bot token and HTTPS URL to set a webhook.
  - **Delete Webhook**: Provide a bot token to remove a webhook.
  - **Webhook Info**: Retrieve current webhook details for a bot.
  - **Support Us**: View a promotional banner (if available).
  - **About Bot**: Display information about the bot.
- Use `/cancel` to reset the current operation and return to the main menu.
- The bot guides users through a step-by-step process for each action, validating inputs like tokens and URLs.

## Code Structure
- `main_menu_markup`: Generates the inline keyboard menu.
- `is_valid_token`, `is_valid_https_url`: Validate bot tokens and URLs.
- `get_banner_bytes`: Loads the optional banner image.
- `start`, `on_callback`, `on_text`: Handle user interactions via commands, buttons, and text input.
- `cancel`: Resets the user session.
- `errors_handler`: Logs and handles unexpected errors.
- State management using `context.user_data` for multi-step processes (e.g., token → URL → drop updates).

## Logging
- Configured to output logs to the console with timestamps, log level, logger name, and message.
- Logs include bot activities, user interactions, and errors.

## License
MIT License

---

# ربات مدیریت وبهوک تلگرام

این یک ربات تلگرامی مبتنی بر پایتون است که برای مدیریت وبهوک‌های سایر ربات‌های تلگرام طراحی شده است. این ربات با استفاده از کتابخانه `python-telegram-bot` ساخته شده و امکان تنظیم، حذف و مشاهده اطلاعات وبهوک‌ها را با رابط کاربری ساده فراهم می‌کند.

## ویژگی‌ها
- تنظیم وبهوک برای ربات‌های تلگرام با گزینه‌های قابل تنظیم (مانند حذف به‌روزرسانی‌های معلق).
- حذف وبهوک‌های موجود با امکان پاک‌سازی به‌روزرسانی‌های معلق.
- دریافت اطلاعات دقیق وبهوک، شامل آدرس URL، وضعیت گواهی، تعداد به‌روزرسانی‌های معلق و جزئیات آخرین خطا.
- منوی کیبورد اینلاین کاربرپسند برای ناوبری آسان.
- پشتیبانی از بنر تبلیغاتی برای حمایت از ربات (نیاز به فایل محلی، اختیاری).
- مدیریت جامع خطاها برای مشکلات API تلگرام (مانند خطاهای شبکه یا توکن نامعتبر).
- پشتیبانی از چند زبان با اولویت زبان پارسی برای تعامل با کاربر.

## پیش‌نیازها
- پایتون نسخه 3.7 یا بالاتر
- کتابخانه `python-telegram-bot` (نصب با `pip install python-telegram-bot`)
- توکن معتبر API ربات تلگرام برای ربات مدیریت.
- اختیاری: فایل بنر (`webhock/static/banner.jpg`) برای قابلیت «حمایت از ما».

## راه‌اندازی
1. مقدار `BOT_TOKEN` در کد را با توکن API ربات تلگرام که از [BotFather](https://t.me/BotFather) دریافت کرده‌اید جایگزین کنید یا آن را به‌عنوان متغیر محیطی (`BOT_TOKEN`) تنظیم کنید.
2. در صورت تمایل، یک فایل بنر در مسیر `webhock/static/banner.jpg` برای قابلیت «حمایت از ما» قرار دهید.
3. وابستگی‌ها را با استفاده از `pip install -r requirements.txt` نصب کنید (فایل `requirements.txt` را با درج `python-telegram-bot` ایجاد کنید).
4. ربات را با اجرای `python bot.py` راه‌اندازی کنید.

## استفاده
- با دستور `/start` ربات را شروع کنید تا به منوی اصلی دسترسی پیدا کنید.
- از کیبورد اینلاین برای انتخاب گزینه‌ها استفاده کنید:
  - **ست وبهوک**: توکن ربات و آدرس HTTPS را برای تنظیم وبهوک وارد کنید.
  - **حذف وبهوک**: توکن ربات را برای حذف وبهوک وارد کنید.
  - **اطلاعات وبهوک**: جزئیات وبهوک فعلی ربات را مشاهده کنید.
  - **حمایت از ما**: بنر تبلیغاتی را مشاهده کنید (در صورت وجود).
  - **درباره ربات**: اطلاعات ربات را مشاهده کنید.
- از دستور `/cancel` برای لغو عملیات جاری و بازگشت به منوی اصلی استفاده کنید.
- ربات کاربران را از طریق فرآیند گام‌به‌گام برای هر عملیات هدایت کرده و ورودی‌هایی مانند توکن و URL را اعتبارسنجی می‌کند.

## ساختار کد
- `main_menu_markup`: تولید منوی کیبورد اینلاین.
- `is_valid_token`، `is_valid_https_url`: اعتبارسنجی توکن ربات و آدرس‌های URL.
- `get_banner_bytes`: بارگذاری تصویر بنر اختیاری.
- `start`، `on_callback`، `on_text`: مدیریت تعاملات کاربر از طریق دستورات، دکمه‌ها و ورودی متنی.
- `cancel`: بازنشانی جلسه کاربر.
- `errors_handler`: ثبت و مدیریت خطاهای غیرمنتظره.
- مدیریت حالت‌ها با استفاده از `context.user_data` برای فرآیندهای چندمرحله‌ای (مانند توکن → URL → حذف به‌روزرسانی‌ها).

## لاگ‌ها
- لاگ‌ها برای نمایش در کنسول با درج زمان، سطح لاگ، نام لاگر و پیام تنظیم شده‌اند.
- لاگ‌ها شامل فعالیت‌های ربات، تعاملات کاربر و خطاها هستند.

## مجوز
مجوز MIT

---

# Telegram Webhook管理机器人

这是一个基于Python的Telegram机器人，专为管理其他Telegram机器人的Webhook设计。使用`python-telegram-bot`库构建，提供简单的界面以设置、删除和获取Webhook信息。

## 功能
- 为Telegram机器人设置Webhook，支持自定义选项（如清除待处理更新）。
- 删除现有Webhook，可选择清除待处理更新。
- 获取详细的Webhook信息，包括URL、证书状态、待处理更新数量和最后错误详情。
- 用户友好的内联键盘菜单，便于导航。
- 支持推广横幅图片（可选，需本地文件）。
- 全面处理Telegram API错误（如网络错误、无效令牌）。
- 支持多语言交互，以波斯语为主要语言。

## 要求
- Python 3.7或更高版本
- `python-telegram-bot`库（使用`pip install python-telegram-bot`安装）
- 有效的Telegram机器人API令牌，用于管理机器人。
- 可选：横幅图片文件（`webhock/static/banner.jpg`），用于“支持我们”功能。

## 设置
1. 将代码中的`BOT_TOKEN`替换为从[BotFather](https://t.me/BotFather)获取的Telegram机器人API令牌，或将其设置为环境变量（`BOT_TOKEN`）。
2. 可选：将横幅图片放置在`webhock/static/banner.jpg`以支持“支持我们”功能。
3. 使用`pip install -r requirements.txt`安装依赖项（创建一个包含`python-telegram-bot`的`requirements.txt`文件）。
4. 使用`python bot.py`运行机器人。

## 使用
- 使用`/start`命令启动机器人以访问主菜单。
- 使用内联键盘选择选项：
  - **设置Webhook**：提供机器人令牌和HTTPS URL以设置Webhook。
  - **删除Webhook**：提供机器人令牌以删除Webhook。
  - **Webhook信息**：查看机器人当前的Webhook详情。
  - **支持我们**：查看推广横幅（如果可用）。
  - **关于机器人**：显示机器人信息。
- 使用`/cancel`命令重置当前操作并返回主菜单。
- 机器人通过分步流程引导用户完成每个操作，并验证令牌和URL等输入。

## 代码结构
- `main_menu_markup`：生成内联键盘菜单。
- `is_valid_token`、`is_valid_https_url`：验证机器人令牌和URL。
- `get_banner_bytes`：加载可选横幅图片。
- `start`、`on_callback`、`on_text`：通过命令、按钮和文本输入处理用户交互。
- `cancel`：重置用户会话。
- `errors_handler`：记录和处理意外错误。
- 使用`context.user_data`进行多步骤流程的状态管理（如令牌→URL→清除更新）。

## 日志
- 配置为输出到控制台，包含时间戳、日志级别、日志记录器名称和消息。
- 日志包括机器人活动、用户交互和错误。

## 许可证
MIT许可证