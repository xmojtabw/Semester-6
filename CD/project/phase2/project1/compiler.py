#!/usr/bin/env python3
"""Main compiler script that coordinates the scanning and parsing process."""
import sys
from pathlib import Path
from scanner import Scanner
from parser import Parser

def main():
    # Initialize components
    scanner = Scanner()
    parser = Parser()
    
    try:
        # Read input file
        input_file = "input.txt"
        if len(sys.argv) > 1:
            input_file = sys.argv[1]
        
        # Process input through scanner
        with open(input_file, 'r') as f:
            input_text = f.read()
        scanner.set_input(input_text)
        scanner.process_input()
        scanner.write_output_files()
        
        # Process tokens through parser
        parser.load_input(input_file)
        parse_tree = parser.parse()
        parser.write_output_files(parse_tree)
        
        print("Compilation completed successfully.")
        print("Output files generated:")
        print("- tokens.txt")
        print("- lexical_errors.txt")
        print("- symbol_table.txt")
        print("- parse_tree.txt")
        print("- syntax_errors.txt")
        
    except Exception as e:
        print(f"Error during compilation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()