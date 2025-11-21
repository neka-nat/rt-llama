# RT-llama

SambanNovaを使ってリアルタイムにllama4を動かすコードです。

```bash
uv sync
cp .env.example .env
# .envにAPIキーを設定
# デフォルトのカメラのインデックスは0
uv run python app.py
# カメラのインデックスを指定して実行
uv run python app.py --camera_index 4
```

https://github.com/user-attachments/assets/1471804a-978b-4f71-af67-b844d9de8130
