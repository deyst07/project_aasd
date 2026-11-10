import os
import sys
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from database.database import SessionLocal
from models.models import GoogleApp
from algorithms.hash_table import MyHashMap

def build_and_save_cache():
    print("Старт генерации файла хэш-таблицы...")
    
    app_hash_map = MyHashMap(capacity=2500000)
    
    db = SessionLocal()
    try:
        batch_size = 100000
        offset = 0
        
        while True:
            print(f"Выкачиваем строки с {offset} по {offset + batch_size}...")
            apps_batch = (
                db.query(GoogleApp)
                .order_by(GoogleApp.app_id)
                .offset(offset)
                .limit(batch_size)
                .all()
            )
            
            if not apps_batch:
                break
                
            for app_obj in apps_batch:
                app_dict = {
                    "app_name": app_obj.app_name,
                    "category": app_obj.category,
                    "rating": app_obj.rating,
                    "maximum_installs": app_obj.maximum_installs,
                    "price": app_obj.price,
                    "currency": app_obj.currency,
                    "free": app_obj.free
                }
                app_hash_map.put(app_obj.app_id, app_dict)
                
            offset += batch_size
            
        print(f"Хэш-таблица собрана! Всего элементов: {len(app_hash_map)}")
        print("Сохраняем файл на диск (hash_map_cache.pkl)...")
        
        with open("hash_map_cache.pkl", "wb") as f:
            pickle.dump(app_hash_map, f)
            
        print("Успешно сохранено! Теперь проект будет запускаться мгновенно.")
        
    except Exception as e:
        print(f"Ошибка сборки: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    build_and_save_cache()
