import argparse
import sys

from studybuddy.scraper import Scraper
from studybuddy.filewriter import FileWriter
from studybuddy.util import parse_file_to_list


class StudyBuddy:
    def __init__(self, dest_dir, selected_language="Python3"):
        self.dest_dir = dest_dir
        self.selected_language = selected_language
        self.language_file_extensions = {"Python3": ".py", "C++": ".cpp"}
        # , "Java": ".java", "C": ".c", "Javascript": ".js", "Typescript": ".ts" #possible todo include these languages
        self.code_file_extension = self.language_file_extensions[self.selected_language]
        self.time_limits = {"Easy": 20, "Medium": 30, "Hard": 40}
        self.scraper = Scraper(selected_language)
        self.file_writer = FileWriter(dest_dir, selected_language)

    def handle_single_question(self, question_url, log=True):
        code_file_name, difficulty, code_lines = self.scraper.get_url_data(question_url)
        self.file_writer.write_code_file(code_file_name, difficulty, question_url, code_lines, log)
        self.scraper.quit()

    def handle_questions_file(self, file_path, log=True):
        question_urls = parse_file_to_list(file_path)
        self.handle_multiple_questions(question_urls, log)

    def handle_multiple_questions(self, question_urls, log=True):
        for question_url in question_urls:
            code_file_name, difficulty, code_lines = self.scraper.get_url_data(question_url)
            self.file_writer.write_code_file(code_file_name, difficulty, question_url, code_lines, log)
        self.scraper.quit()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Optimize Leetcode study sessions by scraping provided URLs to local files with preconfigured "
                    "imports/includes and supporting build files. Generates a log header per file and a consolidated "
                    "log file in the destination directory.",
        epilog="For suggestions or bug reports, raise an issue at 'https://github.com/nellogan/studybuddy/issues'",
    )
    parser.add_argument("DESTINATION_DIR",
                        help="(Required) destination directory (will recursively create directories if they do not exist)")
    parser.add_argument("-l", "--language",
                        help="(Optional) specify language, only Python3 and C++ are supported. Defaults to Python3 if omitted")
    parser.add_argument("-n", "--no_log", action="store_false",
                        help="(Optional) turn off logging")

    # Create a mutually exclusive group for -q and -f
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-q", "--question", type=str,
                       help="(Required, mutually exclusive to -f) URL of question")
    group.add_argument("-f", "--questions_file", type=str,
                       help="(Required, mutually exclusive to -q) path to file that contains question urls that are newline separated")

    args = parser.parse_args()
    return args


def main():
    try:
        args = parse_arguments()
        if args.language:
            language = args.language
        else:
            language = "Python3"
        dest_dir = args.DESTINATION_DIR
    except SystemExit as e:
        sys.exit(e.code)

    print(f"Destination Directory: {dest_dir}")
    print(f"Language selected: {language}")
    studybuddy = StudyBuddy(dest_dir, language)
    logging = args.no_log
    if args.question:
        print(f"Mode: question, URL: {args.question}")
        studybuddy.handle_single_question(args.question, logging)
    elif args.questions_file:
        print(f"Mode: question_file, path to questions url file: {args.questions_file}")
        studybuddy.handle_questions_file(args.questions_file, logging)
    else:
        raise ValueError("Error: Either -q or -f must be passed.")

if __name__ == "__main__":
    main()
