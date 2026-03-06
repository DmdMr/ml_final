# Credit Scoring (UCI Credit Card)

Проект предсказывает вероятность дефолта клиента по кредитной карте в следующем месяце и рассчитывает кредитный рейтинг/категорию риска.

## Почему возникал `KeyError: 'default'`
В вашем CSV цель называется `default.payment.next.month`, а код дальше обращался к `df['default']`. Если переименование колонки не произошло, строка `y = df['default']` падает с `KeyError`.

## Что исправлено
Обновлены `main.py` и `main.ipynb`:
- добавлен устойчивый поиск целевой колонки через нормализацию имени (точки/подчёркивания/пробелы считаются эквивалентными);
- поддерживаются варианты: `default`, `default payment next month`, `default.payment.next.month`, `default_payment_next_month`;
- после определения цель приводится к единому имени `default`, и пайплайн продолжает работу.

## Запуск
```bash
python main.py
```

## Если запускаете ноутбук в VS Code/Jupyter
После изменения кода обязательно сделайте **Restart Kernel** и затем **Run All**, чтобы не осталось старых переменных в памяти.

## Как решить merge conflicts в вашем PR (README.md, main.ipynb, main.py)
### Вариант A (проще): через локальный git + VS Code
```bash
git checkout <ваша-ветка>
git fetch origin
git merge origin/main
```

Дальше откройте VS Code:
- Source Control → откройте каждый конфликтный файл;
- выбирайте **Accept Current / Accept Incoming / Accept Both**;
- удалите все маркеры `<<<<<<<`, `=======`, `>>>>>>>`;
- сохраните файлы.

Затем завершите merge:
```bash
git add README.md main.ipynb main.py
git commit -m "Resolve merge conflicts with main"
git push
```

### Вариант B (GitHub web editor)
На странице PR нажмите **Resolve conflicts**, вручную оставьте нужный итоговый текст без маркеров конфликтов и нажмите **Mark as resolved** → **Commit merge**.

### Что выбрать в вашем случае
- Для `README.md`: обычно лучше **Accept current change** (ваша более новая версия с `KeyError: 'default'` и kernel restart), затем вручную проверить, что нет дублирования блоков.
- Для `main.py` и `main.ipynb`: оставьте версию с нормализацией названия таргета (`default.payment.next.month`/`default payment next month`/`default`).

Если хотите, я могу дать готовый “final merged” текст для каждого из 3 файлов, чтобы просто вставить и закоммитить.
