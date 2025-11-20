from dotenv import load_dotenv

load_dotenv()

from rt_llama.capture import capture_loop


if __name__ == "__main__":
    capture_loop()
