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


def Min_algorithm():
    pageFault = []
    pageFaultIndex = [] #몇번째 page에서 fault가 발생했는지 확인
    memory = []
    forwardDistance = [] #forward distance list
    refStringMin = refString[:]
    n = 1
    while True:
        if len(refStringMin) == 0: #page가 모두 처리되면 break
            print("Min 알고리즘 기법 결과--------------------------------------------------------")
            print("Page Fault 총 횟수: %s" % len(pageFault))
            print("메모리 상태 변화과정(Time): %s \n" % pageFaultIndex)
            break
        incomingPage = refStringMin.pop(0) #처리되는 page number
        if incomingPage in memory:
            n += 1
            continue
        else: #메모리에 해당 페이지가 없을 경우 page fault 발생
            pageFault.append(incomingPage)
            pageFaultIndex.append(n)
            if len(memory) < pageFrameNum: #메모리가 비어있는 첫 시작
                memory.append(incomingPage)
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
                maxFD = [max(forwardDistance)] #forward distance가 제일 높은 값을 교체
                if len(maxFD) > 1:
                    highestFD = (maxFD)[0]
                elif len(maxFD) == 1:
                    highestFD = (maxFD)[0]
                victimIndex = forwardDistance.index(highestFD)
                victim = memory[victimIndex]
                memory.remove(victim)
                memory.append(incomingPage)
                forwardDistance = [] #초기화
        n += 1 #page index 증가


Min_algorithm()

# 3. LRU algorithm---------------------------------------------------------------------------------------

#1. page Frame number만큼 page fault 발생시키고 page fault 발생 표시, page fault
#2. 처리된 page는 list에 담고  reference string list에서 삭제
#3. 처리된 page list에서 메모리에 있는 각 page가 처음부터 시작해서 몇번째에 등장하는지 N+=1로 계산. 리스트를 생성. 해당 값이 제일 낮은 page를 교체
#4. 3,4번이 while loop으로 돌며 if 문을 넣어야 한다. if 첫번째 숫자가(참조되는 숫자) 메모리안에 있으면 pass.


def LRU_algorithm():
    global pageNum
    global pageFrameNum
    global windowSize
    global refStringLen
    global refString
    pageFault = []
    pageFaultIndex = [] #몇번째 page에서 fault가 발생했는지 확인
    memory = []
    backwardDistance = [] #backward distance list
    refHistory = [] #참조한 페이지 list
    refStringLRU = refString[:]
    n = 1
    while True:
        if len(refStringLRU) == 0: #page가 모두 처리되면 break
            print("LRU 알고리즘 기법 결과--------------------------------------------------------")
            print("Page Fault 총 횟수: %s" % len(pageFault))
            print("메모리 상태 변화과정(Time): %s \n" % pageFaultIndex)
            break
        incomingPage = refStringLRU.pop(0) #처리되는 page number
        if incomingPage in memory:
            # print("passed!", incomingPage)
            n += 1
            refHistory.append(incomingPage)
            continue
        else: #메모리에 해당 페이지가 없을 경우 page fault 발생
            pageFault.append(incomingPage)
            pageFaultIndex.append(n)
            if len(memory) < pageFrameNum: #메모리가 비어있을때 첫 시작
                memory.append(incomingPage)
                refHistory.append(incomingPage)
            else:
                refHistory.reverse() #referenced History를 reverse해서 recently referenced page 확인
                for i in memory: #backward distance 구하기
                    m = 0
                    for page in refHistory:
                        if i == page:
                            backwardDistance.append(m)
                            break
                        elif m == len(refHistory)-1:
                            backwardDistance.append(m)
                        else:
                            m+=1
                refHistory.reverse() #refHistory다시 원상복구
                maxBD = [max(backwardDistance)] #backward distance가 제일 높은 값을 교체
                if len(maxBD) > 1:
                    highestBD = (maxBD)[0] #tie-breaking rule로 첫번째 선정
                elif len(maxBD) == 1:
                    highestBD = (maxBD)[0]
                victimIndex = backwardDistance.index(highestBD)
                victim = memory[victimIndex]
                memory.remove(victim)
                memory.append(incomingPage)
                backwardDistance = [] #초기화
                refHistory.append(incomingPage)
        n += 1 #page index 증가


LRU_algorithm()


#4. LFU algorithm---------------------------------------------------------------------------------------

#1. page Frame number만큼 page fault 발생시키고 page fault 발생 표시, page fault
#2. 처리된 page를 list에 담고 min 값을 구한다. min 값이 2개 이상일경우 LRU 알고리즘 적용
#3. #5. 3,4번이 while loop으로 돌며 if 문을 넣어야 한다. if 첫번째 숫자가(참조되는 숫자) 메모리안에 있으면 pass.
# 각 페이지가 담긴 리스트 생성 (pageList)
# 각 페이지를 for loops로 ref string에서 몇번 등장하는지 계산하고 refCount list 생성
# compareList 만들어서 매번 메모리에 있는 페이지들의 refCount를 넣고 min 숫자를 victim으로 선정.
# if statement를 넣어서 만약에 min value가 2개 이상일 시에 tie breaking rule로 LRU를 통해 victim 선정. LRU내에서 tie breaking rule은 제일 첫번째 선정
# pageList의 index와 refcount List 의 index를 동일하게 할것.

