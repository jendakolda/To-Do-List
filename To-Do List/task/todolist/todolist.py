# Write your code here
from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class ToDoList(object):
    activities = ('Do yoga', 'Make breakfast', 'Learn basics of SQL', 'Learn what is ORM',)

    def __init__(self):
        engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def menu(self):
        menu_items = {'1': 'Today\'s tasks', '2': 'Add task', '0': 'Exit'}

        while True:
            for k, v in menu_items.items():
                print(f'{k}) {v}')
            choice = int(input())
            if choice == 1:
                self.todays_tasks()
            elif choice == 2:
                self.add_task()
            elif choice == 0:
                print('Bye')
                exit()
            else:
                print('Incorrect input, try again.')

    def add_task(self):
        new_row = Table(task=input('Enter task\n'),
                        deadline=datetime.strptime('01-24-2020', '%m-%d-%Y').today())
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added\n')

    def todays_tasks(self):
        print('Today:')
        rows = self.session.query(Table).all()
        if rows:
            for row in rows:
                print(f'{row.id}. {row.task}')
            print('\n')
        else:
            print('Nothing to do!\n')


if __name__ == '__main__':
    ToDoList().menu()
