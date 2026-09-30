# 12 OAuth2作用域

## 学习目标

- 理解 OAuth2 scopes（作用域/细粒度权限）
- 掌握 `SecurityScopes` 与 `Security()` 的组合使用
- 学会在依赖链中逐层校验权限

## 核心概念

### 1. 作用域是什么

scopes 是 OAuth2 标准中的细粒度权限字符串，如 `"me"`、`"items"`、`"items:read"`。令牌中携带用户被授权的 scope 列表，端点声明所需 scope，请求时逐一校验。

### 2. 声明带 scopes 的令牌方案

```python
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "读取当前用户信息", "items": "读取物品列表"},
)
```

`scopes` 字典会自动显示在 Swagger UI 的 Authorize 弹窗中，用户可勾选。

### 3. 签发令牌时写入 scopes

```python
@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # ... 校验用户名密码 ...
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes}
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

`form_data.scopes` 是勾选的 scope 列表（真实项目要按用户角色过滤，不能照单全收）。

### 4. 依赖链中逐层校验

```python
from fastapi.security import SecurityScopes

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    # 解码 JWT，取出 token_scopes = payload.get("scopes", [])
    token_scopes = ...  # 从令牌中获得
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="权限不足",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    ...

@app.get("/items/")
async def read_items(
    current_user: Annotated[User, Security(get_current_user, scopes=["items"])],
):
    return [{"name": "Foo", "owner": current_user.username}]
```

关键点：

- 用 `Security()` 替代 `Depends()`，多一个 `scopes` 参数
- 依赖参数 `security_scopes: SecurityScopes` 会**自动聚合**整条依赖链上所有要求的 scope
- 子依赖要求的 scope 与当前端点要求的 scope 会被合并校验
- 未授权时返回带 `WWW-Authenticate: Bearer scope="items me"` 的 401，客户端能知道缺哪些 scope

### 5. 依赖树示意

```
/items/  需要 scopes=["items"]
  └── get_current_active_user 需要 scopes=["me"]（继承给下游）
        └── get_current_user 聚合校验 ["items", "me"]
```

## 最佳实践

1. **scope 命名层级化**：`items:read`、`items:write` 比单个 `items` 更可控
2. **签发端不信任客户端勾选**：按用户实际角色裁剪 scopes 再写入令牌
3. **统一在一个最底层依赖校验**：利用 `SecurityScopes` 聚合，避免每层重复写校验逻辑

## 常见问题

**Q: Security 和 Depends 的区别？**
A: `Security(dep, scopes=[...])` 是 `Depends(dep)` 的扩展版，仅多了 scopes 参数

**Q: scopes 与角色（RBAC）的关系？**
A: scope 是端点/能力级别的授权声明，角色是用户级分组；常见做法是 角色 → scopes 的映射表，签发令牌时转换

## 相关章节

- [11_高级安全.md](./11_高级安全.md) - 高级安全概览
- [33_带JWT的OAuth2.md](../02_教程-用户指南/33_带JWT的OAuth2.md) - JWT 认证基础
- [10_高级依赖注入.md](./10_高级依赖注入.md) - 高级依赖注入
