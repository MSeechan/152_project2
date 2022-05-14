# Professor class has a name and dictionary answer_key that has key=exam name (finals, midterm, etc.)
# and answers values (single answer and set answer) because each professor can have multiple assessments.
# Professor's single responsibility is to grade incoming tests.
class Professor:
    def __init__(self, pname):
        self.professor_name = pname
        self.answer_keys = {}
        self.questions= {}
        self.max_score = 0
        self.score = 0
     
    def set_answer_key(self, answer_key, Exam):
        self.answer_keys[Exam.get_name()] = answer_key
    
    # Get total number of questions (single and in the set)
    def get_total_score(self, correct_answers):
        for i in range(0, len(correct_answers)):
            if type(correct_answers[i]) == list:
                for j in correct_answers[i]:
                    self.max_score+=1
            else: self.max_score+=1
        return self.max_score
       
    def grade_student_answers(self, Exam):
        student_answers=(Exam.get_student_answers())
        correct_answers=(self.answer_keys[Exam.get_name()])
        self.get_total_score(correct_answers)

        for i in range(0, len(correct_answers)):
            if type (correct_answers[i]) == list:
                for student_ans, correct_ans in zip(student_answers[i], correct_answers[i]):
                    if  (student_ans == correct_ans):
                        self.score+=1
            elif (student_answers[i] == correct_answers[i]):
                self.score+=1

        print('score', self.score,'/', self.max_score, '\t', self.score/self.max_score*100,'%')



# Students must be able to subscibe to exams, recieve exam questions, set and return answers to exam interface
class Student:
    def __init__(self, sname):
        self.student_name = sname

    def notify(self, Exam):
        print('{} recieved test: {}'.format(self.student_name, Exam.get_name()))

    def sub(self, Exam):
        Exam.subscribe(self)
        print('{} subbed to {}'.format(self.student_name, Exam.get_name()))

    def take_exam(self, answers, Exam):
        Exam.student_answers = answers
        Exam.notify_exam_done()

        
    
# Exam interface: at minimum, each Exam should be subscritable and must be able to notify all students/observers 
# when there is a change of state (when the questions are ready)
class Exam_Interface():
    def subscribe(self, student:Student): pass
    def notify_students(self): pass

# Exam alerts keep roster of students and notifies them all. It routes student's answers to the respective exam's professor.
# Sets are unordered so iteritive answer comparison is inaccurate. Exam questions are dictionaries consists of 1 question and a set to 
# keep questions and answers together.
class Exam(Exam_Interface):
    def __init__(self, name, professor):
        self.exam_name = name
        self.questions = []
        self.student_answers = []
        self.roster = []
        self.professor = professor
 
    def get_name(self):
        return self.exam_name

    def set_questions(self, questions):
        self.questions = questions

    def get_student_answers(self):
        return self.student_answers

    def subscribe(self, Student):
        self.roster.append(Student)

    def notify_students(self):
        for Student in self.roster:
            Student.notify(self)
    
    def notify_exam_done(self):
        self.professor.grade_student_answers(self)
          


# An Exam is created with a associated professor reference. Students can subscribe to the exam class. Exam class 
# hides the subscribers/roster from the professor and notifies all subscribers when the questions are set.

student1 = Student('malee')
cs_professor = Professor('Dr.Alex')
midterm = Exam('midterm', cs_professor)
student1.sub(midterm)

midterm.set_questions({
  "Q-single" : {
    "What is the best pie flavor? \n1. apple \n2. cherry \n3. lemon \n4. peach \n5. blueberry" : 0,
  },
  "Q-set" : {
    "The answer is 1" : 0 ,
    "The other answer is 2" : 0,
    "But this answer is 5" : 0
  }
})

cs_professor.set_answer_key([5, 2, [1, 2, 5]], midterm)

midterm.notify_students()

student1.take_exam([5, 9, [3, 0, 5]], midterm)




