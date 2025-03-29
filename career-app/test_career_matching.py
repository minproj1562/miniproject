# test_career_matching.py
import pytest
from app import calculate_match
from questions import CAREER_MAPPING

def test_career_calculation():
    user_scores = {
        'personality': {'Openness': 80, 'Conscientiousness': 70},
        'aptitude': {'logical': 85, 'numerical': 90},
        'skill_gap': {'score': 75}
    }
    
    career = CAREER_MAPPING['Software Developer']
    score = calculate_match(user_scores, career)
    
    assert 70 <= score <= 95
    assert isinstance(score, float)