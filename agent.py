import math

def calculate_speed(ships):
    """
    Вычисляет скорость флота согласно правилам игры:
    Скорость масштабируется логарифмически от 1.0 до 6.0 (max_speed).
    """
    if ships <= 1:
        return 1.0
    # max_speed = 6.0 по умолчанию в конфиге
    log_ships = math.log(min(ships, 1000))
    log_max = math.log(1000)
    return 1.0 + 5.0 * (log_ships / log_max) ** 1.5

def predict_position(target, angular_velocity, travel_time, comet_groups):
    """
    Предсказывает будущие координаты планеты или кометы.
    """
    t_id, t_owner, t_x, t_y, t_rad, t_ships, t_prod = target
    
    # Проверяем, является ли объект кометой
    for group in comet_groups:
        if t_id in group['planet_ids']:
            p_idx = group['planet_ids'].index(t_id)
            future_idx = group['path_index'] + int(travel_time)
            path = group['paths'][p_idx]
            if future_idx < len(path):
                return path[future_idx][0], path[future_idx][1], True
            else:
                return -999, -999, True # Комета исчезнет
    
    # Обычная планета
    center_dist = math.hypot(t_x - 50.0, t_y - 50.0)
    # Планеты вращаются только если они внутри ROTATION_RADIUS_LIMIT (50.0)
    if center_dist + t_rad >= 50.0 or angular_velocity == 0:
        return t_x, t_y, False # Статичная планета
    
    current_angle = math.atan2(t_y - 50.0, t_x - 50.0)
    future_angle = current_angle + angular_velocity * travel_time
    
    future_x = 50.0 + center_dist * math.cos(future_angle)
    future_y = 50.0 + center_dist * math.sin(future_angle)
    
    return future_x, future_y, False

def agent(obs):
    """
    Улучшенный агент с поддержкой захвата комет и умным выбором целей.
    """
    planets = obs.get("planets", [])
    player = obs.get("player", 0)
    angular_velocity = obs.get("angular_velocity", 0.0)
    comet_groups = obs.get("comets", [])
    
    my_planets = [list(p) for p in planets if p[1] == player]
    target_planets = [p for p in planets if p[1] != player]
    
    actions = []
    
    if not target_planets or not my_planets:
        return actions

    for p in my_planets:
        p_id, p_owner, p_x, p_y, p_rad, p_ships, p_prod = p
        
        # Минимальный порог для отправки флота
        if p_ships < 15:
            continue
            
        ships_to_send = int(p_ships * 0.6) # Отправляем 60% гарнизона
        speed = calculate_speed(ships_to_send)
        
        best_score = -1e9
        best_target_coords = (0, 0)
        selected_target_id = None
        
        for t in target_planets:
            t_id, t_owner, t_x, t_y, t_rad, t_ships, t_prod = t
            
            # Итеративное предсказание позиции (2 итерации)
            pred_x, pred_y = t_x, t_y
            is_expired = False
            for _ in range(2):
                dist = math.hypot(pred_x - p_x, pred_y - p_y)
                travel_time = dist / speed
                pred_x, pred_y, is_comet = predict_position(t, angular_velocity, travel_time, comet_groups)
                if pred_x < 0:
                    is_expired = True
                    break
            
            if is_expired:
                continue
                
            dist = math.hypot(pred_x - p_x, pred_y - p_y)
            if dist < 1.0: dist = 1.0
            
            # Расчет необходимых сил
            if t_owner == -1:
                # Нейтральная планета (корабли не производятся)
                needed = t_ships + 1
            else:
                # Вражеская планета (производство продолжается во время полета)
                needed = t_ships + t_prod * (dist / speed) + 2
                
            # Эвристика: ценность цели / расстояние
            # Кометы имеют высокий приоритет из-за стратегической важности
            priority = 1.0
            if is_comet:
                priority = 3.0
            elif t_owner == -1:
                priority = 1.5
                
            score = (t_prod * 100 * priority) / (dist ** 1.2)
            
            if ships_to_send > needed:
                if score > best_score:
                    best_score = score
                    selected_target_id = t_id
                    best_target_coords = (pred_x, pred_y)
        
        if selected_target_id is not None:
            angle = math.atan2(best_target_coords[1] - p_y, best_target_coords[0] - p_x)
            actions.append([p_id, float(angle), ships_to_send])
            # Виртуально вычитаем корабли, чтобы не отправить их дважды в одном ходу
            p[5] -= ships_to_send

    return actions
