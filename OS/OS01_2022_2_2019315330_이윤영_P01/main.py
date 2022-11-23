# 1. 텍스트 파일에 입력된 정보를 리스트들에 저장하는 단계 --------------------------------------------------------------------
PIDs, ATs, BTs = [], [], []


def add_dot():  # 텍스트 파일의 마지막 줄에 띄어쓰기를 넣어 컴퓨터가 맨 뒤로 부터 두번째 값만 읽을 수 있도록 하는 함수
    append = open("input.txt", "a")
    append.write(" ")
    append.close()


def add_values():  # 텍스트 파일의 정보를 리스트들에 입력하는 함수
    global no_of_p
    openFile = open("input.txt", "r", encoding="UTF-8")
    lines = openFile.readlines()
    no_of_p = int(lines[0][-2])  # 프로세스 개수
    listOfPID = lines[1:no_of_p + 1]  # 텍스트파일의 PID 리스트만 읽어오기
    listOfAT = lines[no_of_p + 1:no_of_p * 2 + 1]  # 텍스트파일의 Arrival Time 리스트만 읽어오기
    listofBT = lines[no_of_p * 2 + 1:no_of_p * 3 + 1]  # 텍스트파일의 Burst Time 리스트만 읽어오기
    for pid in listOfPID:
        PIDs.append(pid[-2])
    for at in listOfAT:
        ATs.append(at[-2])
    for bt in listofBT:
        BTs.append(bt[-2])
    openFile.close()


add_dot()
add_values()


class MyDictionary(dict):  # 딕셔너리 생성 클라스
    def __init__(self):
        self = dict()

    def add(self, key, value):  # 딕셔너리에 키와 값을 append해주는 함수
        self[key] = value


AT_dic = MyDictionary()
BT_dic = MyDictionary()


def dict_add():  # 딕셔너리에 PID 값과 AT,BT값을 넣어주는 함수
    n = 0
    for _ in range(no_of_p):  # {PID:BT}값과 {PID:AT}값을 갖는 두개의 딕셔너리 생성
        AT_dic.add(int(PIDs[n]), int(ATs[n]))
        BT_dic.add(int(PIDs[n]), int(BTs[n]))
        n += 1


dict_add()
Q01 = sorted(AT_dic.items(), key=lambda x: x[1])  # PID 값과 Arrival time을 묶어서 Q0에 AT 순으로 저장
Q0 = []
Q02 = []
for i in Q01:  # tuple로 되어있는 값을 리스트로 변환
    Q02.append(list(i))
for i in Q02:  # PID와 Arrival time으로 이루어진 리스트를 PID와 Burst time으로 변환하여 Q0에 추가
    Q0.append([i[0], BT_dic[i[0]]])

# 2. 첫 번째 Ready Queue Q0 프로세스 (Time quantum = 2) ---------------------------------------------------------------

GanttChart = []
Q1 = []
Q2 = []
time = []

while Q0 != []:  # 첫번째 Ready Queue RR 스케줄링
    if Q0[0][1] > 2:
        GanttChart.append([Q0[0][0], 2])  # Burst time이 2보다 큰 경우 ganttchart에 CPU 할당시간을 2로 저장
        Q0[0][1] = Q0[0][1] - 2  # BT값 -2
        Q1.append(Q0[0])
        time.append(2)  # Scheduling Time 기록
    else:
        GanttChart.append([Q0[0][0], Q0[0][1]])  # Burst time이 2보다 작은경우 ganttchart에 BT값 그대로 저장
        time.append(Q0[0][1])  # burst time 추가
        time.append("P" + str(Q0[0][0]))  # scheduling 끝난 process 기록
    Q0.remove(Q0[0])

# 3. 두 번째 Ready Queue Q1 프로세스 (Time quantum = 4)----------------------------------------------------------------

