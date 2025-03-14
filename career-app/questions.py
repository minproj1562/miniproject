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
                "time_limit": 150,
                "irt_params": {
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

PERSONALITY_QUESTIONS = [
    # Openness to Experience (O)
    {
        "id": 1,
        "trait": "O",
        "text": "I enjoy hearing new ideas",
        "direction": True,
        "source": "NEO-PI-R",
        "reliability": 0.87,
        "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    },
    {
        "id": 2,
        "trait": "O",
        "text": "I avoid philosophical discussions",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.85
    },
    {
        "id": 2,
        "trait": "O",
        "text": "I avoid philosophical discussions",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.85
    },

    # Conscientiousness (C)
    {
        "id": 11,
        "trait": "C",
        "text": "I pay attention to details",
        "direction": True,
        "source": "BFI-2",
        "reliability": 0.89
    },
    {
        "id": 12,
        "trait": "C",
        "text": "I often forget to put things back in their proper place",
        "direction": False,
        "source": "NEO-PI-R",
        "reliability": 0.83
    },

    # Extraversion (E)
    {
        "id": 21,
        "trait": "E",
        "text": "I feel comfortable around people",
        "direction": True,
        "source": "BFI-2",
        "reliability": 0.88
    },
    {
        "id": 22,
        "trait": "E",
        "text": "I prefer quiet evenings at home to parties",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.84
    },

    # Agreeableness (A)
    {
        "id": 31,
        "trait": "A",
        "text": "I sympathize with others' feelings",
        "direction": True,
        "source": "NEO-PI-R",
        "reliability": 0.86
    },
    {
        "id": 32,
        "trait": "A",
        "text": "I often argue with authority figures",
        "direction": False,
        "source": "BFI-2",
        "reliability": 0.82
    },

    # Neuroticism (N)
    {
        "id": 41,
        "trait": "N",
        "text": "I often feel tense or anxious",
        "direction": True,
        "source": "IPIP-NEO",
        "reliability": 0.90
    },
    {
        "id": 42,
        "trait": "N",
        "text": "I remain calm under pressure",
        "direction": False,
        "source": "NEO-PI-R",
        "reliability": 0.84
    },
{
        "id": 43,
        "trait": "O",
        "text": "I enjoy hearing new ideas",
        "direction": True,
        "source": "NEO-PI-R",
        "reliability": 0.87
    },
    {
        "id": 44,
        "trait": "O",
        "text": "I avoid philosophical discussions",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.85
    },
    {
        "id": 45,
        "trait": "O",
        "text": "I have a vivid imagination",
        "direction": True,
        "source": "BFI-2",
        "reliability": 0.83
    },
    {
        "id": 46,
        "trait": "O",
        "text": "I prefer routine over variety",
        "direction": False,
        "source": "NEO-PI-R",
        "reliability": 0.84
    },
    {
        "id": 47,
        "trait": "O",
        "text": "I appreciate abstract art",
        "direction": True,
        "source": "IPIP-NEO",
        "reliability": 0.81
    },
    {
        "id": 48,
        "trait": "O",
        "text": "I dislike complex theoretical concepts",
        "direction": False,
        "source": "BFI-2",
        "reliability": 0.82
    },
    {
        "id": 49,
        "trait": "O",
        "text": "I enjoy trying new cultural experiences",
        "direction": True,
        "source": "NEO-PI-R",
        "reliability": 0.86
    },
    {
        "id": 50,
        "trait": "O",
        "text": "I prefer practical over creative tasks",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.84
    },

    # Conscientiousness (C) - 8 items
    {
        "id": 51,
        "trait": "C",
        "text": "I pay attention to details",
        "direction": True,
        "source": "BFI-2",
        "reliability": 0.89
    },
    {
        "id": 52,
        "trait": "C",
        "text": "I often forget to put things back in their proper place",
        "direction": False,
        "source": "NEO-PI-R",
        "reliability": 0.83
    },
    {
        "id": 53,
        "trait": "C",
        "text": "I complete tasks thoroughly",
        "direction": True,
        "source": "IPIP-NEO",
        "reliability": 0.85
    },
    {
        "id": 54,
        "trait": "C",
        "text": "I often procrastinate important tasks",
        "direction": False,
        "source": "BFI-2",
        "reliability": 0.82
    },
    {
        "id": 55,
        "trait": "C",
        "text": "I follow through on my commitments",
        "direction": True,
        "source": "NEO-PI-R",
        "reliability": 0.86
    },
    {
        "id": 56,
        "trait": "C",
        "text": "I struggle with time management",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.84
    },
    {
        "id": 57,
        "trait": "C",
        "text": "I keep my living space organized",
        "direction": True,
        "source": "BFI-2",
        "reliability": 0.83
    },
    {
        "id": 58,
        "trait": "C",
        "text": "I often make careless mistakes",
        "direction": False,
        "source": "NEO-PI-R",
        "reliability": 0.81
    },

    # Extraversion (E) - 8 items
    {
        "id": 59,
        "trait": "E",
        "text": "I feel comfortable around people",
        "direction": True,
        "source": "BFI-2",
        "reliability": 0.88
    },
    {
        "id": 60,
        "trait": "E",
        "text": "I prefer quiet evenings at home to parties",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.84
    },
    {
        "id": 62,
        "trait": "E",
        "text": "I am the life of the party",
        "direction": True,
        "source": "NEO-PI-R",
        "reliability": 0.83
    },
    {
        "id": 63,
        "trait": "E",
        "text": "Large social gatherings drain my energy",
        "direction": False,
        "source": "BFI-2",
        "reliability": 0.85
    },
    {
        "id": 64,
        "trait": "E",
        "text": "I enjoy being the center of attention",
        "direction": True,
        "source": "IPIP-NEO",
        "reliability": 0.82
    },
    {
        "id": 65,
        "trait": "E",
        "text": "I find it hard to start conversations",
        "direction": False,
        "source": "NEO-PI-R",
        "reliability": 0.84
    },
    {
        "id": 66,
        "trait": "E",
        "text": "I make friends easily",
        "direction": True,
        "source": "BFI-2",
        "reliability": 0.86
    },
    {
        "id": 67,
        "trait": "E",
        "text": "I prefer working alone rather than in teams",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.83
    },

    # Agreeableness (A) - 8 items
    {
        "id": 68,
        "trait": "A",
        "text": "I sympathize with others' feelings",
        "direction": True,
        "source": "NEO-PI-R",
        "reliability": 0.86
    },
    {
        "id": 69,
        "trait": "A",
        "text": "I often argue with authority figures",
        "direction": False,
        "source": "BFI-2",
        "reliability": 0.82
    },
    {
        "id": 70,
        "trait": "A",
        "text": "I trust others' intentions",
        "direction": True,
        "source": "IPIP-NEO",
        "reliability": 0.84
    },
    {
        "id": 71,
        "trait": "A",
        "text": "I enjoy competitive situations more than cooperative ones",
        "direction": False,
        "source": "NEO-PI-R",
        "reliability": 0.83
    },
    {
        "id": 72,
        "trait": "A",
        "text": "I go out of my way to help others",
        "direction": True,
        "source": "BFI-2",
        "reliability": 0.85
    },
    {
        "id": 73,
        "trait": "A",
        "text": "I sometimes take advantage of others",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.81
    },
    {
        "id": 74,
        "trait": "A",
        "text": "I value harmony in relationships",
        "direction": True,
        "source": "NEO-PI-R",
        "reliability": 0.84
    },
    {
        "id": 75,
        "trait": "A",
        "text": "I enjoy debating controversial topics",
        "direction": False,
        "source": "BFI-2",
        "reliability": 0.83
    },

    # Neuroticism (N) - 8 items
    {
        "id": 76,
        "trait": "N",
        "text": "I often feel tense or anxious",
        "direction": True,
        "source": "IPIP-NEO",
        "reliability": 0.90
    },
    {
        "id": 77,
        "trait": "N",
        "text": "I remain calm under pressure",
        "direction": False,
        "source": "NEO-PI-R",
        "reliability": 0.84
    },
    {
        "id": 78,
        "trait": "N",
        "text": "I worry about things that might go wrong",
        "direction": True,
        "source": "BFI-2",
        "reliability": 0.86
    },
    {
        "id": 79,
        "trait": "N",
        "text": "I rarely feel sad or depressed",
        "direction": False,
        "source": "IPIP-NEO",
        "reliability": 0.83
    },
    {
        "id": 80,
        "trait": "N",
        "text": "I often feel emotionally vulnerable",
        "direction": True,
        "source": "NEO-PI-R",
        "reliability": 0.85
    },
    {
        "id": 81,
        "trait": "N",
        "text": "I handle stress well",
        "direction": False,
        "source": "BFI-2",
        "reliability": 0.84
    },
    {
        "id": 82,
        "trait": "N",
        "text": "I often feel overwhelmed by my emotions",
        "direction": True,
        "source": "IPIP-NEO",
        "reliability": 0.87
    },
    {
        "id": 83,
        "trait": "N",
        "text": "I rarely experience mood swings",
        "direction": False,
        "source": "NEO-PI-R",
        "reliability": 0.82
    },

    # Attention Check Items (3)
    {
        "id": 84,
        "trait": "V",
        "text": "Please select 'Strongly Agree' to verify you're paying attention",
        "direction": True,
        "source": "Validity Check",
        "correct_response": 4
    },
    {
        "id": 85,
        "trait": "V",
        "text": "I always answer questionnaires honestly",
        "direction": True,
        "source": "Validity Check",
        "correct_response": 4
    },
    {
        "id": 86,
        "trait": "V",
        "text": "I have never used a computer before",
        "direction": True,
        "source": "Validity Check",
        "correct_response": 0
    },
    {
        "id": 87,
        "trait": "V",
        "text": "I always double-check my answers on questionnaires",
        "direction": True,
        "source": "Attention Check",
        "reliability": "N/A"
    }
]

SCORING_KEY = {
    "O": {
        "max": 32,  # 8 items * 4 points max
        "norms": [(0,16,"Very Low"), (17,23,"Low"), (24,29,"Average"), (30,35,"High"), (36,40,"Very High")],
        "mean": 24.5,
        "sd": 6.2
    },
    "C": {
        "max": 32,
        "norms": [(0,15,"Very Low"), (16,22,"Low"), (23,28,"Average"), (29,34,"High"), (35,40,"Very High")],
        "mean": 25.1,
        "sd": 5.8
    },
    "E": {
        "max": 32,
        "norms": [(0,14,"Very Low"), (15,21,"Low"), (22,27,"Average"), (28,33,"High"), (34,40,"Very High")],
        "mean": 23.8,
        "sd": 6.5
    },
    "A": {
        "max": 32,
        "norms": [(0,16,"Very Low"), (17,23,"Low"), (24,29,"Average"), (30,35,"High"), (36,40,"Very High")],
        "mean": 25.3,
        "sd": 5.9
    },
    "N": {
        "max": 32,
        "norms": [(0,13,"Very Low"), (14,20,"Low"), (21,26,"Average"), (27,32,"High"), (33,40,"Very High")],
        "mean": 22.7,
        "sd": 7.1
    }
}

TRAIT_WEIGHTS = {
    "O": 1.0,
    "C": 1.0,
    "E": 1.0,
    "A": 1.0,
    "N": 1.0
}

TRAIT_DEFINITIONS = {
    "O": "Openness - Imagination, creativity, and preference for variety",
    "C": "Conscientiousness - Organization, dependability, and self-discipline",
    "E": "Extraversion - Sociability, assertiveness, and emotional expressiveness",
    "A": "Agreeableness - Compassion, cooperation, and trust",
    "N": "Neuroticism - Anxiety, emotional instability, and negative affect"
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