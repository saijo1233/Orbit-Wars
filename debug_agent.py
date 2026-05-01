from kaggle_environments import make

env = make('orbit_wars', debug=False)
env.reset()

state = env.state
obs = state[0].observation
obs_dict = {
    'planets': obs.planets,
    'fleets': obs.fleets,
    'player': obs.player,
    'angular_velocity': obs.angular_velocity,
    'initial_planets': obs.initial_planets,
    'comets': obs.comets,
    'comet_planet_ids': obs.comet_planet_ids,
    'step': 0,
}

import importlib.util
spec = importlib.util.spec_from_file_location('agent', 'agent.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print("=== Turn 0 Debug ===")
my_planets = [p for p in obs.planets if p[1] == 0]
neutral = [p for p in obs.planets if p[1] == -1]
print(f"My planets: {[(p[0], 'ships='+str(p[5]), 'prod='+str(p[6])) for p in my_planets]}")
print(f"Neutral count: {len(neutral)}, top by prod:", sorted([(p[5], p[6]) for p in neutral], key=lambda x: -x[1])[:5])

actions = mod.agent(obs_dict)
print(f"Actions produced ({len(actions)}): {actions}")
