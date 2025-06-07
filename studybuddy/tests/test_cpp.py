import unittest
import os
import shutil

from studybuddy.studybuddy import StudyBuddy
from studybuddy.util import file_name_from_url, parse_file_to_list


class TestQuestionPython(unittest.TestCase):

    def test_single_question(self):
        this_file_path = os.path.dirname(os.path.abspath(__file__))

        question_url_file = f"{this_file_path}/question.txt"
        question_url = parse_file_to_list(question_url_file)[0]
        file_name = file_name_from_url(question_url)

        dest_dir = f"{this_file_path}/tmp"
        language = "C++"
        studybuddy = StudyBuddy(dest_dir, language)
        studybuddy.handle_single_question(question_url)

        # Parse result and save as list
        result_file = f"{this_file_path}/tmp/{file_name}/{file_name}.cpp"
        result_lines = parse_file_to_list(result_file)

        # Parse solution and save as list
        solution_file = f"{this_file_path}/cpp_solutions/{file_name}.cpp"
        solution_lines = parse_file_to_list(solution_file)

        # Compare result with known solution
        self.assertEqual(result_lines, solution_lines,
                         "Error: test_single_question, result_lines and solution_lines were not identical")

        # Clean up the dest_dir directory
        shutil.rmtree(dest_dir)

    def test_questions_file(self):
        this_file_path = os.path.dirname(os.path.abspath(__file__))

        question_urls_file = f"{this_file_path}/question_urls.txt"
        dest_dir = f"{this_file_path}/tmp"
        language = "C++"
        studybuddy = StudyBuddy(dest_dir, language)
        studybuddy.handle_questions_file(question_urls_file, log=False)

        # Loop through all items in dest_dir
        for name in os.listdir(dest_dir):
            # Parse result and save as list
            result_file = f"{this_file_path}/tmp/{name}/{name}.cpp"
            result_lines = parse_file_to_list(result_file)

            # Parse solution and save as list
            solution_file = f"{this_file_path}/cpp_solutions/{name}.cpp"
            solution_lines = parse_file_to_list(solution_file)

            # Compare result with known solution
            self.assertEqual(result_lines, solution_lines,
                             "Error: test_questions_file, result_lines and solution_lines were not identical")

        # Clean up the dest_dir directory
        shutil.rmtree(dest_dir)

if __name__ == "__main__":
    unittest.main()
