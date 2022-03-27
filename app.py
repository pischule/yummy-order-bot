from typing import List, Optional
import datetime
import logging
import os
import re
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Message, ChatMember
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, CommandHandler
from telegram.utils.helpers import mention_markdown, escape_markdown
import cv2 as cv

from menu_parser import MenuParser

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('yummy_bot')
logger.setLevel(logging.INFO)

menu_date: Optional[datetime.date] = None
menu_items: List[str] = []

mp = MenuParser()

load_dotenv()
admin_user = int(os.environ['ADMIN_USER'])
yummy_user = int(os.environ['YUMMY_USER'])
group_chat = int(os.environ['GROUP_CHAT'])
bot_token = os.environ['BOT_TOKEN']

date_map = {}


def remove_old_dates():
    today = datetime.date.today()
    for date in date_map:
        if date < today:
            del date_map[date]


def is_menu_update_text(text: str) -> bool:
    return 'меню на' in text.lower() or '14.00' in text


def is_group(update: Update) -> bool:
    return update.effective_chat.id == group_chat


def user_belongs_to_group(update: Update, context: CallbackContext) -> bool:
    member: ChatMember = context.bot.get_chat_member(group_chat, update.effective_user.id)
    return member and member.status in {ChatMember.CREATOR, ChatMember.ADMINISTRATOR, ChatMember.MEMBER}


def load_image():
    images = [n for n in os.listdir('data') if n.endswith(('.jpg', '.png', '.jpeg'))]
    if not images:
        raise Exception('No images found')
    images.sort()
    latest_image = images[-1]
    logger.info(f'Loading image: {latest_image}')
    menu_image = cv.imread(os.path.join('data', latest_image), cv.IMREAD_COLOR)

    global menu_date
    global menu_items
    menu_items = mp.dish_names(menu_image)
    menu_date = datetime.date.fromisoformat(latest_image.split('.')[0])

    for name in images[:-1]:
        logger.info(f'Removing image: {name}')
        os.remove(os.path.join('data', name))
    remove_old_dates()


def text_handler(update: Update, context: CallbackContext) -> None:
    logger.info(f'Text handler at chat {update.effective_message.chat_id}')
    text = update.message.text
    user_id = update.effective_user.id
    m = re.match(r'.*?(\d{1,2}\.\d{1,2}\.\d{2,4}).*', text, re.DOTALL)
    if is_menu_update_text(text) and user_id in {admin_user, yummy_user} and m:
        next_date = datetime.datetime.strptime(m.group(1), '%d.%m.%Y').date()
        today = datetime.date.today()
        date_map[today] = next_date
        logger.info(f'Next date: {next_date}')


def render_order(item_ids: List[int]) -> str:
    counter = {}
    for item_id in item_ids:
        counter[item_id] = counter.get(item_id, 0) + 1

    order_message = ''
    for i in counter:
        order_message += f'- {menu_items[i]}'
        if counter[i] > 1:
            order_message += f' x{counter[i]}'
        order_message += '\n'
    return order_message


def show_start_text(update: Update, context: CallbackContext) -> None:
    logger.info(f'Show start text at chat {update.effective_message.chat_id}')

    if is_group(update):
        update.message.reply_text(
            'Привет! Я умею делать заказ из меню Yummy. '
            f'Создать заказ можно командой /order в приватном чате с @{context.bot.username}'
        )

    else:
        update.message.reply_text(
            'Привет! Я умею делать заказ из меню Yummy. Создать заказ можно командой /order')


def parse_selected_items(query: str) -> List[int]:
    prefix, items = query.split('_')
    return [int(x) for x in items.split('-') if x]


def build_query(prefix: str, selected_items: List[int]) -> str:
    return prefix + '_' + '-'.join([str(x) for x in selected_items])


