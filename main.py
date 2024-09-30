from aiogram import executor

from create import disp
from handlers import start, registration
from handlers.filters import filter_sent, send_location

start.reg_start(disp)
registration.reg_registration(disp)
filter_sent.reg_filter_sent(disp)
send_location.reg_send_location(disp)

executor.start_polling(disp, skip_updates=True)
