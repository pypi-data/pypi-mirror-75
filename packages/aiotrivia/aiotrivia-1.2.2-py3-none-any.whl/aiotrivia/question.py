"""
-*- coding: utf-8 -*-
The files containing question data
"""

from html import unescape
from random import sample


class Question:
    """
    The question type returned when getting questions
    """
    __slots__ = ('category', 'type', 'question', 'answer', 'incorrect_answers', 'difficulty')

    def __init__(self, data: dict):
        self.category = data.get('category')
        self.type = data.get('type')
        self.question = unescape(str(data.get('question')))
        self.answer = unescape(str(data.get('correct_answer')))
        self.incorrect_answers: list = [unescape(answer) for answer in data.get('incorrect_answers')]
        self.difficulty = data.get('difficulty')

    def __repr__(self):
        return f"<aiotrivia.question.Question: question={self.question}, category={self.category}, type={self.type}>"

    @property
    def responses(self):
        responses = self.incorrect_answers + [self.answer]
        return sample(responses, len(responses))

    def add_incorrect_answers(self, *args):
        for item in args:
            self.incorrect_answers.append(item)
