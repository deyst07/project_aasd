def check_condition(x: float, data: list, target_count: int = 10) -> bool:
    """
    Предикат (функция-чеккер): проверяет, выполняется ли условие при заданном значении x.
    Например: сколько приложений имеют цену меньше или равную x, и при этом они популярны.
    """
    count = 0
    for app in data:
        if app.price is not None and app.price <= x:
            count += 1
            
    return count >= target_count

def binary_search_on_answer(data: list, target_count: int = 10) -> float:
    """
    Ищет минимально возможную цену, удовлетворяющую чекеру.
    """
    if not data:
        return 0.0

    prices = [app.price for app in data if app.price is not None]
    if not prices:
        return 0.0
        
    left = 0.0
    right = max(prices)
    
    epsilon = 0.01 

    while right - left > epsilon:
        mid = (left + right) / 2.0
        
        if check_condition(mid, data, target_count):
            right = mid
        else:
            left = mid
            
    return round(right, 2)