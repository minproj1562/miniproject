# data/aptitude_questions.py
CATEGORIES = {
    "Gf": "Fluid Intelligence",
    "Gc": "Crystallized Intelligence",
    "Gv": "Visual Processing",
    "Gs": "Processing Speed",
    "Gwm": "Working Memory"
}

WEIGHTS = {
    "Gf": 0.30,
    "Gc": 0.25,
    "Gv": 0.20,
    "Gs": 0.15,
    "Gwm": 0.10
}

TIME_LIMITS = {
    "Gf": 300,
    "Gc": 300,
    "Gv": 420,
    "Gs": 360,
    "Gwm": 300
}

CAREER_MAPPINGS = {
    "Software Engineer": {
        "cognitive": ["Gf", "Gwm"],
        "personality": ["C", "O"],
        "score_range": [70, 100],
        "personality_threshold": 65
    },
    "Data Scientist": {
        "cognitive": ["Gf", "Gc"],
        "personality": ["O", "C"],
        "score_range": [75, 100],
        "personality_threshold": 60
    }
}

CAREER_FALLBACK = {
    "Software Engineer": {
        "description": "Develops software applications and systems...",
        "salary": "$95,000-$150,000",
        "skills": ["Programming", "Problem Solving", "Algorithm Design"]
    }
}

QUESTIONS = [
    {
        "id": 1,
        "category": "Gf",
        "text": "What comes next in the sequence: 2, 4, 8, 16...?",
        "options": ["24", "32", "64", "128"],
        "correct": "32",
        "difficulty": 2,
        "time_limit": 45
    },
    {
        "id": 2,
        "category": "Gf",
        "text": "Complete the pattern: △◯△△◯△△△◯_",
        "options": ["△", "◯", "△△", "△△△◯"],
        "correct": "△△△◯",
        "difficulty": 3,
        "time_limit": 60
    }
]