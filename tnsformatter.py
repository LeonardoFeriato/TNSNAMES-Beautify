#!/usr/bin/env python3
# Original Code: https://www.ludovicocaldara.net/dba/tidy_dotora/
import sys
import re
import os

GREEN = "\033[92m"
RESET = "\033[0m"
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def pad(string, length, char):
    """Pad a string with a given char until reaching length."""
    return string + (char * (length - len(string)))

def formatter(input_stream):
    level = 1
    first = True
    lastcomment = False
    wentdown = False
    output_lines = []

    for line in input_stream:
        # Preserve comments
        if re.match(r"^[\s]*#", line):
            if not lastcomment:
                #sys.stdout.write("\n")
                output_lines.append("\n")
            #sys.stdout.write(line.rstrip("\n") + "\n")
            output_lines.append(line.rstrip("\n") + "\n")
            lastcomment = True
            continue
        lastcomment = False

        # Tokenize by inserting backticks before splitting
        line = re.sub(r"=", "`=", line)
        line = re.sub(r"\(", "`(", line)
        line = re.sub(r"\)", "`)", line)
        tokens = line.split("`")

        i = 0
        while i < len(tokens):
            # To remove only spaces and tabs (not newlines)
            token = re.sub(r"[ \t]+", "", tokens[i])
            if not token:
                i += 1
                continue

            # Open bracket
            if re.match(r"^\(", token):
                level += 1
                if not output_lines[-1].endswith("\n"):
                    #sys.stdout.write("\n")
                    output_lines.append("\n")
                #sys.stdout.write(pad("", 2 * level - 1, " "))
                output_lines.append(pad("", 2 * level - 1, " "))

            # Close bracket
            if re.match(r"^\)", token):
                level -= 1
                if wentdown:
                    if not output_lines[-1].endswith("\n"):
                        #sys.stdout.write("\n")
                        output_lines.append("\n")
                    #sys.stdout.write(pad("", 2 * level + 1, " "))
                    output_lines.append(pad("", 2 * level + 1, " "))
                wentdown = True
            else:
                wentdown = False

            # Top level entries
            if level == 1 and i == 0 and re.match(r"[A-Za-z]", token):
                if first:
                    first = False
                else:
                    #sys.stdout.write("\n\n")
                    output_lines.append("\n\n")

            #sys.stdout.write(token)
            output_lines.append(token)
            i += 1

    # Final newline
    #sys.stdout.write("\n")
    output_lines.append("\n")
    return "".join(output_lines)     # Convert list to a single string

if __name__ == "__main__":
    result = formatter(sys.stdin)

    # Remove excessive blank lines (3 or more -> 2)
    result = re.sub(r"\n{3,}", "\n\n", result)

    # Save to file in same folder
    output_file = os.path.join(os.getcwd(), "tnsnames.ora")
    with open(output_file, "w", encoding="utf-8", errors="replace") as f:
        f.write(result + "\n")
    
    sys.stdout.write(GREEN + "\nDone!\n" + RESET)
