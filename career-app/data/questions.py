# Cognitive Ability Assessment (Aptitude Test)
APTITUDE_QUESTIONS = [
    {
        "id": 1,
        "category": "Gf",
        "text": "What comes next in the sequence: 2, 4, 8, 16...?",
        "options": ["24", "32", "64", "128"],
        "weight": 1.2,
        "time_limit": 45
    },
    # 5 more Gf questions with progressive difficulty
    
    # Crystallized Intelligence (Gc) - 6 questions
    {
        "id": 7, 
        "category": "Gc",
        "text": "What is the antonym of 'ephemeral'?",
        "options": ["Permanent", "Fleeting", "Temporary", "Momentary"],
        "weight": 1.1,
        "time_limit": 45
    },
    # 5 more Gc questions testing vocabulary and general knowledge
    
    # Quantitative Reasoning (Gq) - 6 questions
    {
        "id": 13,
        "category": "Gq",
        "text": "If 3x + 2y = 12 and x - y = 1, what is x?",
        "options": ["2", "3", "4", "5"],
        "weight": 1.2,
        "time_limit": 90
    },
    # 5 more Gq questions with algebraic and arithmetic problems
    
    # Visual Processing (Gv) - 6 questions
    {
        "id": 19,
        "category": "Gv",
        "text": "Which 3D shape matches the unfolded net?",
        "options": ["Cube", "Pyramid", "Cylinder", "Dodecahedron"],
        "weight": 1.15,
        "time_limit": 75
    },
    # 5 more Gv questions with spatial rotation/visualization
    
    # Working Memory (Gwm) - 6 questions
    {
        "id": 25,
        "category": "Gwm",
        "text": "Remember these numbers: 7-3-9. After solving: 2+5=?, what were the numbers?",
        "options": ["7-3-9", "7-2-9", "3-7-9", "9-3-7"],
        "weight": 1.25,
        "time_limit": 60
    },
    # 5 more Gwm questions with dual-task challenges

    # Add 29 more questions covering:
    # - Fluid Intelligence (Gf)
    # - Crystallized Intelligence (Gc)
    # - Quantitative Reasoning (Gq)
    # - Visual Processing (Gv)
    # - Working Memory (Gwm)
]

# Big Five Personality Inventory
PERSONALITY_QUESTIONS = [
    {
        "id": 1,
        "trait": "O",
        "text": "I enjoy trying new and foreign foods",
        "direction": True,  # Positive scoring
        "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    },
    {
        "id": 2,
        "trait": "O",
        "text": "I prefer routine over new experiences",
        "direction": False  # Reverse scored
    },
    # 8 more O questions
    
    # Conscientiousness (C) - 10 questions
    {
        "id": 11,
        "trait": "C", 
        "text": "I complete tasks immediately without procrastinating",
        "direction": True
    },
    # 9 more C questions
    
    # Extraversion (E) - 10 questions
    {
        "id": 21,
        "trait": "E",
        "text": "I feel energized when interacting with large groups",
        "direction": True
    },
    # 9 more E questions
    
    # Agreeableness (A) - 10 questions
    {
        "id": 31,
        "trait": "A",
        "text": "I often compromise to maintain harmony in relationships",
        "direction": True
    },
    # 9 more A questions
    
    # Neuroticism (N) - 10 questions
    {
        "id": 41,
        "trait": "N",
        "text": "I frequently worry about potential problems",
        "direction": True
    },
    # 9 more N questions
]

# Career Mapping based on Cognitive and Personality Scores
CAREER_MAPPING = {
    "Software Engineer": {
        "cognitive": {"Gf": 80, "Gwm": 75},
        "personality": {"C": 70, "O": 65},
        "description": "Requires strong problem-solving and attention to detail"
    },
     "Clinical Psychologist": {
        "cognitive": {"Gc": 85, "Gwm": 75},
        "personality": {"A": 85, "E": 65, "N": 40},
        "description": "Needs empathy and emotional stability"
    },
    "Graphic Designer": {
        "cognitive": {"Gv": 90, "Gf": 75},
        "personality": {"O": 80, "E": 60},
        "description": "Requires creativity and visual intelligence"
    },
    "Air Traffic Controller": {
        "cognitive": {"Gwm": 95, "Gv": 85},
        "personality": {"C": 90, "N": 30},
        "description": "Needs high working memory and stress tolerance"
    },
    "Elementary School Teacher": {
        "cognitive": {"Gc": 80, "Gf": 70},
        "personality": {"A": 85, "E": 75},
        "description": "Requires patience and social intelligence"
    }

}