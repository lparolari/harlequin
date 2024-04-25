import argparse

from harlequin.hello import greet

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, default="John")
    args = parser.parse_args()

    print(f"Hello, {greet(args.name)}!")
