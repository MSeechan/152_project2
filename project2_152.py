from abc import ABC, abstractmethod

# Professor class has a name and dictionary answer_key that has key=exam name (finals, midterm, etc.)
# and answers values (single answer and set answer) because each professor can have multiple assessments.
# Professor's responsibility is to grade incoming tests and send them back to the Exam interface.
class Professor:
    def __init__(self, pname):
        self.professor_name = pname
        self.answer_keys = {}
        self.questions= {}
        self.max_score = 0
        self.score = 0
        self.percent = 0
    
    # Answer key is a dictionary where the key is the exam name and the value is the a list of answers for that exam
    def set_answer_key(self, Exam, *answer_key):
        self.answer_keys[Exam.get_name()] = answer_key
    
    # Get total number of questions (single and in the set)
    def get_total_score(self, correct_answers):
        for i in range(0, len(correct_answers)):
            if type(correct_answers[i]) == list:
                for j in correct_answers[i]:
                    self.max_score+=1
            else: self.max_score+=1
        return self.max_score
    
    def notify(self, Exam):
        print('{} received a completed {}'.format(self.professor_name, Exam.get_name()))
    
    def grade_student_answers(self, Exam):
        self.max_score = 0
        correct_answers = (self.answer_keys[Exam.get_name()])
        self.get_total_score(correct_answers)
        for student in Exam.roster:
            self.score = 0
            student_answers = (student.get_student_answers())
            for i in range(0, len(correct_answers)):
                if type (correct_answers[i]) == list:
                    for student_ans, correct_ans in zip(student_answers[i], correct_answers[i]):
                        if  (student_ans == correct_ans):
                            self.score+=1
                elif (student_answers[i] == correct_answers[i]):
                    self.score+=1
            student.set_student_grade(self.score)
        print('{} finished grading all {}'.format((self.professor_name), Exam.get_name()))
        Exam.notify_grades_done()

# Students must be able to subscibe to exams, recieve exam questions, set and return answers to exam interface
# Students get a notification when exams are finished grading and they can view their grade via get_report()
class Student:
    def __init__(self, sname):
        self.student_name = sname
        self.student_answers = []
        self.student_grade = 0
    
    def get_student_name(self):
        return self.student_name
    
    def get_student_answers(self):
        return self.student_answers

    def set_student_grade(self, grade):
        self.student_grade = grade
    
    def get_student_grade(self):
        return self.student_grade

    def notify_recieved_test(self, Exam):
        print('{} recieved exam: {}'.format(self.student_name, Exam.get_name()))

    def sub(self, Exam):
        Exam.subscribe(self)
        print('{} subbed to {}'.format(self.student_name, Exam.get_name()))

    def take_exam(self, Exam, *student_answers):
        self.student_answers = student_answers
        Exam.notify_exam_done()
    
    def notify_grade(self, Exam):
        print('{} {} grades are ready'.format(self.student_name, Exam.get_name()))
    
    def get_report(self,Exam):
        Exam.create_report(self)
    

# Exam abstract class: at minimum, each Exam should be subscritable and must be able to notify all students/observers 
# when there is a change of state (when the questions are ready). ABC enforces inheritence and acts as an interface.
class Exam_Abstract(ABC):
    @abstractmethod
    def subscribe(self, student:Student): pass

    @abstractmethod
    def notify_students(self): pass

# Exam alerts keep roster of students and notifies all subscribed students when a test is ready. It routes student's 
# answers to the respective exam's professor. After grades are returned from a professor, reports are created for each 
# subscriber.
class Exam(Exam_Abstract):
    def __init__(self, name, professor):
        self.exam_name = name
        self.questions = []
        self.roster = []
        self.professor = professor
 
    def get_name(self):
        return self.exam_name

    def set_questions(self, questions):
        self.questions = questions

    def subscribe(self, Student):
        self.roster.append(Student)
      
    def notify_students(self):
        for student in self.roster:
            student.notify_recieved_test(self)
    
    def notify_exam_done(self):
        self.professor.notify(self)
    
    def notify_grades_done(self):
        for student in self.roster:
            student.notify_grade(self)
    
    def create_report(self, Student):
            student_answers=(Student.get_student_answers())
            correct_answers=(self.professor.answer_keys[self.get_name()])
            print( ' ---------------------------------------------')
            print(Student.student_name, self.get_name(), 'results:')
            for i in range(0, len(correct_answers)):
                if type (correct_answers[i]) == list:
                    for student_ans, correct_ans in zip(student_answers[i], correct_answers[i]):
                        if(student_ans==correct_ans):
                            print('\tCorrect!:',student_ans)
                        else:
                            print('\tIncorrect!: you:',student_ans, 'The correct answer:',correct_ans)
                            
                elif (student_answers[i] == correct_answers[i]):
                        print('\tCorrect!:',student_answers[i])
                else:
                        print('\tIncorrect!: you:',student_answers[i], 'The correct answer:',correct_answers[i])
            
            self.professor.percent = Student.get_student_grade()/self.professor.max_score*100
            print('',Student.student_name,'score', Student.get_student_grade(), '/', self.professor.max_score, '\t', self.professor.percent,'% ')
            print( ' ---------------------------------------------')


#--main--
# An Exam is created with a associated professor reference. Students can subscribe to the exam. Exam interface 
# hides the subscribers/roster from the professor and notifies all subscribers when the exam is ready to be taken. 
# It also notifies all subscribers when the professor is done grading. Each student can view their report.

# Scenario where two students are subscribed to a midterm
student1 = Student('malee')
student2 = Student('Javi')
cs_professor = Professor('Dr.Alex')
midterm = Exam('midterm', cs_professor)
student1.sub(midterm)
student2.sub(midterm)

midterm.set_questions({
  "Q-single" : {
    "What is the best pie flavor? \n1. apple \n2. cherry \n3. lemon \n4. peach \n5. blueberry" : 0,
  }, 
   "Q-single" : {
    "What is the best snack? \n1. cake \n2. pie \n3. brownie \n4. candy \n5. fruit" : 0,
  },
  "setA" : {
    "The answer is 1" : 0,
    "The other answer is 2" : 0,
    "But this answer is 5" : 0
  },
  "setB" : {
    "The answer is 1" : 0,
    "The answer is 2" : 0,
    "The answer is 3" : 0
  }
})

cs_professor.set_answer_key(midterm, 5, 2, [1, 2, 5], [1,2,3])
midterm.notify_students()
student1.take_exam(midterm, 1, 4, [3, 1, 2], [1,2,3])
student2.take_exam(midterm, 5, 2, [1, 2, 5], [3,2,3])
cs_professor.grade_student_answers(midterm)
student1.get_report(midterm)
student2.get_report(midterm)

# Scenario when one student is subscribed to a final
final = Exam('final', cs_professor)
student1.sub(final)

final.set_questions({
  "Q-single" : {
    "Is this a hard final? \n1. no \n2. yes \n3. maybe \n4. mostly \n5. it's okay" : 0,
  },
  "setA" : {
    "The answer is 5" : 0,
    "The answer is 4" : 0,
    "The answer is 3" : 0
  },
  "Q-single" : {
    "What grade should I get? \n1. A \n2. B \n3. C \n4. D \n5. E" : 0,
  }
})

cs_professor.set_answer_key(final, 2, [5,4,3],1)
final.notify_students()
student1.take_exam(final,2, [5,4,3],1)
cs_professor.grade_student_answers(final)
student1.get_report(final)






