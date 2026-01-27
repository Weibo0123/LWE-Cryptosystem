import random

def main():
    rng = random.Random(12345)
    print("ok", rng.randrange(1000))

if __name__ == "__main__":
    main()