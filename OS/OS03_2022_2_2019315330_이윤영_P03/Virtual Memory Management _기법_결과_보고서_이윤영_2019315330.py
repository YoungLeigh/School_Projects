# 1. 텍스트 파일에 입력된 정보를 리스트들에 저장---------------------------------------------------------------------------------------

pageNum = []
pageFrameNum = []
windowSize = []
refStringLen = []
refString = []
def add_values():  # 텍스트 파일의 정보를 리스트들에 입력하는 함수
    global pageNum
    global pageFrameNum
    global windowSize
    global refStringLen
    global refString
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
    refStringLen = numbers.pop(0)  # page reference string 길이 가져오기
    refString = numbers #page reference string
    print(refString)


add_values()

# 2. MIN algorithm---------------------------------------------------------------------------------------

#총 page fault 횟수
#메모리 상태 변화 과정 (page fault 발생 위치 표시)

#1. page Frame number만큼 page fault 발생시키고 page fault 발생 표시, page fault
#2. 처리된 page는 referene string list에서 삭제
#3. for loop으로 나머지 reference string list를 확인하고 n+=1 을 통해 메모리에 있는 페이지 숫자가 몇번째에 나오는 지확인.
#4. forward distance 리스트의 max 숫자를 메모리에서 삭제시키고 fault 표시. 다음 page가 메모리로 들어온다. reference string에서 pop, 메모리에는 .remove이후 pop된 숫자 append
#5. forward distance가 동일한 경우에는 tie-breaking rule을 메모리에 첫번째로 들어온 page가 victim이 되는 것으로 설정한다.
#5. 3,4번이 while loop으로 돌며 if 문을 넣어야 한다. if 첫번째 숫자가(참조되는 숫자) 메모리안에 있으면 pass.
#6 전체적으로 하나하나 처리되는 loop을 만들어야한다!!


def minAlgorithm():
    pageFault = []
    pageFaultIndex = [] #몇번째 page에서 fault가 발생했는지 확인
    memory = []
    forwardDistance = [] #forward distance list
    refStringMin = refString
    n = 1
    # for i in range(pageFrameNum):
    #     a = refStringMin.pop(0)
    #     pageFault.append(a) #초기에는 메모리가 비어있으므로 page Frame 수 만큼 fault 발생
    #     memory.append(a)
    #     pageFaultIndex.append(n)
    #     n += 1 #페이지 처리되면 index +1
    while True:
        if len(refStringMin) == 0: #page가 모두 처리되면 break
            print("Page Fault 총 횟수: %s" % len(pageFault))
            print("메모리 상태 변화과정(Time): %s" % pageFaultIndex)
            break
        incomingPage = refStringMin.pop(0) #처리되는 page number
        # print("refstringMin: %s"%refStringMin)
        # print("memory", memory)
        if incomingPage in memory:
            # print("passed!", incomingPage)
            n += 1
            continue
        else: #메모리에 해당 페이지가 없을 경우 page fault 발생
            # print("fault!", incomingPage)
            pageFault.append(incomingPage)
            pageFaultIndex.append(n)
            if len(memory) < pageFrameNum: #메모리가 비어있는 첫 시작
                memory.append(incomingPage)
                # n+=1 #once the memory becomes 4, below starts working
            else:
                for i in memory: #forward distance 구하기
                    m = 0
                    for page in refStringMin:
                        if i == page:
                            forwardDistance.append(m)
                            break
                        elif m == len(refStringMin)-1:
                            forwardDistance.append(m)
                        else:
                            m+=1
                # print("forwardDistance", forwardDistance)
                maxFD = [max(forwardDistance)] #forward distance가 제일 높은 값을 교체
                if len(maxFD) > 1:
                    highestFD = (maxFD)[0]
                elif len(maxFD) == 1:
                    highestFD = (maxFD)[0]
                # print("forwardDistance", forwardDistance)
                # print("highestFD", highestFD)
                victimIndex = forwardDistance.index(highestFD)
                victim = memory[victimIndex]
                memory.remove(victim)
                memory.append(incomingPage)
                forwardDistance = [] #초기화
        n += 1 #page index 증가


minAlgorithm()

# 3. LRU algorithm---------------------------------------------------------------------------------------

#1. page Frame number만큼 page fault 발생시키고 page fault 발생 표시, page fault
#2. 처리된 page는 list에 담고  reference string list에서 삭제
#3. 처리된 page list에서 메모리에 있는 각 page가 처음부터 시작해서 몇번째에 등장하는지 N+=1로 계산. 리스트를 생성. 해당 값이 제일 낮은 page를 교체
#4. 3,4번이 while loop으로 돌며 if 문을 넣어야 한다. if 첫번째 숫자가(참조되는 숫자) 메모리안에 있으면 pass.

#4. LFU algorithm---------------------------------------------------------------------------------------

#1. page Frame number만큼 page fault 발생시키고 page fault 발생 표시, page fault
#2. 처리된 page를 list에 담고 min 값을 구한다. min 값이 2개 이상일경우 LRU 알고리즘 적용
#3. #5. 3,4번이 while loop으로 돌며 if 문을 넣어야 한다. if 첫번째 숫자가(참조되는 숫자) 메모리안에 있으면 pass.

#5. Working set algorithm---------------------------------------------------------------------------------------

#1. window size +1 만큼 우선 page fault 발생시키고 표시. 그리고 page frame list에 추가 (reference string은 pop)
#2. 그다음부터 page하나가 처리되면 우선 page frame list의 first element 삭제.
#3. if문으로 해당 숫자가 page frame list에 있는지 확인. 있으면 pass, 없으면 page fault 표시.







# print("pageNum: %s" %pageNum)
# print("pageFrameNum: %s" %pageFrameNum)
# print("windowSize: %s" %windowSize)
# print("refStringLen: %s" % refStringLen)