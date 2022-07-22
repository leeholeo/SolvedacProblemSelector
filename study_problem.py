import nicknames
import requests
import time


# 난이도 문제 목록 요청(solved.ac)
def tier_problem_request(tier_number: int, page_number=1) -> bool:
    api = f'https://solved.ac/api/v3/search/problem?query=solvable:true+tier:{tier_number}&page={page_number}&sort=solved&direction=desc'
    request_time = time.time()
    response = requests.get(api)
    response_time = time.time()
    print(f"{tier_number}_tier_request: {response_time-request_time:.2f}")
    if not (200 <= response.status_code < 300):
        return False
    response = response.json()
    return response


# 유저가 푼 문제 목록 요청(solved.ac)
def user_solved_problem_request(user_nickname: str, page_number=1) -> bool:
    api = f'https://solved.ac/api/v3/search/problem?query=solved_by:{user_nickname}&page={page_number}'
    request_time = time.time()
    response = requests.get(api)
    response_time = time.time()
    print(f"{user_nickname}_user_request: {response_time-request_time:.2f}")
    if not (200 <= response.status_code < 300):
        return  False
    response = response.json()
    return response


# 응답에 포함된 문제들을 dict에 넣기
def add_response_to_dict(response: dict, dic: dict) -> bool:
    if response is False:
        return False
    items = response["items"]
    for item in items:
            problem_id = item["problemId"]
            if dic.get(problem_id):
                dic[problem_id] += 1
            else:
                dic[problem_id] = 1
    return True


# 유저가 푼 문제들을 받아와서 넣기
def user_solved_problem(user_nickname: str, solved_problems: dict):
    errors = []
    if (initial_response := user_solved_problem_request(user_nickname)) is False:
        errors.append(0)
        return None, errors

    count = initial_response["count"]
    total_page = (count-1)//100 + 1
    add_response_to_dict(initial_response, solved_problems)
    for page_num in range(2, total_page+1):
        response = user_solved_problem_request(user_nickname, page_num)
        if add_response_to_dict(response, solved_problems) is False:
            errors.append(page_num)
    return total_page, errors


# 유저들이 푼 문제들을 받아와서 분류해 넣기
def total_user_solved_problem(user_nicknames: list):
    errors = {}
    pages = {}
    solved_problems = {}
    for user_nickname in user_nicknames:
        user_page, user_errors = user_solved_problem(user_nickname, solved_problems)
        pages[user_nickname] = user_page
        if user_page is not None:
            errors[user_nickname] = user_errors
    return solved_problems, pages, errors


# initial setting
initial_time = time.time()  # time check
S5, S4, S3, S2, S1 = range(6, 11)
G5, G4, G3, G2, G1 = range(11, 16)
TIERS = [S2, S1, G5, G4]
TIER_CONVERTER = {
    6: "S5",
    7: "S4",
    8: "S5",
    9: "S2",
    10: "S1",
    11: "G5",
    12: "G4",
    13: "G5",
    14: "G2",
    15: "G1"
}

# unsolved problems
solved_problems, pages, errors = total_user_solved_problem(nicknames.nicknames)
solved_problems_time = time.time()  # time check

# tier problems unsolved
problems = {}
problems_informations = {}
for tier in TIERS:
    page_num = 1
    recur_count = 0
    # find and ignore solved problems
    while (response := tier_problem_request(tier, page_num)):   # tier request
        # to prevent infinite loop
        if recur_count > 2:
            break
        items = response["items"]
        for item in items:
            problem_id = item["problemId"]
            accepted_user_count = item["acceptedUserCount"]
            average_tries = item["averageTries"]
            if (solve_count := solved_problems.get(problem_id)):
                # 1. 전체 중복 불허용
                continue
                # # 2. 실버는 특정 인원까지 중복 허용
                # if not (tier < G5 and solve_count < 2):
                #     continue
            # 푼 인원 수 제한
            if accepted_user_count < 500:
                continue
            # 평균 시도 횟수 제한
            if average_tries > 7:
                continue
            # if unsolved
            problems[TIER_CONVERTER[tier]] = problem_id
            problems_informations[TIER_CONVERTER[tier]] = {
                "푼 사람 수": accepted_user_count,
                "평균 시도": average_tries,
            }
            break
        # if find unsolved problem, break
        if problems.get(tier):
            break
        page_num += 1
        recur_count += 1
    # searched all pages, but cannot find unsolved problem
    else:
        problems[TIER_CONVERTER[tier]] = "all solved"
    # if request is false
    if response is False:
        problems[TIER_CONVERTER[tier]] = "error occured"
        errors[TIER_CONVERTER[tier]] = "Bad response"
tier_problems_time = time.time()    # time check

# print problems
print(problems) 
# print informations of problems
print(problems_informations)
# print errors if exist
for error_value in errors.values():
    if error_value:
        print(errors)
        break

# print time taken
total_time = time.time()
print(f"solved_problems_time: {solved_problems_time - initial_time:.2f}")
print(f"tier_problems_time: {tier_problems_time - solved_problems_time:.2f}")
print(f"total_time: {total_time - initial_time:.2f}")
