import os
import json
import re

from sambanova import SambaNova


_client = None

def _get_sambanova_client():
    global _client
    if _client is None:
        _client = SambaNova(
            api_key=os.getenv("SAMBANOVA_API_KEY"),
            base_url="https://api.sambanova.ai/v1",
        )
    return _client


_prompt = """画像内に見えている人物がどのような作業を行っているか説明してください。
人物が写っていない場合、Noneを返してください。

## 説明する際の注意点
* 作業者は作業手順書を元に作業を行っています。
* 写っている作業者がどのような状態か、どのような作業をしているか説明してください。
* 作業手順書の各ステップで指差し確認を行う必要があるため、人差し指での指差し確認が認識できた場合、yoshi_checkをtrueにしてください。


## 出力形式
```json
{
    "description": "<人物の作業の説明 or None>",
    "yoshi_check": <true or false>
}
```

## ここから本場
出力は```json```で囲ってください。
出力:
"""


def image_response(image_base64: str) -> tuple[str, bool]:
    try:
        client = _get_sambanova_client()
        response = client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct",
            messages=[
                {
                    "role":"user",
                    "content":[
                        {
                            "type": "text",
                            "text": _prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        }
                    ]
                }
            ],
            temperature=0.1,
            top_p=0.1
        )
        content = response.choices[0].message.content
        content_dict = json.loads(re.search(r"```json(.*)```", content, re.DOTALL).group(1))
        return content_dict["description"], content_dict["yoshi_check"]
    except Exception as e:
        print(e)
        return None, False
