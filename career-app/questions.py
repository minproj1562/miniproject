APTITUDE_QUESTIONS = {
    "Mathematics": {
        "easy": [
            {
                "id": "M1-E",
                "type": "numerical",
                "text": "Solve: 15 + 8 × 3 ÷ 4",
                "options": ["21", "18.5", "19.5", "20.25"],
                "correct": 2,
                "time_limit": 60,
                "irt_params": {
                    "difficulty": -1.2,
                    "discrimination": 0.8
                }
            }
        ],
        "moderate": [
            {
                "id": "M2-M",
                "type": "algebra",
                "text": "If x + y = 15 and 2x - y = 6, what is the value of x?",
                "options": ["7", "8", "9", "10"],
                "correct": 0,
                "time_limit": 90,
                "irt_params": {
                    "difficulty": 0.5,
                    "discrimination": 1.2
                }
            }
        ],
        "hard": [
            {
                "id": "M3-H",
                "type": "calculus",
                "text": "What is the derivative of f(x) = 3x² + 2eˣ - ln(x)?",
                "options": ["6x + 2eˣ - 1/x", "6x + 2eˣ + 1/x", "3x + 2eˣ - 1/x²", "6x + eˣ - 1/x"],
                "correct": 0,
                "time_limit": 120,
                "irt_params": {
                    "difficulty": 1.8,
                    "discrimination": 1.5
                }
            }
        ]
    },
    "Logical Reasoning": {
        "easy": [
            {
                "id": "LR1-E",
                "type": "pattern",
                "text": "Complete the sequence: A, C, E, G, ___",
                "options": ["H", "I", "J", "K"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {
                    "difficulty": -1.0,
                    "discrimination": 0.9
                }
            }
        ],
        "moderate": [
            {
                "id": "LR2-M",
                "type": "deductive",
                "text": "All managers are leaders. Some leaders are visionary. Therefore:",
                "options": [
                    "All managers are visionary",
                    "Some managers may be visionary",
                    "No managers are visionary",
                    "Visionary people cannot be managers"
                ],
                "correct": 1,
                "time_limit": 75,
                "irt_params": {
                    "difficulty": 0.7,
                    "discrimination": 1.1
                }
            }
        ],
        "hard": [
            {
                "id": "LR3-H",
                "type": "analytical",
                "text": "If 3★5 = 16, 4★7 = 30, then 5★9 = ___",
                "options": ["44", "46", "48", "50"],
                "correct": 1,
                "time_params": {
                    "difficulty": 2.0,
                    "discrimination": 1.4
                }
            }
        ]
    },
    "Verbal Ability": {
        "easy": [
            {
                "id": "VA1-E",
                "type": "vocabulary",
                "text": "Select the antonym of EPHEMERAL:",
                "options": ["Transient", "Enduring", "Fleeting", "Momentary"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {
                    "difficulty": -0.8,
                    "discrimination": 0.7
                }
            }
        ],
        "moderate": [
            {
                "id": "VA2-M",
                "type": "comprehension",
                "text": "'The company's pecuniary situation was precarious.' What does 'pecuniary' mean?",
                "options": ["Legal", "Financial", "Ethical", "Structural"],
                "correct": 1,
                "time_limit": 60,
                "irt_params": {
                    "difficulty": 0.6,
                    "discrimination": 1.0
                }
            }
        ],
        "hard": [
            {
                "id": "VA3-H",
                "type": "critical_reasoning",
                "text": "Which statement weakens the argument: 'Remote work increases productivity because employees save commute time'?",
                "options": [
                    "Commute time averages 45 minutes daily",
                    "Home distractions reduce focused work hours",
                    "Companies report higher profits with remote teams",
                    "Video conferencing tools improve collaboration"
                ],
                "correct": 1,
                "irt_params": {
                    "difficulty": 1.5,
                    "discrimination": 1.3
                }
            }
        ]
    }
}

ADAPTIVE_TEST_SETTINGS = {
    "initial_difficulty": "easy",
    "ability_estimation": "bayesian",
    "scaling_factors": {
        "correct_answer": +0.3,
        "wrong_answer": -0.2,
        "time_penalty": -0.1  # per 10% over time limit
    },
    "proficiency_levels": {
        "Mathematics": {"thresholds": [40, 70]},  # 0-40: easy, 40-70: moderate, 70+: hard
        "Logical Reasoning": {"thresholds": [45, 75]},
        "Verbal Ability": {"thresholds": [35, 65]}
    }
}
# Big Five Personality Inventory
# Updated Big Five Inventory with validated items
PERSONALITY_QUESTIONS = [
    # Openness (10 items)
    {
        "id": 1,
        "trait": "O",
        "text": "I enjoy trying new and foreign foods",
        "direction": True,
        "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
        "source": "NEO-PI-R"
    },
    {
        "id": 2,
        "trait": "O",
        "text": "I prefer to stick with things I know rather than try new experiences",
        "direction": False,
        "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
        "source": "IPIP"
    },
    # Additional validated items
    {
        "id": 3,
        "trait": "O",
        "text": "I have a vivid imagination",
        "direction": True,
        "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
        "source": "NEO-PI-R"
    },

    # Conscientiousness (10 items)
    {
        "id": 11,
        "trait": "C",
        "text": "I pay attention to details",
        "direction": True,
        "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
        "source": "NEO-PI-R"
    },
    {
        "id": 12,
        "trait": "C",
        "text": "I often forget to put things back in their proper place",
        "direction": False,
        "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
        "source": "IPIP"
    },
    
    # Continue with 8 items per trait following same pattern...
]

# Add missing time_limit parameter for LR3-H
APTITUDE_QUESTIONS["Logical Reasoning"]["hard"][0]["time_limit"] = 150
APTITUDE_QUESTIONS["Logical Reasoning"]["hard"][0]["irt_params"] = {  # Fix typo
    "difficulty": 2.0, 
    "discrimination": 1.4
}

CAREER_MAPPING = {
    "Data Analyst": {
        "requirements": {
            "aptitude": {
                "Mathematics": 75,
                "Logical Reasoning": 80,
                "Verbal Ability": 65
            },
            "personality": {
                "C": 70,  # Conscientiousness
                "O": 65,  # Openness
                "N": 40   # Neuroticism (lower better)
            }
        },
        "description": "Requires strong numerical analysis and pattern recognition skills",
        "development_path": [...]
    }
}