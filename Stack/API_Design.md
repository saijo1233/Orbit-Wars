# API Design

Currently using the built-in Kaggle Environment API.
The core interface:
```python
def agent(obs):
    # Process observation
    # Return actions
    return []
```

Observation contains:
- `planets`: `[[id, owner, x, y, radius, ships, production], ...]`
- `fleets`: `[[id, owner, x, y, angle, from_planet_id, ships], ...]`
- `player`: `int` (your id)
- `comets` and `comet_planet_ids`
- `angular_velocity`

Back to [[index]]