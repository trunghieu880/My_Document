# against jira.atlassian.com.
from jira import JIRA
import base64
import datetime
import sys

def my_user(file):
    f = open(file, "r")
    contents = f.read()
    username = str(contents.split(",")[0].strip().replace('"', ''))
    password = str(contents.split(",")[-1].strip().replace('"', ''))

    result = {
        "username": username,
        "password": password
    }
    return dict(result)

options = {"server": "http://jira.banvien.com.vn"}
current_user = my_user("./my_pass")

username = str(current_user['username'])
password = str(current_user['password'])

my_jira = JIRA(options, basic_auth=(username, base64.b64decode(password).decode("utf-8")), validate=True)


def convert_sec2hour(number):
    if (number is not None):
        return number/3600
    else:
        return str("N/A")

def get_tickets(opt, my_issue=None, date=None):
    if opt == "all":
        my_issue = my_jira.search_issues('assignee = currentUser() order by updated DESC', fields=['summary', 'status', 'timeoriginalestimate', 'timeestimate', 'timespent', 'worklog'])
    elif opt == "open":
        my_issue = my_jira.search_issues('assignee = currentUser() AND resolution = Unresolved order by updated DESC')
    elif opt == "date":
        str_query = 'assignee = currentUser() AND worklogDate = ' + '"' + str(date.strftime("%Y/%m/%d")) + '"'
        my_issue = my_jira.search_issues(str(str_query), fields=['summary', 'status', 'timeoriginalestimate', 'timeestimate', 'timespent', 'worklog'])
    else:
        print("Don't Know")
        return 1

    if my_issue.total != 0:
        result = dict()
        for issue in my_issue:
            if(opt == "open"):
                result[issue.key] = {
                    "summary": issue.fields.summary,
                    'status': issue.fields.status.name,
                    "timeoriginalestimate": convert_sec2hour(issue.fields.timeoriginalestimate),
                    "timeestimate": convert_sec2hour(issue.fields.timeestimate),
                    "timespent": convert_sec2hour(issue.fields.timespent),
                }
            else:
                result[issue.key] = {
                    "summary": issue.fields.summary,
                    'status': issue.fields.status.name,
                    "timeoriginalestimate": convert_sec2hour(issue.fields.timeoriginalestimate),
                    "timeestimate": convert_sec2hour(issue.fields.timeestimate),
                    "timespent": convert_sec2hour(issue.fields.timespent),
                    'worklog': issue.fields.worklog
                }
        return result
    else:
        return None

def input_worklog_date():
    year = int(input("Year: "))
    month = int(input("Month: "))
    day = int(input("Day: "))

    # year = 2020
    # month = 1
    # day = 8
    result = datetime.datetime(year, month, day)

    return result

def log_work(my_jira, all_ticket):
    print("->Please input the day you want to log")

    input_date = input_worklog_date()
    print("->The date is: {}".format(input_date))
    list_ticket_date = get_tickets(opt="date", date=input_date)
    all_hour = 0

    if list_ticket_date is not None:
        for key in list_ticket_date.keys():
            for wlog in list_ticket_date[key]['worklog'].worklogs:
                wlog_date = datetime.datetime.strptime(str(str(wlog.updated).split("T")[0]), "%Y-%m-%d")
                if (check_matching_date(wlog_date, input_date) is True):
                    all_hour += convert_sec2hour(wlog.timeSpentSeconds)
                else:
                    continue
                # print("{} {}".format(key, all_hour))

    if all_hour >= 8:
        print("->Log hour today is full. No need to log more\n\n")
        return 0
    else:
        print("->You can log this date {}".format(input_date))
        ticket_id = input("Ticket name: ")
        work_hour = input("Log Hour: ")
        comment = input("Comment: ")

        if ticket_id in all_ticket.keys():
            if work_hour.isnumeric():
                opt = input("->Please confirm Y/N to continue: ")
                if opt == "Y":
                    print("->Logged {} for {} on {}\n".format(work_hour, ticket_id, input_date))
                    my_jira.add_worklog(ticket_id, timeSpent=work_hour, comment=comment)
            else:
                print("->Error: input hour is not numberic\n\n")
                return 1
        else:
            print("->Error: Ticket {} is not existed".format(ticket_id))
            return 1

def check_matching_date(wlog_date, input_date):
    return (wlog_date == input_date)

def main_screen():
    print("1. Show all ticket")
    print("2. Show open ticket")
    print("3. Show the tickets on specific date")
    print("4. Log work")
    print("Please type \"exit\" to Exit Program!!!")

def screen_ticket(opt, tickets=None, date=None):
    if opt == "all" or opt == "open" or opt == "date":

        if opt == "date":
            date = input_worklog_date()
            tickets = get_tickets(opt, date=date)
        else:
            tickets = get_tickets(opt)
    else:
        print("-> Error option is wrong")
        sys.exit()

    print("######################################")
    print("-------------" + str(opt).upper() + "TICKET---------------")
    print("######################################")
    if tickets is not None:
        for key in tickets.keys():
            print('\t{}: \n\t\tSummary: {} \n\t\tStatus: {}'.format(key, tickets[key]['summary'], tickets[key]['status']))

            if(opt == "date"):
                print("\t\torginalEstimate: {}h, remainingEstimate: {}h, timeSpent: {}h".format(tickets[key]['timeoriginalestimate'], tickets[key]['timeestimate'], tickets[key]['timespent']))
                print("\t\t\tWorklog:")
                for wlog in tickets[key]['worklog'].worklogs:
                    wlog_date = datetime.datetime.strptime(str(str(wlog.updated).split("T")[0]), "%Y-%m-%d")
                    if (check_matching_date(wlog_date, date) is True):
                        print("\t\t\t\t+ {}: {}h".format(key, convert_sec2hour(wlog.timeSpentSeconds)))
                    else:
                        continue

            else:
                print("\t\torginalEstimate: {}h, remainingEstimate: {}h, timeSpent: {}h".format(tickets[key]['timeoriginalestimate'], tickets[key]['timeestimate'], tickets[key]['timespent']))

    else:
        if opt == "date":
            print("None ticket [] is logged on {}".format(date))
        else:
            print("None ticket []")

    print("######################################")
    print("-------------" + str(opt).upper() + "TICKET---------------")
    print("######################################")

def main():
    while True:
        all_tickets = get_tickets(opt="all")
        main_screen()
        opt = input("Your choice: ")
        if opt == "1":
            screen_ticket(opt="all")
        elif opt == "2":
            screen_ticket(opt="open")
        elif opt == "3":
            screen_ticket(opt="date")
        elif opt == "4":
            log_work(my_jira, all_tickets)
        elif opt == "exit":
            print('Exiting')
            sys.exit()
        else:
            pass

if __name__ == "__main__":
    main()
