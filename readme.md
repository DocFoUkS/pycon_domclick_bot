# pycon_domclick_bot

Тестовый бот для работы с оформлением ипотеки на ДомКлик.

Бот умеет следующее:
* Приветсвует пользователя по команде /start
* Просит ввести запрашиваемую сумму кредита и проверяет ее валидность
* Просит ввести сумму первоначального взноса. Проверяет, что она не меньше 15% от запрашиваемой суммы кредита. Если меньше - просит увеличить сумму первоначального взноса;
* Если все ок - сообщает пользователю, что он может подать онлайн-заявку на ипотеку на сайте https://domclick.ru/ipoteka/programs/onlajn-zayavka.