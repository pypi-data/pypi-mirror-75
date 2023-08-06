"""
-*- coding: utf-8 -*-
Async Wrapper for the OpenTDBAPI
"""

from random import choice
from typing import List
from aiohttp import ClientSession

from aiotrivia.exceptions import *
from aiotrivia.question import Question

CATEGORIES = {
    9: "General Knowledge",
    10: "Entertainment: Books",
    11: "Entertainment: Film",
    12: "Entertainment: Music",
    13: "Entertainment: Musicals & Theatres",
    14: "Entertainment: Television",
    15: "Entertainment: Video Games",
    16: "Entertainment: Board Games",
    17: "Science & Nature",
    18: "Science: Computers",
    19: "Science: Mathematics",
    20: "Mythology",
    21: "Sports",
    22: "Geography",
    23: "History",
    24: "Politics",
    25: "Art",
    26: "Celebrities",
    27: "Animals",
    28: "Vehicles",
    29: "Entertainment: Comics",
    30: "Science: Gadgets",
    31: "Entertainment: Japanese Anime & Manga",
    32: "Entertainment: Cartoon & Animations"
}


class TriviaClient:
    """
    The main trivia client used to get questions from the API
    """
    url = 'https://opentdb.com/api.php'

    def __repr__(self):
        return f"aiotrivia.client.TriviaClient"

    async def get_random_question(self, difficulty=choice(['easy', 'medium', 'hard'])) -> Question:
        difficulties = ('easy', 'medium', 'hard')
        if difficulty not in difficulties:
            raise InvalidDifficulty("%s is not a valid difficulty!" % difficulty)
        async with ClientSession() as cs:
            async with cs.get(self.url, params={"amount": 1, "difficulty": difficulty}) as r:
                data = await r.json()
            await cs.close()
        return Question(data=data.get('results')[0])

    async def get_specific_question(self, **kwargs) -> List[Question]:
        valid_kwargs = ['amount', 'type', 'category', 'difficulty']
        params = {}
        questions = []
        if any(item not in valid_kwargs for item in kwargs.keys()):
            raise InvalidKwarg(
                "You have passed an invalid keyword argument! Valid keyword arguments include: %s" % ', '.join(
                    valid_kwargs))
        amount, type, category, difficulty = kwargs.get('amount', 1), kwargs.get('type'), kwargs.get(
            'category'), kwargs.get('difficulty')
        if amount:
            if not isinstance(amount, int) or not 0 < amount < 50:
                raise InvalidAmount()
            else:
                params['amount'] = amount
        if type:
            if type.lower() not in ['multiple', 'boolean']:
                raise InvalidType()
            else:
                params['type'] = type
        if category:
            if not isinstance(category, int) or category not in CATEGORIES:
                raise InvalidCategory()
            else:
                params['category'] = category
        if difficulty:
            if difficulty.lower() not in ['easy', 'medium', 'hard']:
                raise InvalidDifficulty()
            else:
                params['difficulty'] = difficulty
        async with ClientSession() as cs:
            async with cs.get(self.url, params=params) as r:
                data = await r.json()
            await cs.close()
            if data['response_code'] == 1:
                raise ResponseError()
            for item in data.get('results'):
                questions.append(Question(data=item))
        return questions
