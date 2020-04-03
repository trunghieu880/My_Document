if __name__ == '__main__':
    l = []
    # for _ in range(int(input())):
    #     print("name")
    #     name = input()
    #     score = float(input())
    #     l.append([name, score])


    students = [['Test4', 55], ['Test2', 53], ['Test3', 53], ['Test4', 54]]


    min = students[0][1]
    runner_up = students[0][1]
    l_result = []
    for name, score in students:
        if score < min:
            min = score

    for name, score in students:
        if score < runner_up:
            runner_up = score
        else:
            if runner_up == min and score > min:
                runner_up = score


    for name, score in students:
        if score == runner_up:
            l_result.append([name, score])

    l_result = sorted(l_result)
    for name, score in l_result:
        print(name)

