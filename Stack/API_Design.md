# Дизайн API

В настоящее время используется встроенный API окружения Kaggle.
Основной интерфейс:
```python
def agent(obs):
    # Обработка наблюдений (observation)
    # Возврат действий (actions)
    return []
```

Наблюдение (obs) содержит:
- `planets`: `[[id, owner, x, y, radius, ships, production], ...]`
- `fleets`: `[[id, owner, x, y, angle, from_planet_id, ships], ...]`
- `player`: `int` (ваш id)
- `comets` и `comet_planet_ids`
- `angular_velocity`

Назад к [[index]]