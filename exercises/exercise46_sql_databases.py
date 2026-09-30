# 练习46：SQL数据库（SQL）
# 要求：根据注释要求实现相应的FastAPI应用
# 说明：需要 pip install sqlalchemy

from collections.abc import AsyncIterator, Generator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)
from sqlalchemy.pool import StaticPool

app = FastAPI()

# 题目1：创建引擎和基础
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


class Base(DeclarativeBase):
    pass

# 题目2：定义表模型
class Hero(Base):
    __tablename__ = "hero"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    secret_name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)

# 题目3：建表
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app.router.lifespan_context = lifespan
Base.metadata.create_all(bind=engine)

# 题目4：会话依赖
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]

# 题目5：CRUD路由
class HeroCreate(BaseModel):
    name: str
    secret_name: str
    age: int | None = None


class HeroRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    secret_name: str
    age: int | None = None


@app.post("/heroes/", response_model=HeroRead)
def create_hero(hero: HeroCreate, session: SessionDep) -> HeroRead:
    db_hero = Hero(name=hero.name, secret_name=hero.secret_name, age=hero.age)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return HeroRead.model_validate(db_hero)


@app.get("/heroes/", response_model=list[HeroRead])
def read_heroes(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[HeroRead]:
    heroes = session.scalars(select(Hero).offset(skip).limit(limit)).all()
    return [HeroRead.model_validate(hero) for hero in heroes]


@app.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int, session: SessionDep) -> HeroRead:
    hero = session.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    return HeroRead.model_validate(hero)


@app.delete("/heroes/{hero_id}", response_model=HeroRead)
def delete_hero(hero_id: int, session: SessionDep) -> HeroRead:
    hero = session.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    result = HeroRead.model_validate(hero)
    session.delete(hero)
    session.commit()
    return result

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
