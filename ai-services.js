const bookingBody = document.getElementById('booking-body');
const topics = ['Сайт для студии', 'Автоматизация заявок'];
const times = ['Во вторник утром', 'В пятницу после 14:00'];

function element(tag, text) {
  const node = document.createElement(tag);
  node.textContent = text;
  return node;
}

function choose(prompt, choices, onSelect, moveFocus = true) {
  const question = element('p', prompt);
  question.tabIndex = -1;
  const actions = document.createElement('div');
  actions.className = 'actions';
  for (const choice of choices) {
    const button = element('button', choice);
    button.type = 'button';
    button.addEventListener('click', () => onSelect(choice));
    actions.append(button);
  }
  bookingBody.replaceChildren(question, actions);
  if (moveFocus) question.focus({ preventScroll: true });
}

function booking(moveFocus = true) {
  choose('По какой теме хотите проконсультироваться?', topics, topic => {
    choose('Когда вам удобно получить ответ?', times, time => {
      choose(`Проверьте заявку. Тема — ${topic.toLowerCase()}. Время — ${time.toLowerCase()}. Контакт для демо — @demo_client.`,
        ['Подтвердить', 'Начать заново'], action => {
          if (action === 'Начать заново') {
            booking();
            return;
          }
          choose(`Карточка менеджера: ${topic} · ${time} · @demo_client. Следующий шаг — подтвердить встречу с клиентом.`,
            ['Пройти ещё раз'], () => booking());
        });
    });
  }, moveFocus);
}

const examples = {
  landing: {
    letter: 'Нужен лендинг к выставке 18 мая. Макет в Figma готов, бюджет до 80 000 ₽. Успеете?',
    job: 'Сверстать лендинг по готовому макету Figma.',
    date: 'Выставка 18 мая. Дата запуска требует уточнения.',
    budget: 'До 80 000 ₽.',
    reply: 'Пришлите ссылку на макет и подскажите, за сколько дней до выставки нужно запустить лендинг. После просмотра оценю срок.'
  },
  shop: {
    letter: 'На телефоне у покупателей пропадает кнопка оформления. Магазин на OpenCart. Посмотрите на этой неделе?',
    job: 'Исправить кнопку оформления заказа на телефонах. Магазин на OpenCart.',
    date: 'На этой неделе клиент просит посмотреть проблему. Срок исправления предстоит согласовать.',
    budget: 'Не указан.',
    reply: 'Пришлите ссылку на магазин и, если есть, снимок экрана. На какой модели телефона пропадает кнопка?'
  },
  bot: {
    letter: 'Мы мастерская. По вечерам клиенты пишут в Telegram про запись. Хотим, чтобы бот собирал обращения до открытия. Бюджет обсудим.',
    job: 'Собирать вечерние заявки мастерской в Telegram.',
    date: 'Не указан.',
    budget: 'Предстоит согласовать.',
    reply: 'Какие сведения вы обычно спрашиваете при записи и куда удобнее получать заявки утром? Подскажите также желаемую дату запуска.'
  }
};

const selector = document.getElementById('brief-example');
const result = document.getElementById('brief-result');
selector.addEventListener('change', () => {
  document.getElementById('brief-letter').textContent = examples[selector.value].letter;
  result.replaceChildren();
});
document.getElementById('parse-brief').addEventListener('click', () => {
  const brief = examples[selector.value];
  const fields = document.createElement('dl');
  for (const [label, value] of [['Задача', brief.job], ['Срок', brief.date], ['Бюджет', brief.budget], ['Черновик ответа', brief.reply]]) {
    fields.append(element('dt', label), element('dd', value));
  }
  result.replaceChildren(fields);
});
booking(false);
