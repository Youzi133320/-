# 日志：分级、结构化、带上下文；与 print 的区别
import logging, json, io, sys

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {"level": record.levelname, "logger": record.name, "msg": record.getMessage()}
        if hasattr(record, "request_id"):
            payload["request_id"] = record.request_id
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info).splitlines()[-1]
        return json.dumps(payload, ensure_ascii=False)

logger = logging.getLogger("app.llm")
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler(sys.stdout)          # 人看的：文本格式，INFO 以上
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(levelname)-7s %(name)s: %(message)s"))
buffer = io.StringIO()
machine = logging.StreamHandler(buffer)              # 机器看的：JSON，DEBUG 以上
machine.setFormatter(JsonFormatter())
logger.addHandler(console); logger.addHandler(machine)

logger.debug("请求体大小=%d tokens", 1234)            # 只进 JSON
logger.info("调用模型", extra={"request_id": "req-7"})
logger.warning("接近速率限制: 剩余 %d 次", 3)
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("计算失败", extra={"request_id": "req-8"})

print("---- JSON 日志（可被 ELK/Loki 等系统检索）----")
print(buffer.getvalue().strip())

# 安全：日志里不要出现密钥
api_key = "sk-abcdef1234567890"
logger.info("使用 key=%s", api_key[:5] + "***")
