from functions.run_python_file import run_python_file


def test():
    result = run_python_file("calculator", "main.py")
    print("Result 1:")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result 2:")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("Result 3:")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("Result 4:")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py")
    print("Result 5:")
    print(result)
    print("")

    result = run_python_file("calculator", "lorem.txt")
    print("Result 6:")
    print(result)
    print("")


if __name__ == "__main__":
    test()