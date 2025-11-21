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