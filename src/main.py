from modules.cowsay_demo.greeting import greet_to, greet_from_env


def main():
    # use argument to greet
    greet_to(your_name="Alan")

    # use environment variable to greet
    greet_from_env()


if __name__ == "__main__":
    main()
