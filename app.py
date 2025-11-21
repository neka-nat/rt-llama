import argparse

from dotenv import load_dotenv

load_dotenv()

from rt_llama.capture import capture_loop


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera_index", type=int, default=0)
    args = parser.parse_args()
    capture_loop(args.camera_index)
