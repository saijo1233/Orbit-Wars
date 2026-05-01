from kaggle_environments import make
import os

def test_match():
    # Создаем окружение
    env = make("orbit_wars", debug=True)
    
    # Запускаем матч: наш агент против встроенного starter_agent
    # Мы передаем путь к файлу нашего агента
    print("Starting match: agent.py vs starter...")
    env.run(["agent.py", "starter"])
    
    # Рендерим результат в HTML файл
    print("Rendering replay...")
    html = env.render(mode="html")
    
    # Сохраняем в файл
    output_path = "match_result.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Match finished! Replay saved to {os.path.abspath(output_path)}")

if __name__ == "__main__":
    test_match()
