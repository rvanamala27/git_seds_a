"""
Node Class:
    This is responsible for storing task details in the class and can be added to linked list
"""


class Node:
    # Constructor Implementation
    def __init__(self, task_id, start_time, end_time):
        self.task_id = task_id
        self.start_time = start_time
        self.end_time = end_time
        self.next = None


"""
LinkedList Class:
    This is responsible for implementing Linked List for the tasks and is used for implementing
    various aggregate operations.
"""


class LinkedList:
    # Constructor Implementation
    def __init__(self):
        self.head = None

    # This method will return the head of the linked list
    def get_list_head(self):
        return self.head

    # This method is responsible for printing the linked list nodes
    def print_linked_list(self):
        tmp = self.head
        while tmp:
            if tmp:
                # print(f"task_id = {tmp.task_id}; start_time = {tmp.start_time}; end_time = {tmp.end_time}")
                print(f"{tmp.task_id}")
            tmp = tmp.next

    # This method is responsible for inserting node in the linked list
    # in the beginning or at end based on the flag as insert_at_starting
    def insert_node(self, node, insert_at_starting):
        if self.head is None:
            self.head = node
            return
        if insert_at_starting == 1:
            node.next = self.head
            self.head = node
        elif insert_at_starting == 0:
            tmp = self.head
            while tmp.next:
                tmp = tmp.next
            tmp.next = node

    # This method is responsible for printing the linked list nodes in reverse order
    def print_in_reverse(self, node):
        if node is None:
            return
        self.print_in_reverse(node.next)
        # print(f"task_id = {node.task_id}; start_time = {node.start_time}; end_time = {node.end_time}")
        print(f"{node.task_id}")
