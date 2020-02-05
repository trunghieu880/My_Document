import json
import jira
from jira import JIRAError
import sys
import getpass

# This script use to manage ticket on jira, option
#   : 1. My tickets. List all ticket assign to you
#   : 2. Ticket details. Ticket details.
#   : ...
# refer: https://jira.readthedocs.io/en/latest/examples.html

JIRA_URL = 'http://jira.banvien.com.vn'

print("Enter jira user name & password")
username = input("User: ")
#password = input("Pass: ")
password = getpass.getpass("Pass: ")

my_jira = jira.JIRA(JIRA_URL, basic_auth=(username, password))
# or hard-code usename/password
#my_jira = jira.JIRA(JIRA_URL, basic_auth=('name', 'pass'))

#
# get list of my ticket
#
def get_my_ticket():
    print("My ticket:")
    my_issue = my_jira.search_issues('assignee = currentUser() AND resolution = Unresolved order by updated DESC')
    for issue in my_issue:
        print('{}: \n\tSummary: {} \n\tStatus: {}'.format(issue.key, issue.fields.summary, 'status'))

#
# print options to console, return option as integer
#
def print_option():
    while True:
        print('1. My ticket.')
        print('2. Ticket details.')
        print('3. Exit.')
        try:
            option = int(input('Select action (1 or 2, ..): '))
        except ValueError:
            print('Invalid input')
        else:
            if 1 <= option <= 3:
                break
            else:
                print('Input out of range')
    # End while
    return option


#
# main entry
#
def main():
    while True:
        print('--------------------------------------------------------------')
        action = print_option()
        if action == 1:
            get_my_ticket()
        elif action == 2:
            ticket_id = input("Ticked ID: ")
            try:
                my_issue = my_jira.issue(ticket_id)
                print("\tSummary: {}".format(my_issue.fields.summary))
                print('\tStatus: {}'.format(my_issue.fields.status))
                print('\tDescription:')
                for line in my_issue.fields.description.split('\n'):
                    print("\t\t{}".format(line))
                print("\tSubtasks: {}".format(my_issue.fields.subtasks))
                print("\torginalEstimate: {}, remainingEstimate: {}, timeSpent: {}".format(my_issue.fields.timetracking.originalEstimate, my_issue.fields.timetracking.remainingEstimate, my_issue.fields.timetracking.timeSpent))
            except JIRAError as e:
                print("An error occured {} {}".format(e.status_code, e.text))

            # TODO
            pass
        else:
            print('Exiting')
            sys.exit()
        print('-------------------------------------------------------------\n')

if __name__ == '__main__':
    main()

