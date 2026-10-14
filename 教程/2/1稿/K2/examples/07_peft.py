# PEFT：参数高效微调。给微型 GPT-2 加 LoRA，只训练约 2% 的参数
import torch, peft
from transformers import GPT2Config, GPT2LMHeadModel
from peft import LoraConfig, get_peft_model, TaskType
print("peft", peft.__version__)
torch.manual_seed(0)

base = GPT2LMHeadModel(GPT2Config(vocab_size=1000, n_positions=64, n_embd=128, n_layer=4, n_head=4, bos_token_id=0, eos_token_id=0))
cfg = LoraConfig(task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=16, lora_dropout=0.0, target_modules=["c_attn"], fan_in_fan_out=True)
model = get_peft_model(base, cfg)
model.print_trainable_parameters()

# LoRA 结构：W x + (B A) x * alpha/r，B 初始化为 0 → 训练开始时与原模型完全一致
layer = model.base_model.model.transformer.h[0].attn.c_attn
print("LoRA A 形状", tuple(layer.lora_A["default"].weight.shape), "| B 形状", tuple(layer.lora_B["default"].weight.shape),
      "| B 全零:", bool((layer.lora_B["default"].weight == 0).all()))

# 让模型记住一个固定序列：只更新 LoRA 参数
seq = torch.tensor([[5, 17, 42, 8, 99, 3, 64, 21]])
frozen_before = base.transformer.wte.weight.clone()
opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=5e-3)
for step in range(1, 101):
    loss = model(input_ids=seq, labels=seq).loss
    opt.zero_grad(); loss.backward(); opt.step()
    if step in (1, 50, 100): print(f"step {step:>3} loss {loss.item():.4f}")
print("冻结的嵌入层未被修改:", torch.equal(frozen_before, base.transformer.wte.weight))

# 只保存适配器（体积很小），可合并回基座
import tempfile, os
d = tempfile.mkdtemp(); model.save_pretrained(d)
size = sum(os.path.getsize(os.path.join(d, f)) for f in os.listdir(d))
print("保存的文件:", sorted(os.listdir(d)), f"共 {size/1024:.0f} KB")
model.eval()
with torch.no_grad(): before = model(seq).logits
merged = model.merge_and_unload()
with torch.no_grad(): after = merged(seq).logits
print("合并进基座后输出一致:", torch.allclose(before, after, atol=1e-5), "| 合并后类型:", type(merged).__name__)
