# Write your code here

class ToDoList(object):
    activities = ('Do yoga', 'Make breakfast', 'Learn basics of SQL', 'Learn what is ORM',)
    def __init__(self):
        pass

    print('Today:')
    for k, v in enumerate(activities, start=1):
        print(f'{k}) {v}')


if __name__ == '__main__':
    ToDoList()