def show_order_keys(update: Update, context: CallbackContext) -> None:
    logger.info(f'Show order keys at chat {update.effective_chat.id}')
    if is_group(update):
        update.message.reply_text(
            f'Команда работает только в приватном чате с @{context.bot.username}'
        )
        return

    if not menu_date or not menu_items:
        if update.callback_query:
            update.callback_query.message.edit_text('Меню не загружено 😿')
            update.callback_query.answer()
        else:
            update.message.reply_text('Меню еще не загружено 😿')
        return

    query = update.callback_query
    selected_items = []
    if query:
        query.answer()
        selected_items = parse_selected_items(query.data)

    keyboard = []
    columns = 2
    for i in range(0, len(menu_items), columns):
        row = []
        for j in range(columns):
            if i + j < len(menu_items):
                row.append(InlineKeyboardButton(
                    text=menu_items[i + j], callback_data=build_query('order', selected_items + [i + j])))
        keyboard.append(row)

    control_keys = []
    if selected_items:
        control_keys += [
            InlineKeyboardButton("✅", callback_data=build_query('confirm', selected_items)),
            InlineKeyboardButton("⬅️", callback_data=build_query('order', selected_items[:-1])),
        ]
    control_keys += [InlineKeyboardButton("❌", callback_data='cancel')]
    keyboard.append(control_keys)

    reply_text = f'Меню на {menu_date:%d.%m.%Y} 🗓\n\n{update.effective_user.last_name}:\n'
    if selected_items:
        reply_text += render_order(selected_items)
    else:
        reply_text += ' - выберите что-нибудь'

    reply_markup = InlineKeyboardMarkup(keyboard)
    if query:
        query.edit_message_text(text=reply_text, reply_markup=reply_markup)
    else:
        update.message.reply_text(reply_text, reply_markup=reply_markup)


def confirm_order(update: Update, context: CallbackContext) -> None:
    logger.info(f'Confirm order at chat {update.effective_message.chat_id}')
    query = update.callback_query
    query.answer()
    selected_items = parse_selected_items(query.data)
    order_message = mention_markdown(update.effective_user.id, update.effective_user.last_name, version=2) + ':\n'
    order_message += escape_markdown(render_order(selected_items), version=2)

    if user_belongs_to_group(update, context):
        logger.info(f'Send order to group {group_chat}')
        query.edit_message_text(text='Заказ создан 👌')
        # send to group
        chat_id = update.effective_chat.id
        message: Message = context.bot.send_message(chat_id=group_chat,
                                                    text=order_message,
                                                    parse_mode=ParseMode.MARKDOWN_V2)
        context.bot.forwardMessage(chat_id=chat_id,
                                   from_chat_id=message.chat_id,
                                   message_id=message.message_id)
    else:
        logger.warning(f'Confirm order at chat {update.effective_message.chat_id}, user does not belong to group')
        query.edit_message_text(text='Вы не состоите в группе. Перешлите заказ сами 😉')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=order_message,
                                 parse_mode=ParseMode.MARKDOWN_V2)


def cancel_order(update: Update, context: CallbackContext) -> None:
    logger.info(f'Cancel order at chat {update.effective_message.chat_id}')
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Отмена")


def photo_handler(update: Update, context: CallbackContext) -> None:
    logger.info(f'Photo handler at chat {update.effective_message.chat_id}')
    user_id = update.effective_user.id

    if user_id not in {admin_user, yummy_user}:
        return

    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    image_date = date_map.get(today, tomorrow)

    img = update.effective_message.photo[-1].get_file()
    image_name = f'{image_date.isoformat()}.jpeg'
    img.download(os.path.join('data', image_name))

    logger.info(f'Saving image: {image_name}')
    load_image()

    if user_id == admin_user:
        update.message.reply_text(f'🔄 Меню обновлено: {len(menu_items)} позиций')


def unknown_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="🤷‍ Неизвестная команда")
    logger.error(f'Unknown query: {query.data}')


if __name__ == '__main__':
    try:
        load_image()
    except Exception as e:
        logger.error(f'Error loading image: {e}')

    updater = Updater(bot_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', show_start_text))
    dispatcher.add_handler(CommandHandler('order', show_order_keys))
    dispatcher.add_handler(CallbackQueryHandler(show_order_keys, pattern='order.*'))
    dispatcher.add_handler(CallbackQueryHandler(confirm_order, pattern='confirm.*'))
    dispatcher.add_handler(CallbackQueryHandler(cancel_order, pattern='cancel'))
    dispatcher.add_handler(CallbackQueryHandler(unknown_query))

    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))

    updater.start_polling()
    updater.idle()
