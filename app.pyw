from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from os import system
import pyautogui as pag
from ctypes import *
import webbrowser as wb
import cv2 
from PIL import Image
from PIL import Image, ImageDraw, ImageFont
import pyttsx3
import json

config = json.load(open('config.json'))

buts = [['q','й'],['w','ц'],['e','у'],['r','к'],['t','е'],['y','н'],['u','г'],['i','ш'],['o','щ'],['p','з'],['[','х'],[']','ъ'],['a','ф'],['s','ы'],['d','в'],['f','а'],['g','п'],['h','р'],['j','о'],['k','л'],['l','д'],[';','ж'],["'",'э'],['z','я'],['x','ч'],['c','с'],['v','м'],['b','и'],['n','т'],['m','ь'],[',','б'],['.','ю']]

try:
    s_engn = pyttsx3.init()
    for i in s_engn.getProperty('voices'):
        if i.name == 'Elena':
            s_engn.setProperty('voice',i.id)
except:
    pass

def say(text):
    try:
        s_engn.say(text)
        s_engn.runAndWait()
    except:
        pass

bot = Bot(token=config['token'])
dp = Dispatcher(bot)

def create_kb(kb_type):
    if kb_type == 'menu':
        kb_button1 = KeyboardButton('Л.Клик')
        kb_button2 = KeyboardButton('П.Клик')
        kb_button3 = KeyboardButton('Состояние')
        kb_button4 = KeyboardButton('Скриншот')
        kb_button5 = KeyboardButton('Скрин с сеткой')
        kb_button6 = KeyboardButton('Сменить раскладку')
        kb_button7 = KeyboardButton('Отправить')
        kb_button8 = KeyboardButton('Отменить')
        kb_button9 = KeyboardButton('Спец. меню')
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(kb_button1, kb_button2, kb_button3, kb_button4, kb_button5, kb_button6, kb_button7, kb_button8, kb_button9)
        return kb
    elif kb_type == 'spec_menu':
        kb_button1 = KeyboardButton('В спящий режим')
        kb_button2 = KeyboardButton('Заблокировать')
        kb_button3 = KeyboardButton('Блокировать ввод')
        kb_button4 = KeyboardButton('Разблокировать ввод')
        kb_button5 = KeyboardButton('Выйти')
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(kb_button1, kb_button2, kb_button3, kb_button4, kb_button5)
        return kb


@dp.message_handler()
async def cmd_test1(message: types.Message):
    global block
    if message.text in ('/start','Выйти'):
        await message.answer('Здравствуйте, сэр',reply_markup=create_kb('menu'))        
    elif 'Блокировать ввод' in message.text:
        windll.user32.BlockInput(True)
        await message.answer('Ввод заблокирован')
    elif 'Разблокировать ввод' in message.text:
        windll.user32.BlockInput(False)
        await message.answer('Ввод разблокирован')
    elif 'В спящий режим' in message.text:
        await message.answer('Компьютер введён в спящий режим')
        system("powercfg -hibernate off")
        system(r'rundll32.exe powrprof.dll,SetSuspendState Standby')
    elif '/say ' in message.text:
        text = message.text.replace('/say ','')
        say(text)
        await message.answer(f'Произнесено: {text}')
    elif 'Отменить' in message.text:
        pag.hotkey('ctrl','z')
        await message.answer('Последнее действие отменено')
    elif 'Сменить раскладку' in message.text:
        pag.hotkey('shift','alt')
        await message.answer('Раскладка изменена')
    elif '/type ' in message.text:
        pre_text = message.text.replace('/type ','')
        text = ''
        for i in pre_text:
            if i in ('йцукенгшщзхъфывапролджэячсмитьбю'):
                for j in buts:
                    if j[1] == i:
                        text += j[0]
            else:
                text += i
        pag.typewrite(text)
        await message.answer(f'Напечатан текст: {text}')
    elif 'Спец. меню' in message.text:
        await message.answer('Специальное меню',reply_markup=create_kb('spec_menu'))
    elif 'Заблокировать' in message.text:
        windll.user32.LockWorkStation()
        await message.answer('Компьютер заблокирован')
    elif '/eval ' in message.text:
        await message.answer(eval(message.text.replace('/eval ','')))
    elif '/open ' in message.text:
        site = message.text.replace('/open ','')
        wb.open_new_tab(site)
        await message.answer(f'Открыт сайт: {site}')
    elif 'Скриншот' in message.text:
        pag.screenshot('screen.png')
        with open('screen.png','rb') as img:
            await bot.send_photo(message.chat.id,img)
    elif 'Состояние' in message.text:
        await message.answer('Обработчик работает')
    elif '/move ' in message.text:
        args = message.text.replace('/move ','').split()
        pag.moveTo(int(args[0]),int(args[1]))
        await message.answer(f'Курсор перемещён на {args[0]}, {args[1]}')
    elif 'П.Клик' in message.text:
        pag.click(button='right')
        await message.answer('Вы нажали ПКМ')
    elif 'Л.Клик' in message.text:
        pag.click(button='left')
        await message.answer('Вы нажали ЛКМ')
    elif 'Отправить' in message.text:
        pag.hotkey('enter')
        await message.answer('Вы нажали Enter')    
    elif '/hk2' in message.text:
        args = message.text.replace('/hk2 ','').split()
        pag.hotkey(args[0],args[1])
        await message.answer(f'Вы нажали {args[0]}+{args[1]}')
    elif '/hk3' in message.text:
        args = message.text.replace('/hk3 ','').split()
        pag.hotkey(args[0],args[1],args[2])
        await message.answer(f'Вы нажали {args[0]}+{args[1]}+{args[2]}')
    else:
        if len(message.text.split()) == 1:
            pag.press(message.text)
            await message.answer(f'Вы нажали клавишу {message.text}')
        else:
            pass

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
