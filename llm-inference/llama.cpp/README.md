# llama.cpp LLM 推理优化 — 文章配套 Demo

## 目录结构

```
llama.cpp/
  music_assistant.py    # 音乐推荐 AI 助手（接入 llama.cpp API）
  quantize_example.sh   # 模型量化示例脚本
  server_start.sh       # llama-server 启动脚本
```

## 服务器部署步骤

### 1. 安装 llama.cpp

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
mkdir build && cd build
cmake .. -DLLAMA_CUBLAS=ON   # 有 GPU 时
cmake .. -DLLAMA_METAL=ON    # Mac M 系列
make -j$(nproc)
```

### 2. 下载并量化模型

```bash
# 下载 HuggingFace GGUF 模型（已有量化版本，无需自己量化）
huggingface-cli download Qwen/Qwen2-7B-Instruct-GGUF \
    --include "qwen2-7b-instruct-q4_k_m.gguf" \
    --local-dir ./models/qwen2-7b/

# 如果需要自己量化（已有 FP16 模型）：
./llama-quantize models/model-f16.gguf models/model-q4_k_m.gguf Q4_K_M
```

### 3. 启动 API 服务

```bash
./llama-server \
    -m ./models/qwen2-7b/qwen2-7b-instruct-q4_k_m.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    -t 12 \
    --ctx-size 4096 \
    --parallel 32 \
    2>&1 | tee server.log
```

### 4. 测试 API

```bash
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "qwen2-7b",
        "messages": [{"role": "user", "content": "你好"}],
        "max_tokens": 128
    }'
```

## 性能参考

| 模型 | 量化 | 硬件 | 首 token 延迟 | 生成速度 |
|------|------|------|------------|---------|
| Qwen2-7B | Q4_K_M | 16核 CPU | ~0.8-1.5s | 15-18 tok/s |
| Qwen2-7B | Q4_K_M | RTX 4090 (24G) | ~0.2-0.5s | 60-80 tok/s |
| Mistral-7B | Q5_K_M | 16核 CPU | ~1-2s | 10-15 tok/s |
| Llama2-13B | Q4_K_M | 16核 CPU | ~2-4s | 6-10 tok/s |

## 量化格式选择建议

- **Q4_K_M**：性价比最高，4bit 里精度最好的方案（首选）
- **Q5_K_M**：精度更高一点，体积大 1/3，适合代码生成
- **Q6_K**：接近 FP16 精度，体积约为 FP16 的 60%，有条件优先用这个
- **不要用 Q3_K 及以下**：数学/推理任务精度损失明显

## 常见问题

**Q: 内存不足 OOM？**
→ 减小 `--parallel`（并发数）和 `--ctx-size`（上下文长度）

**Q: 生成速度太慢？**
→ 增加 CPU 线程（`-t`），确保设置为 CPU 核心数的 75%

**Q: CUDA 版本不兼容？**
→ 重新编译：`cmake .. -DLLAMA_CUBLAS=ON`
