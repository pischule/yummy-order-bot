# Бот для заказа еды в офис

![GitHub top language](https://img.shields.io/github/languages/top/pischule/yummy-bot) [![build-publish](https://github.com/pischule/yummy-bot/actions/workflows/docker-build-publish.yml/badge.svg)](https://github.com/pischule/yummy-bot/actions/workflows/docker-build-publish.yml) ![Docker Pulls](https://img.shields.io/docker/pulls/pischule/yummy-bot)

- бот получает фото меню
 <img src="https://user-images.githubusercontent.com/41614960/160286923-fdb716c2-b2a9-4ac1-9682-411e31dc384d.jpeg" width="350">

- картинка парсится [OpenCV](https://opencv.org/) и [Tesseract](https://github.com/tesseract-ocr/tesseract)
- пользователь видит удобный интерфейс
 <img src="https://user-images.githubusercontent.com/41614960/160286753-e905577e-4f81-47e8-b4be-0d1777f49eb5.jpg" width="350">

---

.env:
```dotenv
BOT_TOKEN=*********
ADMIN_USER=11111111
GROUP_CHAT=22222222
YUMMY_USER=33333333
MENU_HOUR_START=9
MENU_HOUR_END=12
ORDER_HOUR_END=14
```