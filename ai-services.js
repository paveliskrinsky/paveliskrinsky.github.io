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

function enhanceSelect(box) {
  const native = box.querySelector('select');
  const label = document.querySelector(`label[for="${native.id}"]`);
  const btn = document.createElement('button');
  const list = document.createElement('ul');
  const options = [...native.options].map((opt, i) => {
    const li = element('li', opt.textContent);
    li.className = 'select-option';
    li.id = `${native.id}-opt-${i}`;
    li.setAttribute('role', 'option');
    list.append(li);
    return li;
  });
  let active = native.selectedIndex;

  btn.type = 'button';
  btn.className = 'select-btn';
  btn.id = `${native.id}-btn`;
  btn.setAttribute('role', 'combobox');
  btn.setAttribute('aria-haspopup', 'listbox');
  btn.setAttribute('aria-controls', `${native.id}-list`);
  btn.setAttribute('aria-expanded', 'false');
  list.id = `${native.id}-list`;
  list.className = 'select-list';
  list.setAttribute('role', 'listbox');
  if (label) {
    label.htmlFor = btn.id;
    label.id = label.id || `${native.id}-label`;
    list.setAttribute('aria-labelledby', label.id);
  }
  native.classList.add('select-native');
  native.tabIndex = -1;
  native.setAttribute('aria-hidden', 'true');
  box.classList.add('is-enhanced');
  box.append(btn, list);

  const isOpen = () => box.classList.contains('is-open');

  function sync() {
    options.forEach((li, i) => {
      li.setAttribute('aria-selected', i === native.selectedIndex);
      li.classList.toggle('is-active', i === active);
    });
    btn.textContent = native.options[native.selectedIndex].textContent;
    if (isOpen()) btn.setAttribute('aria-activedescendant', options[active].id);
    else btn.removeAttribute('aria-activedescendant');
  }

  function setOpen(open) {
    box.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', open);
    active = native.selectedIndex;
    sync();
  }

  function pick(i) {
    native.selectedIndex = i;
    native.dispatchEvent(new Event('change', { bubbles: true }));
    setOpen(false);
    btn.focus();
  }

  function move(i) {
    active = Math.max(0, Math.min(options.length - 1, i));
    sync();
  }

  btn.addEventListener('click', () => setOpen(!isOpen()));
  btn.addEventListener('keydown', (e) => {
    const open = isOpen();
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      if (!open) setOpen(true);
      else move(active + (e.key === 'ArrowDown' ? 1 : -1));
    } else if ((e.key === 'Home' || e.key === 'End') && open) {
      e.preventDefault();
      move(e.key === 'Home' ? 0 : options.length - 1);
    } else if ((e.key === 'Enter' || e.key === ' ') && open) {
      e.preventDefault();
      pick(active);
    } else if (e.key === 'Escape' && open) {
      e.preventDefault();
      setOpen(false);
    } else if (e.key === 'Tab' && open) {
      setOpen(false);
    }
  });
  list.addEventListener('pointermove', (e) => {
    const i = options.indexOf(e.target.closest('.select-option'));
    if (i >= 0 && i !== active) {
      active = i;
      sync();
    }
  });
  list.addEventListener('click', (e) => {
    const i = options.indexOf(e.target.closest('.select-option'));
    if (i >= 0) pick(i);
  });
  document.addEventListener('pointerdown', (e) => {
    if (!box.contains(e.target)) setOpen(false);
  });
  native.addEventListener('change', () => {
    active = native.selectedIndex;
    sync();
  });
  sync();
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
document.querySelectorAll('[data-select]').forEach(enhanceSelect);
booking(false);
