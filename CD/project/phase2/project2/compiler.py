from parser import Parser
from utils import write_output_files, getfile 
from preprocess import preprocess, process_invalid
# name: Mojtaba Mollaei
# stdnum: 40131383
# resources: Chatgpt, Copilot, Slides and Compilers, principles, techniques and tools by Aho, Sethi and Ullman


def main():

    # Read input file
    code = getfile("./Test Cases/T03/input.txt")

    # Preprocess the code
    code = preprocess(code)
    errors, code = process_invalid(code)

    # Create parser and parse the code
    parser = Parser(code)
    write_output_files(parser.tree, parser.syntax_errors)
    print("Parsing successful")


if __name__ == "__main__":
    main()
