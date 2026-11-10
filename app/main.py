import os
import pickle

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from algorithms.binary_search import binary_search_on_answer
from algorithms.hash_table import MyHashMap
from database.database import get_db, engine, Base, SessionLocal
from models.models import GoogleApp

# Base.metadata.create_all(bind=engine)

app_hash_map = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global app_hash_map
    cache_path = "hash_map_cache.pkl"
    
    if os.path.exists(cache_path):
        print("Обнаружен готовый кэш! Мгновенная загрузка Хэш-таблицы с диска...")
        with open(cache_path, "rb") as f:
            app_hash_map = pickle.load(f)
        print(f"Хэш-таблица успешно загружена из файла! Элементов: {len(app_hash_map)}")
    else:
        print("Файл кэша hash_map_cache.pkl не найден!")
        print("Инициализируем пустую хэш-таблицу. Запусти build_cache.py для генерации.")
        app_hash_map = MyHashMap(capacity=16)
        
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory='templates')


@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context = {}
    )

@app.get('/apps', response_class=HTMLResponse)
def apps_table(request: Request, page: int = 1):
    if app_hash_map is None:
        return templates.TemplateResponse(
            request=request, name="apps.html", context={"request": request, "apps": [], "page": page}
        )
        
    limit = 50 
    start_index = (page - 1) * limit  
    end_index = start_index + limit

    apps_from_cache = app_hash_map.all_apps_list[start_index:end_index]

    return templates.TemplateResponse(
        request=request,
        name="apps.html",
        context={
            "request": request,
            "apps": apps_from_cache,
            "page" : page
        }
    )

# @app.get("/analysis", response_class=HTMLResponse)
# def analysis_page(request: Request, db: Session = Depends(get_db)):
#     apps_data = db.query(GoogleApp).limit(5000).all()

#     required_count = 50
#     calculated_min_price = binary_search_on_answer(apps_data, target_count = required_count)

#     return templates.TemplateResponse(
#         request=request,
#         name="analysis.html",
#         context={
#             "request": request,
#             "min_price": calculated_min_price,
#             "required_count": required_count,
#             "total_analyzed": len(apps_data)
#         }
#     )

@app.post("/search-id", response_class=HTMLResponse)
def search_by_id(request: Request, app_id: str = Form(...)):
    target_id = app_id.strip()
    
    if app_hash_map is not None:
        found_app = app_hash_map.get(target_id)
        hash_stats = app_hash_map.stats()
    else:
        found_app = None
        hash_stats = {"size": 0, "capacity": 0, "load_factor": 0,
                      "empty_buckets": 0, "max_bucket_size": 0}
    
    return templates.TemplateResponse(
        request=request,
        name="search_result.html",
        context={
            "request": request,
            "app_id": target_id,
            "app": found_app,
            "stats": hash_stats
        }
    )

