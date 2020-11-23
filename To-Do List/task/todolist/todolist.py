# Write your code here
from datetime import datetime, timedelta

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

    def __init__(self):
        engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def menu(self):
        menu_items = {'1': 'Today\'s tasks',
                      '2': 'Week\'s tasks',
                      '3': 'All tasks',
                      '4': 'Missed tasks',
                      '5': 'Add task',
                      '6': 'Delete task',
                      '0': 'Exit'}
        while True:
            for k, v in menu_items.items():
                print(f'{k}) {v}')
            choice = int(input())
            if choice == 1:
                self.show_tasks('Today')
            elif choice == 2:
                self.show_tasks('Week')
            elif choice == 3:
                self.show_tasks()
            elif choice == 4:
                self.show_tasks('Missed')
            elif choice == 5:
                self.add_task()
            elif choice == 6:
                self.delete_task()
            elif choice == 0:
                print('Bye!')
                exit()
            else:
                print('Incorrect input, try again.')

    def add_task(self):
        new_row = Table(task=input('Enter task\n'),
                        deadline=datetime.strptime(input('Enter deadline\n'), '%Y-%m-%d'))
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added\n')

    def delete_task(self):
        print('Choose the number of the task you want to delete:')
        self.show_tasks()
        while True:
            try:
                self.session.delete(self.session.query(Table).order_by(Table.deadline).all()[int(input()) - 1])
                break
            except IndexError:
                print('Invalid task ID.')

        self.session.commit()
        print('The task has been deleted!')

    def show_tasks(self, interval='all'):

        if interval == 'all':
            rows = self.session.query(Table).order_by(Table.deadline).all()
            if rows:
                for row in rows:
                    print(f'{row.id}. {row.task}. {row.deadline.strftime("%#d %b")}')
                print('\n')
            else:
                print('Nothing to do!\n')

        elif interval == 'Today':
            print(interval, datetime.today().strftime("%#d %b"))
            rows = self.session.query(Table).filter(Table.deadline == datetime.today().date()).all()
            if rows:
                for row in rows:
                    print(f'{row.id}. {row.task}')
                print('\n')
            else:
                print('Nothing to do!\n')

        elif interval == 'Week':
            days = [datetime.today().date() + timedelta(days=i) for i in range(7)]
            for day in days:
                rows = self.session.query(Table).filter(Table.deadline == day).all()
                print(day.strftime('%A %#d %b') + ':')
                if rows:
                    for row in rows:
                        print(f'{row.id}. {row.task}')
                    print('\n')
                else:
                    print('Nothing to do!\n')

        elif interval == 'Missed':
            print(interval, 'tasks')
            rows = self.session.query(Table).filter(Table.deadline <= datetime.today().date()).all()
            if rows:
                for row in rows:
                    print(f'{row.id}. {row.task}. {row.deadline.strftime("%#d %b")}')
                print('\n')
            else:
                print('Nothing is missed!\n')


if __name__ == '__main__':
    ToDoList().menu()
