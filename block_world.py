#!/usr/bin/python3

from enum import Enum


class action(Enum):
    pick_up = 1
    put_down = 2
    stack_up = 3
    unstack = 4


class predicate(Enum):
    on = 5
    on_table = 6
    clear = 7
    holding = 8
    armempty = 9


input_state = [['b', 'a'], ['c']]
output_state = [['c', 'b', 'a']]


def solve(input_notation, output_notation):
    stack = []
    input_notation = set(input_notation)
    output_notation = set(output_notation)
    stack.append(list(output_notation))
    while len(stack) != 0:
        top_stack = stack[-1]
        if isinstance(top_stack, list):
            stack.pop()
            for sub_goal in top_stack:
                stack.append(sub_goal)
        elif isinstance(top_stack[0], action):
            #Perform the precondition for it
            preconditions = list()
            delete = list()
            Add = list()
            satisfy_pre_condition = True
            string = ""
            if top_stack[0] == action.pick_up:
                # check for precondition
                """
                    Pick up : pick_up(X)
                    1.Precondition :
                        A.clear X
                        B.ontable(X)
                        C.Hand_empty
                    2.Delete condition:
                        A.clear(X)
                        b.Ontable(x)
                        c.Handempty
                    3.Add list:
                        A.Holding(x)
                """
                x = top_stack[1]
                preconditions.extend([(predicate.clear, x),
                                      (predicate.on_table, x),
                                      (predicate.armempty, )])
                delete.extend([(predicate.clear, x), (predicate.on_table, x),
                               (predicate.armempty, )])
                Add.extend([(predicate.holding, x)])
                string += "Pickup ({})".format(x)

            elif top_stack[0] == action.put_down:
                """
                    1.Precondition:
                        a. holding(x)
                    2.delete condition:
                        a. holding(x)
                    3.Add list :
                        a. clear(x)
                        b. on_table(x)
                        c. handempty
                """
                x = top_stack[1]
                preconditions.extend([(predicate.holding, x)])
                delete.extend([(predicate.holding, x)])
                Add.extend([(predicate.clear, x), (predicate.on_table, x),
                            (predicate.armempty, )])
                string += "PutDown({})".format(x)

            elif top_stack[0] == action.stack_up:
                """
                    1.Precondition:
                        a.Holding(x)
                        b.clear(y)
                    2.delete condition:
                        a.Holding(x)
                        b.clear(y)
                    3.add list:
                        a.clear(x)
                        b.On(x,y)
                        c.Handempty
                """
                x = top_stack[1]
                y = top_stack[2]
                preconditions.extend([(predicate.holding, x),
                                      (predicate.clear, y)])
                delete.extend([(predicate.holding, x), (predicate.clear, y)])
                Add.extend([(predicate.clear, x), (predicate.on, x, y),
                            (predicate.armempty, )])
                string += "stack({},{})".format(x, y)

            else:
                # this is unstack
                """
                    1.Precondition:
                        a.clear(x)
                        b.on(x,y)
                        c.handempty
                    2.delete condition:
                        a.clear(x)
                        b.on(x,y)
                        c.handempty
                    3.Add list:
                        a.holding(x)
                        b.clear(y)
                """
                x = top_stack[1]
                y = top_stack[2]
                preconditions.extend([(predicate.clear, x),
                                      (predicate.on, x, y),
                                      (predicate.armempty, )])
                delete.extend([(predicate.clear, x), (predicate.on, x, y),
                               (predicate.armempty, )])
                Add.extend([(predicate.holding, x), (predicate.clear, y)])
                string += "Unstack({},{})".format(x, y)

            for precondition in preconditions:
                if precondition not in input_notation:
                    satisfy_pre_condition = False
                    stack.append(precondition)
            if satisfy_pre_condition:

                print(string)
                stack.pop()
                for sub_state in delete:
                    input_notation.remove(sub_state)
                for sub_state in Add:
                    input_notation.add(sub_state)

        elif isinstance(top_stack[0], predicate):
            # Delete the predicate and perform the action related to it
            if top_stack[0] == predicate.on:
                stack.pop()
                x = top_stack[1]
                y = top_stack[2]
                stack.append((action.stack_up, x, y))
            elif top_stack[0] == predicate.on_table:
                stack.pop()
                x = top_stack[1]
                stack.append((action.put_down, x))
            elif top_stack[0] == predicate.clear:
                stack.pop()
                x = top_stack[1]
                for sub_state in input_notation:
                    if sub_state[0] == predicate.on and sub_state[2] == x:
                        stack.append(
                            (action.unstack, sub_state[1], sub_state[2]))
            elif top_stack[0] == predicate.holding:
                stack.pop()
                x = top_stack[1]
                for sub_state in input_notation:
                    if sub_state[0] == predicate.on.value and sub_state[1] == x:
                        stack.append((action.unstack, x, sub_state[2]))
                    elif sub_state[0] == predicate.on_table and sub_state[
                            1] == x:
                        stack.append((action.pick_up, x))
                        stack.append((predicate.clear, x))
                        break
            else:
                # This is armempty
                stack.pop()
                for sub_state in input_notation:
                    if sub_state[0] == predicate.holding:
                        stack.append((action.put_down, sub_state[1]))
        elif top_stack in input_notation:
            stack.pop()


def convert_to_state(list_state):
    """
        input_state:

        -----
        | a |             --->   [['b','a'],['c']]
        -----     -----
        | b |     | c |
        ---------------

    """
    """
        Output_state:

        ----- 
        | a |             ---> [['c','b','a']]
        -----
        | b |
        -----
        | c |
        ----------------
    """
    result = []

    for col in list_state:
        result.append((predicate.on_table, col[0]))
        temp = col[0]
        for block in col[1:]:
            result.append((predicate.on, block, temp))
            temp = block
        result.append((predicate.clear, col[-1]))
    result.append((predicate.armempty, ))
    return result


def take_input():
    result = []
    ncols = input("Enter the number of columns present : ")
    print(
        "Enter the string for each col with first block on the ground and each block sperated by space"
    )
    for _ in range(ncols):
        col = input().split()
        result.append(col)
    return convert_to_state(result)


if __name__ == '__main__':
    in_notation = convert_to_state(input_state)
    out_notation = convert_to_state(output_state)
    solve(in_notation, out_notation)
