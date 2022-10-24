from TIERS import TIERS, TIER_CONVERTER


def get_table_header():
    table_header = '| 난이도 | 번호 | 문제 이름 |\n|:------:|:----:|:---------:|\n'
    return table_header


def get_table_row(problem_tier, problem_number, problem_name):
    table_row_svg = f'<img height="25px" width="25px" src="https://static.solved.ac/tier_small/{problem_tier}.svg"/>'
    table_row_number = f'[{problem_number}](https://www.acmicpc.net/problem/{problem_number})'
    table_row_name = f'[{problem_name}](https://www.acmicpc.net/problem/{problem_number})'
    table_row_form = f'| {table_row_svg} | {table_row_number} | {table_row_name} |\n'
    return table_row_form


def get_table_content(problems: dict, problems_names: dict) -> str or bool:
    table_content = ''
    for tier in TIERS:
        tier_name = TIER_CONVERTER[tier]
        if not (problems.get(tier_name) and problems_names.get(tier_name)):
            # error exception NEEDED
            return False
        table_row = get_table_row(tier, problems[tier_name], problems_names[tier_name])
        table_content += table_row
    return table_content


def get_problem_table(problems: dict, problems_names: dict) -> str:
    table_header = get_table_header()
    table_content = get_table_content(problems, problems_names)
    table = table_header + table_content
    return table
