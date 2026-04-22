#!/usr/bin/env python3
# music_assistant.py
# 基于 llama.cpp API 的音乐推荐 AI 助手

from openai import OpenAI
import json

class MusicAssistant:
    def __init__(self, llm_url="http://47.254.68.82:8080/v1"):
        self.client = OpenAI(base_url=llm_url, api_key="not-needed")
        # 模拟曲库（实际可对接 music-library 查询接口）
        self.library = [
            {"name": "夜曲", "artist": "周杰伦", "genre": "R&B", "mood": "night"},
            {"name": "稻香", "artist": "周杰伦", "genre": "民谣", "mood": "warm"},
            {"name": "七里香", "artist": "周杰伦", "genre": "流行", "mood": "spring"},
            {"name": "贝加尔湖畔", "artist": "李健", "genre": "民谣", "mood": "night"},
            {"name": "成都", "artist": "赵雷", "genre": "民谣", "mood": "night"},
            {"name": "平凡之路", "artist": "朴树", "genre": "摇滚", "mood": "reflective"},
            {"name": "那些年", "artist": "胡夏", "genre": "流行", "mood": "nostalgic"},
            {"name": "起风了", "artist": "买辣椒", "genre": "流行", "mood": "bittersweet"},
        ]

    def _format_library(self):
        lines = [f"- {s['artist']}《{s['name']》[{s['genre']}]" for s in self.library]
        return "\n".join(lines)

    def chat(self, user_input: str, system_hint: str = "") -> str:
        system_prompt = f"""你是一个音乐助手，可以根据用户的请求推荐歌曲。

音乐库现有歌曲：
{self._format_library()}

{system_hint}

当用户询问歌曲时，请根据曲库内容推荐。"""

        response = self.client.chat.completions.create(
            model="qwen2-7b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    assistant = MusicAssistant()

    questions = [
        "晚上一个人听，什么歌比较合适？",
        "推荐一些周杰伦的歌",
        "有没有适合心情不好的时候听的？",
    ]

    for q in questions:
        print(f"\n用户：{q}")
        print(f"AI：{assistant.chat(q)}")
