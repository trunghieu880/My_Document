if __name__ == '__main__':
    N = int(input())
    l_a = list()
    
    for i in range(N):
        command = input().strip()
        if "insert" in command:
            index = int(command.split(" ")[1])
            val = int(command.split(" ")[2])
            l_a.insert(index, val)
        elif "print" in command:
            print(l_a)
        elif "remove" in command:
            val = int(command.split(" ")[1])
            l_a.remove(val)
        elif "append" in command:
            val = int(command.split(" ")[1])
            l_a.append(val)
        elif "sort" in command:
            l_a.sort()
        elif "pop" in command:
            l_a.pop()
        elif "reverse" in command:
            l_a.reverse()