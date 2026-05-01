import math

def agent(obs):
    """
    Базовый (жадный) бот для Orbit Wars.
    Анализирует свои планеты и отправляет корабли на ближайшую вражескую или нейтральную планету.
    """
    planets = obs.get("planets", [])
    player = obs.get("player", 0)
    
    # Структура планеты: [id, owner, x, y, radius, ships, production]
    my_planets = [p for p in planets if p[1] == player]
    target_planets = [p for p in planets if p[1] != player]
    
    actions = []
    
    if not target_planets:
        return actions
        
    for p in my_planets:
        p_id, p_owner, p_x, p_y, p_rad, p_ships, p_prod = p
        
        # Если кораблей достаточно, часть отправляем в атаку
        if p_ships > 20:
            # Ищем ближайшую цель
            best_target = min(target_planets, key=lambda t: math.hypot(t[2] - p_x, t[3] - p_y))
            t_x, t_y = best_target[2], best_target[3]
            
            # Вычисляем угол в радианах
            angle = math.atan2(t_y - p_y, t_x - p_x)
            if angle < 0:
                angle += 2 * math.pi
                
            # Отправляем половину от имеющихся кораблей (простая эвристика)
            ships_to_send = int(p_ships // 2)
            actions.append([p_id, float(angle), ships_to_send])
            
    return actions
