# 异常处理的五个好习惯
import json, logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("demo")

class ConfigError(Exception):
    """1) 自定义异常：让调用方能精确捕获"""

def read_port(cfg: dict) -> int:
    try:
        port = int(cfg["port"])               # 2) try 块尽量小
    except KeyError:
        raise ConfigError("缺少 port 配置") from None
    except (TypeError, ValueError) as e:      # 3) 捕获具体异常，而不是裸 except
        raise ConfigError(f"port 不是整数: {cfg['port']!r}") from e
    else:
        if not 0 < port < 65536:
            raise ConfigError(f"port 越界: {port}")
        return port
    finally:
        log.info("read_port 检查完毕")         # 4) finally 做清理/收尾

for cfg in [{"port": "8080"}, {}, {"port": "abc"}, {"port": 70000}]:
    try:
        print("端口 =", read_port(cfg))
    except ConfigError as e:
        log.warning("配置错误: %s", e)        # 5) 在合适的层级处理并记录

# Python 3.11+：ExceptionGroup 与 except*，处理"同时发生的多个错误"
try:
    raise ExceptionGroup("批量校验失败", [ValueError("A 字段为空"), TypeError("B 字段类型错")])
except* ValueError as eg:
    print("处理值错误:", [str(e) for e in eg.exceptions])
except* TypeError as eg:
    print("处理类型错误:", [str(e) for e in eg.exceptions])
