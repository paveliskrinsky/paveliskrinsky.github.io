# Павел Искринский — Фронтенд-разработчик

Персональный сайт-портфолио: [paveliskrinsky.github.io](https://paveliskrinsky.github.io)

На сайте:

- **Обо мне** — кратко об опыте и специализации
- **Опыт работы** — No Logo Studio, фриланс и аутсорс, Nisanov Corp, freelance.ru
- **Навыки** — AI-разработка и процесс работы с AI, вёрстка, JavaScript, сборка, работа с макетами, CMS, оптимизация
- **Проекты** — с замерами PageSpeed Insights: Зеленогорский зоопарк (test.zelzoo.ru), Ввези.ru (vvezi.ru, личный проект), КодРазбор (kodrazbor.ru) и АвтоПарам (autoparam.ru) — личные AI-проекты, АО «КемВод» (kemvod.ru)
- **Отзывы** — цитаты заказчиков с freelance.ru
- **Контакты** — e-mail, Telegram, GitHub, резюме на hh.ru и форма обратной связи

## Стек

Один файл `index.html`: HTML, CSS и ванильный JavaScript без фреймворков и сборки. Картинки в AVIF/WebP/JPG с `srcset`: исходники лежат в `_src/`, оптимизированные версии собираются в `img/` скриптами `python tools/images.py` и `python tools/previews.py` (скриншоты проектов), замеры Lighthouse — `python tools/pagespeed.py`. Светлая и тёмная тема по системным настройкам, адаптив под мобильные. Форма работает через Formspree, хостинг — GitHub Pages.