while Q1 != []:  # 두번째 Ready Queue RR 스케줄링
    if Q1[0][1] > 4:
        GanttChart.append([Q1[0][0], 4])
        Q1[0][1] = Q1[0][1] - 4  # BT값 -2
        Q2.append(Q1[0])
        time.append(4)  # Scheduling Time 기록
    else:
        GanttChart.append([Q1[0][0], Q1[0][1]])
        time.append(Q1[0][1])  # burst time 추가
        time.append("P" + str(Q1[0][0]))  # scheduling 끝난 process 기록
    Q1.remove(Q1[0])


# 4. 세 번째 Ready Queue Q2 프로세스 (SPN Scheduling)----------------------------------------------------------------


def Sort(sub_li):  # 두번째 Ready Queue를 짧은 Burst time 순으로 정렬하는 함수
    sub_li.sort(key=lambda x: x[1])
    return sub_li


Sort(Q2)


def q2_process():  # 세 번째 Ready Queue SPN 스케줄링 함수
    for _ in range(len(Q2)):
        GanttChart.append(Q2[0])  # Q2에 남은 process를 GanttChart에 append한 후 삭제
        time.append(Q2[0][1])  # burst time 추가
        time.append("P" + str(Q2[0][0]))  # scheduling 끝난 process 기록
        Q2.remove(Q2[0])


q2_process()

# 5. 다섯 번째 Average Turnaround Time 및 Average Wait Time 구하기---------------------------------------------------
endTime_dic = MyDictionary()
pid_list = [x for x in time if not isinstance(x, int)]  # time 리스트에 기록된 Process ID로 리스트 구성
n = 0
for i in time:  # PID와 end time 딕셔너리 형태로 기록
    if i in pid_list:  # time을 차례대로 더하고 PID가 나올경우 PID에 딕셔너리 값으로 배정
        endTime_dic.add(i, n)
    else:
        n += int(i)
m = 1
tt = []
tt_list = []
wt = []
wt_list = []
et_list = []
et_s = sorted(endTime_dic.items(), key=lambda x: x[0])  # PID 순서대로 튜플로 end time 저장
for i in et_s:  # tuple로 되어있는 값을 리스트로 변환
    et_list.append(list(i))
for i in et_list:
    tt.append(i[1] - AT_dic[m])
    tt_list.append([i[0], i[1] - AT_dic[m]])
    m += 1
s = 1
o = 0
while True:
    if s == 6:
        break
    else:
        wt.append(tt_list[o][1] - BT_dic[s])
        wt_list.append([tt_list[o][0], tt_list[o][1] - BT_dic[s]])
    s += 1
    o += 1

tt_average = sum(tt) / int(no_of_p)
wt_average = sum(wt) / int(no_of_p)

# 6. GanttChart 및 실행 결과 출력------------------------------------------------------------------------------------
gantt_chart = []
for i in GanttChart:  # 갠트차트 시각화
    gantt_chart.append(["P" + str(i[0]), i[1]])


def visualized_chart():  # 갠트차트 출력 함수
    print("\nGanttchart(Visualized): ", end="")
    for process in GanttChart:
        print("P" + str(process[0]) + " ", end="")
        print("O" * process[1] + " ", end="")
    print("\n")
    print("Ganttchart: ", end="")
    print(gantt_chart)
    print("\n")


print("Average Turnaround time: ", tt_average)
print("Average Wait time: ", wt_average)
print("Turnaround time of Processes: ", tt_list)
print("Wait time of Processes: ", wt_list)

visualized_chart()

# print("Process IDs = %s" % PIDs)
# print("Arrival Times = %s" % ATs)
# print("Burst Times = %s" % BTs)
# print("Arrival Times Dictionary = %s" % AT_dic)
# print("Burst Times Dictionary = %s" % BT_dic)
# print("Q0: ", Q0)
# print("Q1: ", Q1)
# print("Q2: ", Q2)
# print('Ganttchart: ', GanttChart)
# print("time: ", time)
# print("pidlist: ", pid_list)
# print("endtime: ", endTime_dic)
# print("average turnaround time: ", tt_average)
# print("average wait time: ", wt_average)
# print("tt list:", tt_list)
# print("wt list: ", wt_list)
