from src.LinkedList import LinkedList

"""
Aggregate class is responsible for implementing various operations on the linked list
    1. Get Minimum Timed Task Details
    2. Get Maximum Timed Task Details
    3. Get Average of all the execution times of the tasks pushed in the linked list
"""


class Aggregate:

    # Initializing linked list object for various operations
    def __init__(self, linked_list: LinkedList):
        self.linked_list = linked_list

    # Function responsible for searching the task having maximum execution time among all the tasks
    def get_maximised_time_task(self):
        tmp_ll = self.linked_list
        tmp = tmp_ll.get_list_head()
        start_t = tmp.start_time
        end_t = tmp.end_time
        task_run_time = end_t - start_t
        check_task_id = tmp.task_id
        while tmp:
            if task_run_time < tmp.end_time - tmp.start_time:
                task_run_time = tmp.end_time - tmp.start_time
                check_task_id = tmp.task_id
            tmp = tmp.next
        return check_task_id, task_run_time

    # Function responsible for searching the task having minimum execution time among all the tasks
    def get_minimised_timed_task(self):
        tmp_ll = self.linked_list
        tmp = tmp_ll.get_list_head()
        start_t = tmp.start_time
        end_t = tmp.end_time
        task_run_time = end_t - start_t
        check_task_id = tmp.task_id
        while tmp:
            if task_run_time > tmp.end_time - tmp.start_time:
                task_run_time = tmp.end_time - tmp.start_time
                check_task_id = tmp.task_id
            tmp = tmp.next
        return check_task_id, task_run_time

    # Function responsible for calculating average of the all execution times of the tasks in the linked list
    def get_average_time_of_all_tasks(self):
        tmp_ll = self.linked_list
        tmp = tmp_ll.get_list_head()
        sum_task_times = 0
        no_of_nodes = 0

        while tmp:
            task_run_time = tmp.end_time - tmp.start_time
            sum_task_times += task_run_time
            no_of_nodes += 1
            tmp = tmp.next
        average = sum_task_times / no_of_nodes
        return average, sum_task_times, no_of_nodes
