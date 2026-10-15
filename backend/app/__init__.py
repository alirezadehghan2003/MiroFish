"""
MiroFish Backend - Flask应用工厂
"""

import json
import os
import warnings

# 抑制 multiprocessing resource_tracker 的警告（来自第三方库如 transformers）
# 需要在所有其他导入之前设置
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, jsonify, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger
from .utils.security import find_unsafe_id, is_host_allowed


def create_app(config_class=Config):
    """Flask应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 设置JSON编码：确保中文直接显示（而不是 \uXXXX 格式）
    # Flask >= 2.3 使用 app.json.ensure_ascii，旧版本使用 JSON_AS_ASCII 配置
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False
    
    # 设置日志
    logger = setup_logger('mirofish')
    
    # 只在 reloader 子进程中打印启动信息（避免 debug 模式下打印两次）
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process
    
    if should_log_startup:
        logger.info("=" * 50)
        logger.info("MiroFish Backend 启动中...")
        logger.info("=" * 50)
    
    # 启用CORS（仅允许配置的前端来源）
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ALLOWED_ORIGINS']}})
    
    # 注册模拟进程清理函数（确保服务器关闭时终止所有模拟进程）
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("已注册模拟进程清理函数")
    
    # 请求日志中间件
    @app.before_request
    def log_request():
        logger = get_logger('mirofish.request')
        logger.debug(f"请求: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"请求体: {request.get_json(silent=True)}")
    
    # 安全检查：拒绝非本机 Host（防 DNS rebinding）和可能逃逸目录的 ID
    @app.before_request
    def enforce_request_safety():
        if not is_host_allowed(request.host, app.config['ALLOWED_HOSTS']):
            return jsonify({"success": False, "error": "Host not allowed"}), 403

        sources = [request.view_args, request.args]
        if request.is_json:
            sources.append(request.get_json(silent=True))
        for values in sources:
            field = find_unsafe_id(values)
            if field:
                return jsonify({"success": False, "error": f"Invalid {field}"}), 400
        return None

    @app.after_request
    def log_response(response):
        logger = get_logger('mirofish.request')
        logger.debug(f"响应: {response.status_code}")
        return response

    # 非调试模式下不向客户端返回内部堆栈信息
    @app.after_request
    def strip_tracebacks(response):
        if (
            app.config.get('DEBUG')
            or response.direct_passthrough
            or response.is_streamed
            or not response.is_json
        ):
            return response
        payload = response.get_json(silent=True)
        if isinstance(payload, dict) and 'traceback' in payload:
            payload.pop('traceback')
            response.set_data(json.dumps(payload, ensure_ascii=False))
        return response
    
    # 注册蓝图
    from .api import graph_bp, simulation_bp, report_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    
    # 健康检查
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'MiroFish Backend'}
    
    if should_log_startup:
        logger.info("MiroFish Backend 启动完成")
    
    return app

