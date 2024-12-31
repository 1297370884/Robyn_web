import os
from pathlib import Path
from robyn.templating import JinjaTemplate
from robyn import Robyn, ALLOW_CORS

"""
配置环境

"""
# 获取当前文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # 项目根目录
# BASE_DIR = Path(__file__).resolve().parent.parent

def serve_static_files(app):
    """
    配置静态资源在哪个目录
    """
    # 配置静态文件目录服务
    app.serve_directory(
        route="/static",  # 访问路由前缀
        directory_path=os.path.join(BASE_DIR, "static"),  # 静态文件目录的绝对路径
        index_file=None  # 不需要指定索引文件
    )



# 创建模板实例
template = JinjaTemplate(directory=os.path.join(BASE_DIR, "templates"))

def render_template(template_name, **kwargs):
    """
    全局配置render_template
    """
    return template.render_template(template_name, **kwargs)


# def configure_cors(app):
#     """
#     配置CORS
#     """
#     ALLOW_CORS(app, origins=[
#         "http://localhost:8080",  # 后端服务器
#         "http://127.0.0.1:8080"
#     ])

