from fastapi import FastAPI, HTTPException, Depends
import aioredis
import httpx
from sqlalchemy.orm import Session

from app.models import Usuario, Post
from app.schemas import UsuarioCreate, PostCreate
from app.database import get_db
from app.celery_app import celery
from app.configs import settings

app = FastAPI()

redis = aioredis.from_url(settings.redis_url)


@celery.task
def send_notification(post_id: int):
    try:
        response = httpx.post(settings.notification_service_url, json={"post_id": post_id})
        response.raise_for_status()
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")


@app.post("/usuarios/", response_model=UsuarioCreate)
async def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@app.get("/usuarios/{usuario_id}", response_model=UsuarioCreate)
async def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    cache_key = f"usuario:{usuario_id}"
    cached_usuario = await redis.get(cache_key)
    if cached_usuario:
        return UsuarioCreate.parse_raw(cached_usuario)

    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")

    await redis.set(cache_key, db_usuario.json(), ex=60)
    return db_usuario


@app.post("/posts/", response_model=PostCreate)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    send_notification.delay(db_post.id)
    return db_post


@app.get("/posts/{post_id}", response_model=PostCreate)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    cache_key = f"post:{post_id}"
    cached_post = await redis.get(cache_key)
    if cached_post:
        return PostCreate.parse_raw(cached_post)

    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    await redis.set(cache_key, db_post.json(), ex=60)
    return db_post