def LFU_algorithm():
    global pageNum
    global pageFrameNum
    global windowSize
    global refStringLen
    global refString
    pageFault = []
    pageFaultIndex = []  # 몇번째 page에서 fault가 발생했는지 확인
    memory = []
    backwardDistance = []  # backward distance list
    refHistory = []  # 참조한 페이지 list
    pageList = []
    refCount = []
    refStringLFU = refString[:]
    n = 1
    [pageList.append(page) for page in refStringLFU if page not in pageList] #page number 리스트 생성
    for i in pageList: #reference count
        m = 0
        for j in refStringLFU:
            if i == j:
                m += 1
            else:
                continue
        refCount.append(m)
    while True:
        if len(refStringLFU) == 0: #page가 모두 처리되면 break
            print("LFU 알고리즘 기법 결과--------------------------------------------------------")
            print("Page Fault 총 횟수: %s" % len(pageFault))
            print("메모리 상태 변화과정(Time): %s \n" % pageFaultIndex)
            break
        incomingPage = refStringLFU.pop(0) #처리되는 page number
        if incomingPage in memory:
            n += 1
            refHistory.append(incomingPage)
            continue
        else: #메모리에 해당 페이지가 없을 경우 page fault 발생
            pageFault.append(incomingPage)
            pageFaultIndex.append(n)
            if len(memory) < pageFrameNum: #메모리가 비어있을때 첫 시작
                memory.append(incomingPage)
                refHistory.append(incomingPage)
            else:
                compareList = []
                for page in memory: # ref count수를 비교하기 위한 compareList 만들기
                    pageIndex = pageList.index(page) #pageList에서 해당 page의 index 찾기
                    compareList.append(refCount[pageIndex])
                minRef = [min(compareList)]  # reference count가 제일 낮은 수 찾기
                if len(minRef) > 1: # reference count가 제일 낮은 수가 하나 이상인 경우 tie-breaking rule로 LRU 사용
                    pageNumbers = []
                    for i in minRef: #각 ref count의 page number 구하기
                        a = compareList.index(i)
                        pageNumber = memory[a]
                        pageNumbers.append(pageNumber)
                    refHistory.reverse()  # referenced History를 reverse해서 recently referenced page 확인
                    for i in pageNumbers:  # backward distance 구하기
                        m = 0
                        for page in refHistory:
                            if i == page:
                                backwardDistance.append(m)
                                break
                            elif m == len(refHistory) - 1:
                                backwardDistance.append(m)
                            else:
                                m += 1
                    refHistory.reverse()  # refHistory다시 원상복구
                    maxBD = [max(backwardDistance)]  # backward distance가 제일 높은 값을 교체
                    if len(maxBD) > 1:
                        highestBD = (maxBD)[0]  # backward distance가 동일한 page가 두개 이상일 경우 tie-breaking rule로 첫번째 선정
                    elif len(maxBD) == 1:
                        highestBD = (maxBD)[0]
                    victimIndex = backwardDistance.index(highestBD)
                    victim = memory[victimIndex]
                    memory.remove(victim)
                    memory.append(incomingPage)
                    backwardDistance = []  # 초기화
                    refHistory.append(incomingPage)

                elif len(minRef) == 1: # ref count가 제일 낮은 수가 하나인 경우
                    lowestRf = (minRef)[0]
                    victimIndex = compareList.index(lowestRf)
                    victim = memory[victimIndex]
                    memory.remove(victim)
                    memory.append(incomingPage)
                    refHistory.append(incomingPage)
        n += 1 #page index 증가


LFU_algorithm()



#5. Working set algorithm---------------------------------------------------------------------------------------
# 처음에 win size만큼 메모리에 페이지 추가
#memory에 page가 추가되면서 while loop 위에 if statement에 window size
def WS_algorithm():
    global pageNum
    global pageFrameNum
    global windowSize
    global refStringLen
    global refString
    pageFault = []
    pageFaultIndex = []  # 몇번째 page에서 fault가 발생했는지 확인
    memory = []
    refHistory = []  # 참조한 페이지 list
    refStringWS = refString[:]
    n = 1 #index count 계산
    m = 0
    while True:
        if len(refStringWS) == 0: #page가 모두 처리되면 break
            print("Working Set 알고리즘 기법 결과--------------------------------------------------------")
            print("Page Fault 총 횟수: %s" % len(pageFault))
            print("메모리 상태 변화과정(Time): %s \n" % pageFaultIndex)
            break
        incomingPage = refStringWS.pop(0) #처리되는 page number
        if incomingPage in memory: #해당 page가 메모리에 있으면 pass
            n += 1
            refHistory.append(incomingPage)
            continue
        else: #메모리에 해당 페이지가 없을 경우 page fault 발생
            pageFault.append(incomingPage)
            pageFaultIndex.append(n)
            
  #처음에 어떻게 메모리를 담고 시작할 건지. 한가지 참고해야할 것은 메모리 사이즈에 if 문을 넣어서 len(memory) == winsize 일때는 메모리에서 지우는 일이 없어야한다.
  # m은 필요 없을 거 같고 그냥 매번 len(memory) winsize를 벗어나면 메모리에서 pop한다.






#1. window size +1 만큼 우선 page fault 발생시키고 표시. 그리고 page frame list에 추가 (reference string은 pop)
#2. 그다음부터 page하나가 처리되면 우선 page frame list의 first element 삭제.
#3. if문으로 해당 숫자가 page frame list에 있는지 확인. 있으면 pass, 없으면 page fault 표시.







# print("pageNum: %s" %pageNum)
# print("pageFrameNum: %s" %pageFrameNum)
# print("windowSize: %s" %windowSize)
# print("refStringLen: %s" % refStringLen)