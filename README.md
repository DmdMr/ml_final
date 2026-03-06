# Credit Scoring (UCI Credit Card)

Проект предсказывает вероятность дефолта клиента по кредитной карте в следующем месяце и рассчитывает кредитный рейтинг/категорию риска.

## Что было не так
В датасете целевая колонка часто называется `default.payment.next.month`, а не `default payment next month`. Из-за этого переименование не срабатывало и пайплайн падал с `KeyError: 'default'`.

## Исправление
Исправлены `main.ipynb` и `main.py`:
- добавено устойчивое определение целевой колонки с поддержкой вариантов:
  - `default`
  - `default payment next month`
  - `default.payment.next.month`
- после определения колонка приводится к единому имени `default`;
- остальной pipeline (feature engineering, обучение, scoring и risk segmentation) работает без изменений.

## Запуск
```bash
python main.py
```
