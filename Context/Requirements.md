# Requirements

Based on the parsed Orbit Wars rules (see [[Data/Parsed/Orbit_Wars/index|Parsed Task Requirements]]):

- **Environment**: Kaggle environment `kaggle_environments.envs.orbit_wars`
- **Output**: The agent must return a list of fleets to launch: `[[from_planet_id, direction_angle, num_ships], ...]`
- **Constraints**:
    - Maximum 500 turns.
    - `actTimeout`: 1 second per turn.
- **Goal**: Maximize total ships on owned planets and owned fleets at the end of the game or upon elimination of all enemies.

Back to [[index]]