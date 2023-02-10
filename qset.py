from dictionary import DICTIONARY

class Qset:
    def __init__(self, question, answer, id = 0):
        self.question = question
        self.answer = answer
        self.id = id

    def voice_question(self):
        self.temp_q = self.question.split()
        for i in self.temp_q:
            if i in DICTIONARY:
                self.question = self.question.replace(i, DICTIONARY[i])
        return self.question

    def voice_answer(self):
        self.temp_a = self.answer.split()
        for i in self.temp_a:
            if i in DICTIONARY:
                self.answer = self.answer.replace(i, DICTIONARY[i])
        return self.answer

