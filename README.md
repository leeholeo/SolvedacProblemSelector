# SolvedacProblemSelector
> 백준 알고리즘 스터디에서 사용한 알고리즘 문제 선정 프로그램
### 개요
- 스터디원의 백준 nickname, 원하는 수준의 문제 tier를 기반으로 스터디원이 풀지 않은 백준 문제를 자동으로 선정해주는 프로그램
- 토큰을 통해 선정한 문제를 github issue에 자동으로 올려준다.
  ![image](https://user-images.githubusercontent.com/87463874/197561713-970c8844-0ddd-43d7-ba35-7bd973490ee7.png)

### 사용 방법
- study_problem.py 실행
```
python study_problem.py
```

### 진행 예정
- 가이드 문서 작성
- refactoring
- gui화

### 사용 API 상세
- 등급별, 푼 사람이 많은 순서의 문제 목록
    - API: https://solved.ac/api/v3/search/problem
    - *example api(json).* `https://solved.ac/api/v3/search/problem?query=solvable:true+tier:<tier_number>&page=<page_number>&sort=solved&direction=desc`
    - rtn.
    ```json
    {
        "count": 685,
        "items": [{
    		}]
    }
    ```
- 아이디를 아는 경우 그 사람이 푼 문제의 목록
    - API: https://solved.ac/api/v3/search/problem
    - *example api(json).* `https://solved.ac/api/v3/search/problem?query=solved_by:<user_nickname>&page=<page_number>`
    - page는 100개마다 바뀐다.
    - rtn.
    ```json
    {
        "count": 270,
        "items": [{
    		}]
    }
    ```
