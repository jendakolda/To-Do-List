# Write your code here

class ToDoList(object):
    def __init__(self):
        self.activities = ('Do yoga', 'Make breakfast', 'Learn basics of SQL', 'Learn what is ORM')

    def main(self):
        print('Today:')
        for k, v in enumerate(self.activities, start=1):
            print(f'{k}) {v}')


if __name__ == '__main__':
    ToDoList().main()