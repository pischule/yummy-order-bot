# Бот для заказа еды в офис

![GitHub top language](https://img.shields.io/github/languages/top/pischule/yummy-bot) [![build-publish](https://github.com/pischule/yummy-bot/actions/workflows/docker-build-publish.yml/badge.svg)](https://github.com/pischule/yummy-bot/actions/workflows/docker-build-publish.yml) ![Docker Pulls](https://img.shields.io/docker/pulls/pischule/yummy-bot)

- бот получает фото меню
 <img src="https://user-images.githubusercontent.com/41614960/162609029-5734fb1a-0cdf-4adb-809b-aac239ff21c6.jpeg" width="350">

- из картинки извлекаются регионы с текстом
 <img src="https://user-images.githubusercontent.com/41614960/162609053-bf175329-757d-4cab-9108-7235a8a405b5.png" width="350">

- регионы обрабатывает [OpenCV](https://opencv.org/)
- [Tesseract](https://github.com/tesseract-ocr/tesseract) извлекает текст
- пользователь видит кнопочки в чате
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

Настройки бота вынесены в файл .env:
```dotenv
BOT_TOKEN=*********
ADMIN_USER=11111111
GROUP_CHAT=22222222
YUMMY_USER=33333333
MENU_HOUR_START=9
MENU_HOUR_END=12
ORDER_HOUR_END=14
```

Для настройки регионов интереса (ROI) в боте есть команда <kbd>/roi</kbd> и соответствующее [приложение](https://pischule.github.io/yummy-bot/) в ветке [frontend](https://github.com/pischule/yummy-bot/tree/frontend)
<img width="785" alt="image" src="https://user-images.githubusercontent.com/41614960/162608913-122baab4-b1a0-43d1-95be-5fd6eea6377b.png">
<img width="785" alt="image" src="https://user-images.githubusercontent.com/41614960/162609297-19a2e03c-af6f-4650-8d0a-5d8a740dff1e.png">
