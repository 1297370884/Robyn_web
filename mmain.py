import os
from robyn import Request, Response, Robyn, status_codes, HttpMethod
from apps.market.api_routes import market_api_routes # 导入商城接口路由
from apps.users.api_routes import users_api_routes # 导入用户接口路由
from apps.users.views.view_routes import users_view_routes # 导入用户视图路由
from core.routes import view_routes # 导入总视图路由
from pathlib import Path
from settings import serve_static_files # configure_cors, 
# 创建 Robyn 实例
app = Robyn(__file__)


# 配置静态资源
serve_static_files(app)

# # 配置CORS
# configure_cors(app)

# 注册总视图路由
view_routes(app)

# 注册商城接口路由
market_api_routes(app)

# 注册用户接口路由
users_api_routes(app)

# 注册用户视图路由
users_view_routes(app)



if __name__ == "__main__":
    app.start(port=8080)
