# Transformers：预训练模型的统一接口。CPU 上用“随机初始化的微型 GPT-2”演示结构与生成流程
import torch, transformers
from transformers import GPT2Config, GPT2LMHeadModel
print("transformers", transformers.__version__)
torch.manual_seed(0)

# 1) 从配置构建一个微型模型（无需下载权重）
cfg = GPT2Config(vocab_size=1000, n_positions=64, n_embd=64, n_layer=2, n_head=4, bos_token_id=0, eos_token_id=0)
model = GPT2LMHeadModel(cfg).eval()
print(f"微型 GPT-2：{cfg.n_layer} 层、{cfg.n_head} 头、隐藏维度 {cfg.n_embd}，参数量 {model.num_parameters():,}")

# 2) 前向：输入 token id → 每个位置对词表的 logits
ids = torch.tensor([[11, 42, 7, 99]])
with torch.no_grad(): out = model(input_ids=ids, labels=ids)
print("logits 形状 (batch, 序列长度, 词表):", tuple(out.logits.shape))
print(f"随机模型的损失 {out.loss.item():.3f} ≈ ln(词表大小) = {torch.log(torch.tensor(1000.)).item():.3f}")

# 3) 生成：贪心解码 vs 采样
g = model.generate(ids, max_new_tokens=8, do_sample=False, pad_token_id=0)
s = model.generate(ids, max_new_tokens=8, do_sample=True, top_k=50, temperature=1.0, pad_token_id=0)
print("贪心生成的 token id:", g[0].tolist())
print("采样生成的 token id:", s[0].tolist())

# 4) 从 Hugging Face Hub 加载一个测试用的极小模型 + 分词器（需要网络）
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    name = "hf-internal-testing/tiny-random-gpt2"
    tok = AutoTokenizer.from_pretrained(name); lm = AutoModelForCausalLM.from_pretrained(name)
    enc = tok("Hello world, this is", return_tensors="pt")
    print("分词结果:", tok.convert_ids_to_tokens(enc.input_ids[0]))
    gen = lm.generate(**enc, max_new_tokens=5, do_sample=False, pad_token_id=tok.eos_token_id)
    print("Hub 微型模型生成(随机权重，输出无意义):", repr(tok.decode(gen[0][enc.input_ids.shape[1]:])))
except Exception as e:
    print("Hub 加载跳过:", type(e).__name__, str(e)[:120])
