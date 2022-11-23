# 1. 텍스트 파일에 입력된 정보를 리스트들에 저장---------------------------------------------------------------------------------------

pageNum = []
pageFrameNum = []
windowSize = []
RefStringLen = []
RefString = []
def add_values():  # 텍스트 파일의 정보를 리스트들에 입력하는 함수
    global pageNum
    global pageFrameNum
    global windowSize
    global RefStringLen
    global RefString
    open("input.txt", "r", encoding="UTF-8")
    with open("input.txt") as f:
        data = f.read().splitlines()
    numbers = []
    for i in data: #띄어쓰기를 기준으로 데이터 분리
        numbers.extend((i.split()))
    for i in range(0, len(numbers)): #문자열 데이터를 정수형으로 변환
        numbers[i] = int(numbers[i])
    pageNum = numbers.pop(0) #프로세스 페이지 개수 가져오기
    pageFrameNum = numbers.pop(0) #page Frame 개수 가져오기
    windowSize = numbers.pop(0)  # window Size 가져오기
    RefStringLen = numbers.pop(0)  # page reference string 길이 가져오기
    RefString = numbers #page reference string


add_values()


# 2. MIN algorithm---------------------------------------------------------------------------------------
#총 page fault 횟수
#메모리 상태 변화 과정 (page fault 발생 위치 표시)

#1. page Frame number만큼 page fault 발생시키고 page fault 발생 표시
#2. 처리된 page는 referene string list에서 삭제
#3. for loop으로 나머지 reference string list를 확인하고 n+=1 을 통해 메모리에 있는 페이지 숫자가 몇번째에 나오는 지확인.
#4. forward distance 리스트의 max 숫자를 메모리에서 삭제시키고 fault 표시. 다음 page가 메모리로 들어온다. reference string에서 pop, 메모리에는 .remove이후 pop된 숫자 append
#5. 3,4번이 while loop으로 돌며 if 문을 넣어야 한다. if 첫번째 숫자가(참조되는 숫자) 메모리안에 있으면 pass.
#6 전체적으로 하나하나 처리되는 loop을 만들어야한다!!

# 3. LRU algorithm---------------------------------------------------------------------------------------






print("pageNum: %s" %pageNum)
print("pageFrameNum: %s" %pageFrameNum)
print("windowSize: %s" %windowSize)
print("refStringLen: %s" %RefStringLen)