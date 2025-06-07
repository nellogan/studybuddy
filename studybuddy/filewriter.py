import os


def write_makefile(question_dir):
    makefile_lines = [f"_DIR_DUMMY := $(shell mkdir -p ./bin)\n",
                      f"SRC = .\n"
                      f"BIN = ./bin\n"
                      f"OPT = -O0\n\n"
                      f"C_SRCS = $(wildcard $(SRC)/*.c)\n"
                      f"C_BINS = $(C_SRCS:$(SRC)/%.c=%)\n\n"
                      f"CPP_SRCS = $(wildcard $(SRC)/*.cpp)\n"
                      f"CPP_BINS = $(CPP_SRCS:$(SRC)/%.cpp=%)\n\n"
                      f"FLAGS = $(OPT) -Wall -Werror -Werror\n\n"
                      f".PHONY: all clean run\n\n"
                      f"all: $(CPP_BINS) $(C_BINS) run\n\n",
                      "run:\n",
                      "\t@EXEC_FILE=$$(ls ${BIN} | head -n 1); \\\n"
                      "\tEXEC_FILE_PATH=${BIN}/$$EXEC_FILE; \\\n"
                      "\tif [ -n \"$$EXEC_FILE\" ]; then \\\n",
                      "\t\techo \"Running first file: $$EXEC_FILE_PATH\"; \\\n"
                      "\t\t$$EXEC_FILE_PATH; \\\n",
                      "\telse \\\n",
                      "\t\techo \"No files found in $(BIN)\"; \\\n",
                      "\tfi\n\n",
                      "%: $(SRC)/%.c\n",
                      "\t$(CC) $(FLAGS) $< -o $(BIN)/$@\n\n",
                      "%: $(SRC)/%.cpp\n",
                      "\t$(CXX) $(FLAGS) $< -o $(BIN)/$@\n\n",
                      "clean:\n",
                      "\t-rm -f $(BIN)/*"]

    with open(f"{question_dir}/makefile", 'w') as f:
        f.writelines(makefile_lines)


def write_cpp_file(header, question_dir, code_file_name, code_lines):
    with open(f"{question_dir}/{code_file_name}.cpp", 'w') as f:
        imports = ["#include <iostream>\n",
                   "#include <vector>\n",
                   "#include <string>\n",
                   "#include <unordered_map>\n",
                   "#include <algorithm>\n",
                   "#include <utility>\n\n"]
        main = ["\nint main(int argc, char *argv[])\n",
                "{\n",
                "    \n",
                "    \n",
                "    Solution sln{};\n",
                "    /**\n",
                "    auto test = sln.method(arg);\n",
                "    std::cout << test << std::endl;\n",
                "    */\n",
                "    \n",
                "    return 0;\n",
                "}\n"]
        content = header + imports + code_lines + main

        f.writelines(content)

# possible todo write C file
# possible todo write Java file
# possible todo write Javascript file
# possible todo write Typescript file

def write_python_file(header, question_dir, code_file_name, code_lines):
    with open(f"{question_dir}/{code_file_name}.py", 'w') as f:
        imports = ["from typing import *\n",
                   "from collections import defaultdict\n",
                   "from collections import deque\n",
                   "from heapq import heappush, heappop, heapify\n",
                   "from queue import PriorityQueue\n",
                   "from math import inf, sqrt, gcd\n\n"
                  ]

        commented_out_test = ["# arg = None\n",
                              "# test = Solution().method(arg)\n",
                              "# print(f\"test {test}\")\n"]

        content = header + imports + code_lines + commented_out_test

        f.writelines(content)


class FileWriter:
    def __init__(self, dest_dir, selected_language="Python3"):
        self.dest_dir = dest_dir
        self.selected_language = selected_language
        self.language_file_extensions = {"Python3": ".py", "C++": ".cpp"}
        self.code_file_extension = self.language_file_extensions[self.selected_language]
        self.time_limits = {"Easy": 20, "Medium": 30, "Hard": 40}

        # Create dest_dir if not already created
        os.makedirs(dest_dir, exist_ok=True)

    def generate_header(self, code_file_name, url, difficulty):
        comment_prefix = "#" if self.selected_language == "Python3" else "//"
        info = [f"{comment_prefix}File: {code_file_name}{self.code_file_extension}\n",
                f"{comment_prefix}Question URL: {url}\n",
                f"{comment_prefix}Solution URL:\n",
                f"{comment_prefix}Difficulty: {difficulty}\n",
                f"{comment_prefix}Estimated Time: {self.time_limits[difficulty]} minutes\n"
                f"{comment_prefix}Start Time: \n",
                f"{comment_prefix}End Time: \n",
                f"{comment_prefix}Time Taken: \n",
                f"{comment_prefix}Passed: \n",
                f"{comment_prefix}NOTE: \n",
                "\n\n"]
        return info

    def generate_log_entry(self, code_file_name, url, difficulty):
        log_entry = [f"File: {code_file_name}{self.code_file_extension}\n",
                     f"URL:  {url}\n",
                     f"Difficulty: {difficulty}\n",
                     f"Estimated Time: {self.time_limits[difficulty]} minutes\n,"
                      "Start Time: \n",
                      "End Time: \n",
                      "Time Taken: \n",
                      "Passed: \n",
                      "NOTE: \n",
                      "\n"]
        return log_entry

    def write_code_file(self, code_file_name, difficulty, question_url, code_lines, log=True):
        # Create directory for each question:
        question_dir = f"{self.dest_dir}/{code_file_name}"
        os.makedirs(question_dir, exist_ok=True)

        header = self.generate_header(code_file_name, question_url, difficulty)
        if self.selected_language == "Python3":
            write_python_file(header, question_dir, code_file_name, code_lines)
        elif self.selected_language == "C++":
            write_cpp_file(header, question_dir, code_file_name, code_lines)
            write_makefile(question_dir)
        else:
            print(f"Unsupported language {self.selected_language}, cannot write_code_file(), exiting...")

        # Append header to log
        if log:
            with open(f"{self.dest_dir}/log.txt", 'a') as f:
                f.writelines(header)

        print(f"Finished writing: {self.dest_dir}/{code_file_name}{self.code_file_extension}")