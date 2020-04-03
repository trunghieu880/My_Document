#a = [1, 2, 3, 0, 2, 3, 4, 5, 6]

def swapPositions(list, pos1, pos2): 
      
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

students = [['Test4', 533.5], ['Test2', 53], ['Test3', 53], ['Test4', 54]]

position = 0
a = [score for name, score in students]

for i in range(0, len(a)):
    j = i + 1
    position = i
    temp = a[i]
    temp_students = students[i]
    for j in range(j, len(a)):
        if(a[j] < temp):
            temp = a[j]
            temp_students = students[j]
            position = j
    
    a[position] = a[i]
    a[i] = temp
    students[position] = students[i]
    students[i] = temp_students

print(students)

