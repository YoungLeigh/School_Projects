# 1. 텍스트 파일에 입력된 정보를 리스트들에 저장---------------------------------------------------------------------------------------
import numpy as np
no_of_Runits = []
req_Matrix = []
alloc_Matrix = []
process_List = []
def add_values():  # 텍스트 파일의 정보를 리스트들에 입력하는 함수
    global no_of_p
    global no_of_Rtypes
    global no_of_Runits
    open("input.txt", "r", encoding="UTF-8")
    with open("input.txt") as f:
        data = f.read().splitlines()
    numbers = []
    for i in data: #띄어쓰기를 기준으로 데이터 분리
        numbers.extend((i.split()))
    for i in range(0, len(numbers)): #문자열 데이터를 정수형으로 변환
        numbers[i] = int(numbers[i])
    no_of_p = numbers.pop(0) #프로세스 개수 가져오기
    no_of_Rtypes = numbers.pop(0) #Resource types 개수 가져오기
    for _ in range(no_of_Rtypes): #Resource units 개수 가져오기
        no_of_Runits.append(numbers.pop(0))
    n = 0
    for _ in range(no_of_p): #process 개수 만큼 numbers 리스트에서 슬라이싱을 통해 Allocation matrix에 담기
        alloc_Matrix.append(numbers[0+n:no_of_Rtypes+n])
        n += no_of_p #index를 증가하기 위해 프로세스 수 만큼 더하기
    n = 0
    m = no_of_p*no_of_Rtypes
    for _ in range(no_of_p): #process 개수 만큼 numbers 리스트에서 슬라이싱을 통해 Request matrix에 담기
        req_Matrix.append(numbers[m+n:m+no_of_Rtypes+n])
        n += no_of_p
    for i in range(no_of_p): #Process 리스트 생성
        i += 1
        process_List.append("P"+str(i))


add_values()



# 2. Deadlock detection---------------------------------------------------------------------------------------
# array_Runits = np.array(no_of_Runits)
# array_Rtypes = np.array(no_of_Rtypes)
# total_Runits = list(np.multiply(array_Runits, array_Rtypes)) #각 Resource type의 Resource units 총 합 구하기


def find_remaining(current_allocation): #remaining resource units의 합을 찾는 함수
    totalList = []
    sum1 = []
    remainList = []
    for n in range(len(alloc_Matrix)): #total resource units 구하기
        for i in current_allocation:
            sum1.append(i[n])
        totalList.append(sum(sum1))
        sum1 = []
    for n in range(len(totalList)):
        remainList.append(no_of_Runits[n]-totalList[n]) #total resource units와 allocated resource units의 차 구하기
    return remainList


remainList = find_remaining(alloc_Matrix)


def check_Unblocked(remainList, req_Matrix): #unblocked process 찾는 함수
    p_index = []
    for n in range(len(req_Matrix)):  # total resource units 구하기
        for i in req_Matrix:
            if i[n] < remainList[n]:
                p_index.append(n) #몇번째 리스트가 unblocked process인지 확인
    return p_index

unblocked_pIndex = check_Unblocked(remainList, req_Matrix)
print(unblocked_pIndex)

def delete_node(n, alloc_Matrix1, req_Matrix1, remainList1, unblocked_pIndex, new_RemainList1):
    global new_unblocked_pIndex
    for j in range(len(unblocked_pIndex)):
        i = unblocked_pIndex[j]
        for m in range(len(remainList)):  # unblocked process 수 만큼
            new_RemainList1.append(remainList1[m] + alloc_Matrix1[n][m])  # unblocked process node 지우고 new R_units 값
        alloc_Matrix1.remove(alloc_Matrix1[i])  # 처리한 이후 리스트에서 삭제
        req_Matrix1.remove(req_Matrix1[i])
        new_unblocked_pIndex = check_Unblocked(new_RemainList1, req_Matrix1)  # 그다음 처리할 수 있는 프로세스 찾기
    if len(req_Matrix1) == 0:
        return
    delete_node(n, alloc_Matrix1, req_Matrix1, remainList1, new_unblocked_pIndex, new_RemainList1)

def graph_reduction():
    global unblocked_pIndex
    for n in unblocked_pIndex: #unblocked process 개수 만큼 실행
        alloc_Matrix1 = alloc_Matrix[:]
        req_Matrix1 = req_Matrix[:]
        remainList1 = remainList[:]
        new_RemainList = []
        delete_node(n, alloc_Matrix1, req_Matrix1, remainList1, unblocked_pIndex, new_RemainList)

graph_reduction()


# a_allocated = np.array(alloc_Matrix)
# total_allocated = sum(a_allocated, 0) #각 Resource type의 allocated resource units 총 합 구하기
# a_Runits = np.array(no_of_Runits)
# remain_Runits = np.subtract(a_Runits, total_allocated) #R_units와 allocated units의 차 구하기
# dlocked_Process = []
# unblocked_Process = []
#
#
# #-----------------------------------------------------------------------------
#
# def deadlock_detection():
#     global dlocked_Process
#     a_req_mat = np.array(req_Matrix) #array로 만든 requested matrix
#     a_alloc_mat = a_allocated #array로 만든 allocated matrix
#     a_rrunits = remain_Runits #array로 만든 Remaining resource units
#     m = 0
#     n = 0
#     while True: #graph reduction 기법
#         if no_of_p < n:  # request matrix를 모두 확인하면 while loop 나오기
#             break
#         elif a_req_mat.size == 0: #모든 리스트들이 처리되어 지워졌을때 (모든 process들이 allocated 받았을때)
#             print("Deadlock Detection 결과 deadlocked process가 없습니다.")
#             break
#         subt_value = np.subtract(a_rrunits, a_req_mat[n])  # req matrix와 remaining units의 차 구하기
#         if np.any(subt_value<0) == True: #subt_value 값에 negative 값이 있을 시
#             n += 1
#             continue
#         if np.any(subt_value<0) == False: #sub_value 값에 negative 값이 없을 시 = unblocked process
#             unblocked_Process.append(n)
#             a_rrunits = np.sum(a_alloc_mat[n], a_rrunits)
#             np.delete(a_req_mat, n, 0)  # requsted matrix에서 처리한 list는 삭제
#             np.delete(a_alloc_mat, n, 0)
#             n = 0 #requested matrix 처음부터 다시 확인

#모두 deadlock 일때
#하나만 deadlock일때
#하나 이상이 deadlock 일떄 어떻게 확인하는지

        # print(subt_value)
        # print(a_req_mat)
        # print(a_rrunits)



# deadlock_detection()

# requested R_units - remaining r units = 0보다 크다면, (pop을 해야한다)
# 해당 process를 allocated R_units에서 찾아서 remaining에 더해준다
#
# requested R_units -remaining r units = 0보다 크다면, (pop을 해야한다)
# 해당 process를 allocated R_units에서 찾아서 remaining에 더해준다
#
# (1) 만약에, Requested Runits가 모두 pop되어 빈 리스트가 되면, deadlock이 없는 것으로 판정
# (2) 만약에, requested - remaining을 했을때, 0보다 작다면, pass를 하고 나머지 process들을 deadlock list에 추가한다.




print("list of processes: %s" %process_List)
print("no of processes: %s" %no_of_p)
print("no of Resource types: %s" %no_of_Rtypes)
print("no of Resource units: %s" %no_of_Runits)
print("Allocated R_units matrix: %s" %alloc_Matrix)
print("Requested R_units matrix: %s" % req_Matrix)
