from groq import Groq

_client = None

def _get_groq_client():
    global _client
    if _client is None:
        _client = Groq()
    return _client



def image_response(image_base64: str) -> str:
    client = _get_groq_client() 
    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "見えているものを説明してください。"
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
    return response.choices[0].message.content
