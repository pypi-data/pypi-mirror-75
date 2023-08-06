import os
import sys
import json
from robot.api import ExecutionResult, ResultVisitor
from robot.model import TestCase, TestSuite
import hashlib


class KeywordCall:

    def __init__(self, parent_hash: str):
        self.call_count: int = 1
        self.parents = {parent_hash}

    def add(self, parent_hash: str):
        self.call_count += 1
        self.parents.add(parent_hash)

    def to_dict(self):
        return {"call_count": self.call_count, "parent_count": len(self.parents)}


KEYWORD_CALLS = dict()


class ResultAnalyzer(ResultVisitor):

    def start_keyword(self, keyword):
        if keyword.libname == 'SeleniumLibrary':

            # next we are hashing the names of the calling keywords, test cases or test suites
            # because we never want to store your names even temporarily!
            # the hashes just allows us to count the different calling parents.
            # We even do not store the entire hash, but just 16 bytes.
            # it will never be possible to get the names back
            if isinstance(keyword.parent, (TestCase, TestSuite)):
                parent_hash = hashlib.sha3_512(
                    keyword.parent.longname.encode("UTF-8")
                ).hexdigest()[16:32]
            else:
                parent_hash = hashlib.sha3_512(
                    str(keyword.parent.source + keyword.parent.name).encode("UTF-8")
                ).hexdigest()[16:32]
            kw_name = keyword.name[16:]
            if kw_name not in KEYWORD_CALLS:
                KEYWORD_CALLS[kw_name] = KeywordCall(parent_hash)
            else:
                KEYWORD_CALLS[kw_name].add(parent_hash)

    def end_total_statistics(self, stats):
        kw_calls = dict()
        for key in sorted(KEYWORD_CALLS.keys()):
            kw_calls[key] = KEYWORD_CALLS[key].to_dict()
        self.print_stats(kw_calls)
        json_stats = json.dumps(kw_calls, indent=2)
        with open(f'keyword_stats.json', 'w') as keyword_stats_file:
            keyword_stats_file.write(json_stats)
        print(f'\nStatistics File: {os.path.abspath("keyword_stats.json")}')
        print('Please upload the file to https://data.keyword-driven.de/index.php/s/SeleniumStats for full anonymity.')
        print('IP-Addresses or other personal data are not logged when uploading the file!')
        print('You can also mail it to mailto:rene@robotframework.org.\n')
        print('Thanks you very much for your support!')
        print('Your Browser-Team (Mikko, Tatu, Kerkko, Janne and René)')


    def print_stats(self, kw_calls):
        longest_keyword = 0
        for kw_name in kw_calls:
            current_length = len(kw_name)
            longest_keyword = current_length \
                if current_length > longest_keyword \
                else longest_keyword
        print(f'+-{"".ljust(longest_keyword, "-")       }-+-------+---------+')
        print(f'| {"Keyword".ljust(longest_keyword, " ")} | count | parents |')
        print(f'+-{"".ljust(longest_keyword, "-")       }-+-------+---------+')
        for kw_name in kw_calls:
            print(f'| {kw_name.ljust(longest_keyword , " ")} |'
                  f' {str(kw_calls[kw_name]["call_count"]).ljust(5," ")} |'
                  f' {str(kw_calls[kw_name]["parent_count"]).ljust(7, " ")} |')
        print(f'+-{"".ljust(longest_keyword, "-")}-+-------+---------+')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        original_output_xml = sys.argv[1]
        if not os.path.isfile(original_output_xml):
            raise FileNotFoundError(f'{original_output_xml} is no file')
        print(f'reading results from: {os.path.abspath(original_output_xml)}')
        ExecutionResult(original_output_xml).visit(ResultAnalyzer())
    else:
        print('Use the path to a output.xml as first arguemnt.  Example:  python -m SeleniumStats ../output.xml')