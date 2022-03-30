# Бот для заказа еды в офис

![GitHub top language](https://img.shields.io/github/languages/top/pischule/yummy-bot) [![build-publish](https://github.com/pischule/yummy-bot/actions/workflows/docker-build-publish.yml/badge.svg)](https://github.com/pischule/yummy-bot/actions/workflows/docker-build-publish.yml) ![Docker Pulls](https://img.shields.io/docker/pulls/pischule/yummy-bot)

- бот получает фото меню
 <img src="https://user-images.githubusercontent.com/41614960/160286923-fdb716c2-b2a9-4ac1-9682-411e31dc384d.jpeg" width="350">

- картинка парсится [OpenCV](https://opencv.org/) и [Tesseract](https://github.com/tesseract-ocr/tesseract)
- пользователь видит удобный интерфейс
<table>
 <tr>
  <td> 
   <img src="https://user-images.githubusercontent.com/41614960/160935556-8779e0f9-694b-4f63-a080-fbac6a2d6a2c.jpg" width="330">
  </td>
  <td>
   <img src="https://user-images.githubusercontent.com/41614960/160935616-50fa48ef-2317-437d-a46e-21e0b8504743.jpg" width="330">
  </td>
 </tr>
</table>

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
