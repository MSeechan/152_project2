from abc import ABC, abstractmethod

# Professor's responsibility is to grade incoming tests and send them back to the Exam interface.
class Professor:
    def __init__(self, pname):
        self.professor_name = pname
        self.questions= {}
        self.score = 0
        self.percent = 0

    def notify(self, Exam):
        print('{} received a completed {}'.format(self.professor_name, Exam.get_name()))
    
    def grade_student_answers(self, Exam):
        for student in Exam.roster:
            self.score = 0
            student_answers = (student.get_student_answers())
        
            for i in range(0,len(Exam.question_list)):
                if type(Exam.question_list[i].question) is list:
                    for j in range(0,len(Exam.question_list[i].question)):
                        if (student_answers[i][j] == Exam.question_list[i].question[j].answer):
                             self.score+=1
                elif student_answers[i] == (Exam.question_list[i].answer):  
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

# Question objects are created and can be left as is or subsequently added into a set for composition
class Question_Abstract(ABC):
    @abstractmethod
    def create_question(self): pass
    @abstractmethod
    def get_question(self): pass

class SingleQuestion(Question_Abstract):
    def __init__(self):
        self.question = ""
        self.answer = 0

    def create_question(self, question, answer):
        self.question = question
        if (answer in range(1,6)):
            self.answer = answer
        else:    
            print("Please provide answer as 1-5")
        
    def get_question(self):
        return print('question',self.question)
    
    def get_answer(self):
        return print('answer',self.answer)
        
class SetQuestions(Question_Abstract):
    def __init__(self):
        self.question = []
        self.question_qty = 0

    def create_question(self, question):
        self.question.append(question)
        self.question_qty += 1
    
    def get_question(self):
        return print('question',self.question)

# Exam abstract class: at minimum, each Exam should be subscritable and must be able to notify all students/observers 
# when there is a change of state (when the questions are ready). ABC enforces inheritence and acts as an interface.
class Exam_Abstract(ABC):
    @abstractmethod
    def subscribe(self, student:Student): pass
    @abstractmethod
    def notify_students(self): pass

# Exam alerts keep roster of students and notifies all subscribed students when a test is ready. Question objects are 
# saved to the Exam's question_list for composition. Student's answers are routed to the respective exam's professor. 
# After gradeing is done, reports can be created for each subscriber.

class Exam(Exam_Abstract):
    def __init__(self, name, professor):
        self.exam_name = name
        self.question_list = []
        self.roster = []
        self.professor = professor
        self.max_score = 0
 
    def get_name(self):
        return self.exam_name

    def set_questions(self, questions):
        self.question_list.append(questions)

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
    
    def get_max_score(self):
        self.max_score = 0
        for question in self.question_list:
            if type(question.question) is list:
                self.max_score += len(question.question)
            else: 
                self.max_score +=1
        return self.max_score
  
    def create_report(self, Student):
            student_answers=(Student.get_student_answers())

            print( Student.get_student_name(),'Report---------------------------------------------')
            for i in range(0,len(self.question_list)):
                if type(self.question_list[i].question) is list:
                    for j in range(0,len(self.question_list[i].question)):
                        if (student_answers[i][j] == self.question_list[i].question[j].answer):
                               print('\tCorrect!:',student_answers[i][j])
                        else:
                                print('\tIncorrect! you:',student_answers[i][j], ', correct answer:',self.question_list[i].question[j].answer)
                elif (student_answers[i] == self.question_list[i].answer):
                    print('\tCorrect!:',student_answers[i])
                else:
                    print('\tIncorrect!: you:',student_answers[i], 'The correct answer:',self.question_list[i].answer)

            self.professor.percent = Student.get_student_grade()/self.get_max_score()*100
            print('',Student.get_student_name(),'score', Student.get_student_grade(), '/', self.max_score, '\t', self.professor.percent,'% ')
            
           
#--main--
# An Exam is created withcreate_question a associated professor reference. Students can subscribe to the exam. Exam interface 
# hides the subscribers/roster from the professor and notifies all subscribers when the exam is ready to be taken. 
# It also notifies all subscribers when the professor is done grading. Each student can get their report.

#Scenario where two students are subscribed to a midterm -- first create objects
student1 = Student('malee')
student2 = Student('Javi')
cs_professor = Professor('Dr.Alex')
midterm = Exam('midterm', cs_professor)

#students subcribe to an exam
student1.sub(midterm)
student2.sub(midterm)

#Setup midterm questions
question1 = SingleQuestion()
question1.create_question("Q: Am I revising this?: \n1) Yes \t2) No \t3) Maybe \t4) Just turn it in \t5) I'll just try", 1)
midterm.set_questions(question1)

#Set of single questions
question2 = SingleQuestion()
question2.create_question("Q: The answer is 4", 4)
question3 = SingleQuestion()
question3.create_question("Q: The other answer is 2", 2)
question4 = SingleQuestion()
question4.create_question("Q: But this answer is 5", 5)

question_set1 = SetQuestions()
question_set1.create_question(question2)
question_set1.create_question(question3)
question_set1.create_question(question4)
midterm.set_questions(question_set1)

student1.take_exam(midterm,2,(4,1,5))
student2.take_exam(midterm,1,(4,1,5))
cs_professor.grade_student_answers(midterm)
student1.get_report(midterm)
student2.get_report(midterm)


