"""Test bot for applying for a mortgage."""

import logging
import os
from typing import Union

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = os.environ.get('MORTAGE_BOT_KEY')
USER_STEP = 0
CREDIT = 0

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
if API_TOKEN:
    logging.info('Start bot!')
else:
    logging.error('Not set bot api key!')
bot = Bot(token=API_TOKEN)
bot_dispatcher = Dispatcher(bot)


def check_credit_sum(credit: str) -> Union[int, float]:
    """Check credit summ from message and return sum in int or float.
    
    :param credit: text with credit.
    :type credit" str
    
    :return: Credit sum in float or int.
    :rtype: Union[int, float]
    """
    if credit.count('.') == 1:
        return float(credit)
    elif credit.count('.') > 1:
        credit = credit.replace('.', '')
        return int(credit)
    return int(credit)
    

def check_initial_payment(payment: Union[int, float], credit: Union[int, float]) -> bool:
    """Check initial payment.
    
    If payment < 15% of credit - return False. Else - True.
    
    :param payment: payment value.
    :type payment: Union[int, float]
    
    :param credit: credit value.
    :type credit: Union[int, float]
    
    :return: Checking that the initial payment is more than 15%.
    :rtype: bool
    """
    return payment >= (credit / 100) * 15


@bot_dispatcher.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """This handler will be called when user sends `/start` command.
    
    :param message: command from user.
    :type message: types.Message
    """
    global USER_STEP
    await message.answer(
        f"Привет, {message.from_user.full_name}!"
        '\nЯ супер бот для подачи заявки на ипотеку на твое жилье мечты!'
        'Я подсчитаю хватит ли тебе первоначального взноса и помогу оформить заявку!'
        "\nДерзай!"
    )
    await message.answer('Введи сумму кредита на жилье, которое хочешь купить.')
    USER_STEP = 1


@bot_dispatcher.message_handler()
async def echo(message: types.Message):
    """Handler for parse answers and send message to user.
    
    :param message: message from user.
    :type message: types.Message
    """
    global USER_STEP, CREDIT
    message_text = message.text
    message_text = message_text.replace(' ', '').replace(',', '.')
    if message_text.count('.') == 1:
        if USER_STEP == 1:
            if message_text.replace('.', '').isdigit():
                CREDIT = check_credit_sum(message_text)
                await message.answer('Введите сумму первоначального взноса.')
                USER_STEP = 2
            else:
                await message.answer('Введите, пожалуйста, число.')
        elif USER_STEP == 2:
            if message_text.replace('.', '').isdigit():
                payment = check_credit_sum(message_text)
                if check_initial_payment(payment, CREDIT):
                    await message.answer(
                        'Прекрасно! Вы можете оформить заявку на ипотеку по ссылке:\n'
                        'https://domclick.ru/ipoteka/programs/onlajn-zayavka'
                    )
                    USER_STEP = 0
                else:
                    await message.answer(
                        'Первоначального взноса не хватает! Он должен быть более 15% от суммы кредита.'
                        f'Первоначальный взнос должен быть больше {(CREDIT / 100) * 15}.'
                    )
            else:
                await message.answer('Введите, пожалуйста, число.')
    else:
        await message.answer('Я пока не научился полноценно болтать( Подождите немного. Я обязательно научусь!')
        

if __name__ == '__main__':
    executor.start_polling(bot_dispatcher, skip_updates=True)