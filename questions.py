import random
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Question:
    """Класс для представления вопроса"""
    text: str
    correct_answer: str
    wrong_answers: List[str]
    difficulty: int
    
    def get_shuffled_answers(self) -> List[str]:
        """Получить перемешанные варианты ответов"""
        answers = [self.correct_answer] + self.wrong_answers
        random.shuffle(answers)
        return answers
    
    def check_answer(self, answer: str) -> bool:
        """Проверить правильность ответа"""
        return answer.strip() == self.correct_answer.strip()

class QuestionBank:
    """Банк вопросов"""
    
    def __init__(self):
        self.questions = [
            # A1-A2 (2 вопроса)
            Question(
                text="Translate 'книга' into English:",
                correct_answer="book",
                wrong_answers=["magazine", "newspaper", "letter"],
                difficulty=1
            ),
            Question(
                text="Choose the correct form: She ___ to school every day.",
                correct_answer="goes",
                wrong_answers=["go", "going", "went"],
                difficulty=2
            ),
            
            # B1 (2 вопроса)
            Question(
                text="What is the meaning of the phrase 'to give up'?",
                correct_answer="to stop doing something",
                wrong_answers=["to start something", "to continue doing", "to finish quickly"],
                difficulty=3
            ),
            Question(
                text="Complete the sentence: She has been learning English ___ 2010.",
                correct_answer="since",
                wrong_answers=["for", "from", "in"],
                difficulty=3
            ),
            
            # B2 (2 вопроса)
            Question(
                text="Translate the sentence: 'Я би хотів покращити свою англійську'",
                correct_answer="I would like to improve my English",
                wrong_answers=["I will improve my English", "I want improve my English", "I like to improve my English"],
                difficulty=4
            ),
            Question(
                text="Complete the sentence: I wish I ___ harder for my exams last year.",
                correct_answer="had studied",
                wrong_answers=["studied", "have studied", "would study"],
                difficulty=4
            ),
            
            # C1-C2 (3 вопроса)
            Question(
                text="What does 'to beat around the bush' mean?",
                correct_answer="to avoid talking about something directly",
                wrong_answers=["to talk too much", "to speak very fast", "to be very direct"],
                difficulty=5
            ),
            Question(
                text="Translate: 'Чим більше я практикую, тим краще стаю'",
                correct_answer="The more I practice, the better I become",
                wrong_answers=["More I practice, better I become", "As more I practice, I become better", "When I practice more, I become better"],
                difficulty=5
            ),
            Question(
                text="Complete: If I ___ about the meeting earlier, I would have attended it.",
                correct_answer="had known",
                wrong_answers=["knew", "would know", "have known"],
                difficulty=5
            )
        ]
    
    def get_questions(self, count: int = 10) -> List[Question]:
        """Получить случайные вопросы с сохранением пропорций по сложности"""
        if count > len(self.questions):
            count = len(self.questions)
            
        # Группируем вопросы по сложности
        questions_by_difficulty = {}
        for q in self.questions:
            if q.difficulty not in questions_by_difficulty:
                questions_by_difficulty[q.difficulty] = []
            questions_by_difficulty[q.difficulty].append(q)
        
        # Определяем количество вопросов для каждого уровня сложности
        total_difficulties = sum(len(qs) for qs in questions_by_difficulty.values())
        selected_questions = []
        
        for difficulty, questions in questions_by_difficulty.items():
            # Пропорционально выбираем количество вопросов для каждой сложности
            n_questions = round(count * len(questions) / total_difficulties)
            if n_questions == 0 and questions:
                n_questions = 1
            selected_questions.extend(random.sample(questions, min(n_questions, len(questions))))
        
        # Если получилось меньше вопросов, чем нужно, добавляем случайные
        while len(selected_questions) < count:
            remaining = random.choice(self.questions)
            if remaining not in selected_questions:
                selected_questions.append(remaining)
        
        # Если получилось больше вопросов, чем нужно, убираем случайные
        while len(selected_questions) > count:
            selected_questions.pop(random.randrange(len(selected_questions)))
        
        # Перемешиваем итоговый список
        random.shuffle(selected_questions)
        return selected_questions

# Создаем глобальный экземпляр банка вопросов
question_bank = QuestionBank()
