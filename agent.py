import math

def calculate_speed(ships):
    if ships <= 1:
        return 1.0
    return 1.0 + 5.0 * (math.log(ships) / math.log(1000.0)) ** 1.5

def predict_planet_position(t_x, t_y, t_rad, angular_velocity, travel_time):
    # Check if planet rotates
    center_dist = math.hypot(t_x - 50.0, t_y - 50.0)
    if center_dist + t_rad >= 50.0 or angular_velocity == 0:
        return t_x, t_y # Static planet
    
    # Orbiting planet
    current_angle = math.atan2(t_y - 50.0, t_x - 50.0)
    future_angle = current_angle + angular_velocity * travel_time
    
    future_x = 50.0 + center_dist * math.cos(future_angle)
    future_y = 50.0 + center_dist * math.sin(future_angle)
    
    return future_x, future_y

def agent(obs):
    """
    Продвинутый бот для Orbit Wars.
    Использует предсказание движения планет (advanced routing) для вычисления точки перехвата.
    """
    planets = obs.get("planets", [])
    player = obs.get("player", 0)
    angular_velocity = obs.get("angular_velocity", 0.0)
    
    my_planets = [p for p in planets if p[1] == player]
    target_planets = [p for p in planets if p[1] != player]
    
    actions = []
    
    if not target_planets:
        return actions
        
    for p in my_planets:
        p_id, p_owner, p_x, p_y, p_rad, p_ships, p_prod = p
        
        if p_ships > 20:
            ships_to_send = int(p_ships // 2)
            speed = calculate_speed(ships_to_send)
            
            # Ищем ближайшую цель
            best_target = min(target_planets, key=lambda t: math.hypot(t[2] - p_x, t[3] - p_y))
            t_x, t_y, t_rad = best_target[2], best_target[3], best_target[4]
            
            # Итеративное предсказание (2 итерации для точности)
            predicted_x, predicted_y = t_x, t_y
            for _ in range(2):
                dist = math.hypot(predicted_x - p_x, predicted_y - p_y)
                travel_time = dist / speed
                predicted_x, predicted_y = predict_planet_position(t_x, t_y, t_rad, angular_velocity, travel_time)
            
            angle = math.atan2(predicted_y - p_y, predicted_x - p_x)
            if angle < 0:
                angle += 2 * math.pi
                
            actions.append([p_id, float(angle), ships_to_send])
            
    return actions
