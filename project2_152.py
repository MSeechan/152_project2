from abc import abstractmethod
from typing import List

class Professor:
    def __init__(self, pname):
        self.professor_name = pname
        self.answer_key = []
    



class Student:
    def __init__(self, sname):
        self.student_name = sname
        self.student_answers = []
    def notify(self, Exam):
        print('{} recieved test: {}'.format(self.student_name, Exam.get_name()))
    def sub(self, Exam):
        Exam.subscribe(self)
        print('{} subbed to {}'.format(self.student_name, Exam.get_name()))
    def take_exam(self, single, set):
        self.student_answers = [single, set]

class Exam_Interface():
    @abstractmethod
    def __init__(self, name):pass
    @abstractmethod
    def subscribe(self, student:Student): pass
    @abstractmethod
    def notify_students(self): pass

class Exam(Exam_Interface):
    def __init__(self, name):
        self.exam_name = name
        self.roster = []
    
    def get_name(self):
        return self.exam_name

    def set_questions(self, single, set):
        self.question = single 
        self.question_set = set

    def subscribe(self, Student):
        self.roster.append(Student)

    def notify_students(self):
        for Student in self.roster:
            Student.notify(self)
    


midterm = Exam('midterm')
finals = Exam('finals')

midterm.set_questions("What is the best pie flavor? 1)apple 2)cherry 3)lemon 4)peach 5)blueberry", {"select #1", "select #2"})

malee = Student('malee')
malee.take_exam(1, {1,2})
# mike = Student('mike')

# malee.sub(midterm)
# mike.sub(finals)

# midterm.notify_students()
# finals.notify_students()

