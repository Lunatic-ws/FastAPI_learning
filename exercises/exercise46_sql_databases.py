# 练习46：SQL数据库（SQL）
# 要求：根据注释要求实现相应的FastAPI应用
# 说明：需要 pip install sqlalchemy

# 题目1：创建引擎和基础
# 使用 create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
# 创建 Base = declarative_base()

# 题目2：定义表模型
# 创建Hero表模型(Base)：id(Integer主键自增), name(String索引), secret_name(String必填), age(Integer可选)

# 题目3：建表
# 在启动时执行 Base.metadata.create_all(bind=engine) 创建所有表

# 题目4：会话依赖
# 创建 SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 实现get_session依赖：yield session，finally中session.close()

# 题目5：CRUD路由
# POST /heroes/  接收HeroCreate模型(name, secret_name, age可选)，创建并返回新英雄
# GET /heroes/   返回英雄列表（支持skip和limit分页参数）
# GET /heroes/{hero_id}  不存在时返回404
# DELETE /heroes/{hero_id}  删除并返回删除的英雄
# Session依赖统一使用 Annotated[Session, Depends(get_session)]

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
