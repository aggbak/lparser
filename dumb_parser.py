def main():
    operators = ["+","-","*","/"]
    input_str = "2 + 3 = 5"
    op_stack = []
    output = []

    for char in input_str.split(" "):
        if char in operators:
            op_stack.append(char)
        elif 

if __name__ == "__main__":
    main()