import sys


def main():
    try:
        from core.main import initialise
    except ImportError as exc:
        raise ImportError(
            "Couldn't initialise DMXControl. Make sure that it is installed by running pip install -r requirements.txt"
        ) from exc
    initialise(sys.argv)


if __name__ == '__main__':
    main()
