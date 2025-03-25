APTITUDE_QUESTIONS = {
    "Mathematics": {
        "easy": [
            {
                "id": "M1-E",
                "type": "numerical",
                "text": "Solve: 15 + 8 × 3 ÷ 4",
                "options": ["21", "18.5", "19.5", "20.25"],
                "correct": 0,  # Fixed: 15 + (8 × 3 ÷ 4) = 15 + 6 = 21
                "time_limit": 60,
                "irt_params": {"difficulty": -1.2, "discrimination": 0.8}
            },
            {
                "id": "M4-E",
                "type": "geometry",
                "text": "What is the area of a rectangle with length 5 cm and width 3 cm?",
                "options": ["15 cm²", "16 cm²", "18 cm²", "20 cm²"],
                "correct": 0,
                "time_limit": 45,
                "irt_params": {"difficulty": -1.0, "discrimination": 0.9}
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
                "irt_params": {"difficulty": 0.5, "discrimination": 1.2}
            },
            {
                "id": "M5-M",
                "type": "statistics",
                "text": "Find the median of: 3, 7, 2, 8, 5",
                "options": ["5", "6", "7", "8"],
                "correct": 0,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.1}
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
                "irt_params": {"difficulty": 1.8, "discrimination": 1.5}
            },
            {
                "id": "M6-H",
                "type": "probability",
                "text": "A bag has 4 red and 6 blue balls. What’s the probability of drawing 2 red balls in a row without replacement?",
                "options": ["1/15", "2/15", "4/45", "6/45"],
                "correct": 2,
                "time_limit": 150,
                "irt_params": {"difficulty": 2.1, "discrimination": 1.4}
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
                "irt_params": {"difficulty": -1.0, "discrimination": 0.9}
            },
            {
                "id": "LR4-E",
                "type": "analogy",
                "text": "Bird is to Fly as Fish is to ___",
                "options": ["Swim", "Walk", "Jump", "Crawl"],
                "correct": 0,
                "time_limit": 40,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.8}
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
                "irt_params": {"difficulty": 0.7, "discrimination": 1.1}
            },
            {
                "id": "LR5-M",
                "type": "syllogism",
                "text": "Some A are B. All B are C. Therefore:",
                "options": ["All A are C", "Some A are C", "No A are C", "All C are A"],
                "correct": 1,
                "time_limit": 90,
                "irt_params": {"difficulty": 0.8, "discrimination": 1.2}
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
                "irt_params": {"difficulty": 2.0, "discrimination": 1.4}
            },
            {
                "id": "LR6-H",
                "type": "logic_puzzle",
                "text": "Three friends rank 1st, 2nd, 3rd in a race. A is not last, B is ahead of C. Who is 2nd?",
                "options": ["A", "B", "C", "Cannot determine"],
                "correct": 0,
                "time_limit": 180,
                "irt_params": {"difficulty": 2.2, "discrimination": 1.5}
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
                "irt_params": {"difficulty": -0.8, "discrimination": 0.7}
            },
            {
                "id": "VA4-E",
                "type": "synonym",
                "text": "Find a synonym for 'Benevolent':",
                "options": ["Kind", "Harsh", "Greedy", "Silent"],
                "correct": 0,
                "time_limit": 40,
                "irt_params": {"difficulty": -0.7, "discrimination": 0.8}
            }
        ],
        "moderate": [
            {
                "id": "VA2-M",
                "type": "comprehension",
                "text": "'The company’s pecuniary situation was precarious.' What does 'pecuniary' mean?",
                "options": ["Legal", "Financial", "Ethical", "Structural"],
                "correct": 1,
                "time_limit": 60,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.0}
            },
            {
                "id": "VA5-M",
                "type": "sentence_completion",
                "text": "Her ___ attitude inspired the team to exceed their goals.",
                "options": ["apathetic", "motivating", "indifferent", "hostile"],
                "correct": 1,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.1}
            }
        ],
        "hard": [
            {
                "id": "VA3-H",
                "type": "critical_reasoning",
                "text": "Which weakens: 'Remote work increases productivity because employees save commute time'?",
                "options": [
                    "Commute time averages 45 minutes daily",
                    "Home distractions reduce focused work hours",
                    "Companies report higher profits with remote teams",
                    "Video conferencing tools improve collaboration"
                ],
                "correct": 1,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.5, "discrimination": 1.3}
            },
            {
                "id": "VA6-H",
                "type": "analogies",
                "text": "Mitigate : Severity :: Amplify : ___",
                "options": ["Volume", "Calmness", "Silence", "Weakness"],
                "correct": 0,
                "time_limit": 100,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
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
        "Mathematics": {"thresholds": [40, 70]},
        "Logical Reasoning": {"thresholds": [45, 75]},
        "Verbal Ability": {"thresholds": [35, 65]}
    }
}

PERSONALITY_QUESTIONS = [
    # Openness to Experience (O)
    {"id": 1, "trait": "O", "text": "I enjoy hearing new ideas", "direction": True, "source": "NEO-PI-R", "reliability": 0.87, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 2, "trait": "O", "text": "I avoid philosophical discussions", "direction": False, "source": "IPIP-NEO", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 3, "trait": "O", "text": "I have a vivid imagination", "direction": True, "source": "BFI-2", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 4, "trait": "O", "text": "I prefer routine over variety", "direction": False, "source": "NEO-PI-R", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 5, "trait": "O", "text": "I appreciate abstract art", "direction": True, "source": "IPIP-NEO", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 6, "trait": "O", "text": "I dislike complex theoretical concepts", "direction": False, "source": "BFI-2", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 7, "trait": "O", "text": "I enjoy trying new cultural experiences", "direction": True, "source": "NEO-PI-R", "reliability": 0.86, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 8, "trait": "O", "text": "I prefer practical over creative tasks", "direction": False, "source": "IPIP-NEO", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Conscientiousness (C)
    {"id": 9, "trait": "C", "text": "I am always prepared", "direction": True, "source": "NEO-PI-R", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 10, "trait": "C", "text": "I often forget to put things back in their proper place", "direction": False, "source": "IPIP-NEO", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 11, "trait": "C", "text": "I pay attention to details", "direction": True, "source": "BFI-2", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 12, "trait": "C", "text": "I leave my tasks unfinished", "direction": False, "source": "NEO-PI-R", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 13, "trait": "C", "text": "I follow a schedule", "direction": True, "source": "IPIP-NEO", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 14, "trait": "C", "text": "I am careless with my work", "direction": False, "source": "BFI-2", "reliability": 0.80, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 15, "trait": "C", "text": "I strive for excellence", "direction": True, "source": "NEO-PI-R", "reliability": 0.86, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 16, "trait": "C", "text": "I procrastinate on important tasks", "direction": False, "source": "IPIP-NEO", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Extraversion (E)
    {"id": 17, "trait": "E", "text": "I am the life of the party", "direction": True, "source": "NEO-PI-R", "reliability": 0.88, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 18, "trait": "E", "text": "I prefer to stay in the background", "direction": False, "source": "IPIP-NEO", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 19, "trait": "E", "text": "I enjoy meeting new people", "direction": True, "source": "BFI-2", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 20, "trait": "E", "text": "I feel drained after social events", "direction": False, "source": "NEO-PI-R", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 21, "trait": "E", "text": "I am talkative", "direction": True, "source": "IPIP-NEO", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 22, "trait": "E", "text": "I avoid large gatherings", "direction": False, "source": "BFI-2", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 23, "trait": "E", "text": "I am assertive in conversations", "direction": True, "source": "NEO-PI-R", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 24, "trait": "E", "text": "I prefer solitude over socializing", "direction": False, "source": "IPIP-NEO", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Agreeableness (A)
    {"id": 25, "trait": "A", "text": "I am interested in others' well-being", "direction": True, "source": "NEO-PI-R", "reliability": 0.86, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 26, "trait": "A", "text": "I am indifferent to others' feelings", "direction": False, "source": "IPIP-NEO", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 27, "trait": "A", "text": "I am willing to help others", "direction": True, "source": "BFI-2", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 28, "trait": "A", "text": "I can be harsh in my criticism", "direction": False, "source": "NEO-PI-R", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 29, "trait": "A", "text": "I trust others easily", "direction": True, "source": "IPIP-NEO", "reliability": 0.80, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 30, "trait": "A", "text": "I often argue with others", "direction": False, "source": "BFI-2", "reliability": 0.79, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 31, "trait": "A", "text": "I am cooperative in team settings", "direction": True, "source": "NEO-PI-R", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 32, "trait": "A", "text": "I hold grudges against others", "direction": False, "source": "IPIP-NEO", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Neuroticism (N)
    {"id": 33, "trait": "N", "text": "I get stressed out easily", "direction": True, "source": "NEO-PI-R", "reliability": 0.87, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 34, "trait": "N", "text": "I remain calm under pressure", "direction": False, "source": "IPIP-NEO", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 35, "trait": "N", "text": "I often feel anxious", "direction": True, "source": "BFI-2", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 36, "trait": "N", "text": "I rarely feel depressed", "direction": False, "source": "NEO-PI-R", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 37, "trait": "N", "text": "I experience mood swings", "direction": True, "source": "IPIP-NEO", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 38, "trait": "N", "text": "I am emotionally stable", "direction": False, "source": "BFI-2", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 39, "trait": "N", "text": "I worry about things a lot", "direction": True, "source": "NEO-PI-R", "reliability": 0.86, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 40, "trait": "N", "text": "I handle setbacks well", "direction": False, "source": "IPIP-NEO", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]}
]

SCORING_KEY = {
    "O": {
        "max": 32,
        "norms": [(0, 16, "Very Low"), (17, 23, "Low"), (24, 29, "Average"), (30, 35, "High"), (36, 40, "Very High")],
        "mean": 24.5,
        "sd": 6.2
    },
    "C": {
        "max": 32,
        "norms": [(0, 15, "Very Low"), (16, 22, "Low"), (23, 28, "Average"), (29, 34, "High"), (35, 40, "Very High")],
        "mean": 25.1,
        "sd": 5.8
    },
    "E": {
        "max": 32,
        "norms": [(0, 14, "Very Low"), (15, 21, "Low"), (22, 27, "Average"), (28, 33, "High"), (34, 40, "Very High")],
        "mean": 23.8,
        "sd": 6.5
    },
    "A": {
        "max": 32,
        "norms": [(0, 16, "Very Low"), (17, 23, "Low"), (24, 29, "Average"), (30, 35, "High"), (36, 40, "Very High")],
        "mean": 25.3,
        "sd": 5.9
    },
    "N": {
        "max": 32,
        "norms": [(0, 13, "Very Low"), (14, 20, "Low"), (21, 26, "Average"), (27, 32, "High"), (33, 40, "Very High")],
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
    "Software Developer": {
        "aptitude": {"Mathematics": 70, "Logical Reasoning": 80, "Verbal Ability": 60},
        "personality": {"Openness": 60, "Conscientiousness": 70, "Extraversion": 50, "Agreeableness": 50, "Neuroticism": 40},
        "skills": {"Software Development": 70},
        "interests": ["Software Development"],
        "description": "Designs and builds software applications.",
        "resources": [
            {"name": "Learn Python", "link": "https://www.codecademy.com/learn/learn-python-3"},
            {"name": "Git Tutorial", "link": "https://www.atlassian.com/git/tutorials"}
        ],
        "soc_code": "15-1252.00"
    },
    "Data Scientist": {
        "aptitude": {"Mathematics": 85, "Logical Reasoning": 75, "Verbal Ability": 50},
        "personality": {"Openness": 70, "Conscientiousness": 65, "Extraversion": 40, " Agreeableness": 45, "Neuroticism": 35},
        "skills": {"Data Science": 80},
        "interests": ["Data Science"],
        "description": "Analyzes complex data to uncover insights and trends.",
        "resources": [
            {"name": "Data Science Course", "link": "https://www.coursera.org/learn/data-science"},
            {"name": "Pandas Tutorial", "link": "https://pandas.pydata.org/docs/getting_started/"}
        ],
        "soc_code": "15-2051.00"
    },
    "Graphic Designer": {
        "aptitude": {"Mathematics": 40, "Logical Reasoning": 50, "Verbal Ability": 70},
        "personality": {"Openness": 80, "Conscientiousness": 60, "Extraversion": 60, " Agreeableness": 55, "Neuroticism": 45},
        "skills": {"Graphic Design": 75},
        "interests": ["Graphic Design"],
        "description": "Creates visual content to communicate messages.",
        "resources": [
            {"name": "Adobe Photoshop Basics", "link": "https://www.adobe.com/products/photoshop.html"},
            {"name": "Design Principles", "link": "https://www.canva.com/learn/design-principles/"}
        ],
        "soc_code": "27-1024.00"
    },
    "Business Manager": {
        "aptitude": {"Mathematics": 60, "Logical Reasoning": 70, "Verbal Ability": 80},
        "personality": {"Openness": 50, "Conscientiousness": 75, "Extraversion": 70, " Agreeableness": 60, "Neuroticism": 30},
        "skills": {"Business Management": 70},
        "interests": ["Business Management"],
        "description": "Oversees operations and strategic planning for organizations.",
        "resources": [
            {"name": "MBA Essentials", "link": "https://www.coursera.org/learn/mba-essentials"},
            {"name": "Leadership Skills", "link": "https://www.mindtools.com/pages/main/leadership.htm"}
        ],
        "soc_code": "11-1021.00"
    }
}

SKILL_GAP_QUESTIONS = {
    "Software Development": [
        {
            "id": 1,
            "text": "What will be the output of the following Python code? \n\n```python\nx = [1, 2, 3]\ny = x\ny[0] = 5\nprint(x)\n```",
            "options": ["[1, 2, 3]", "[5, 2, 3]", "[5, 5, 5]", "Error"],
            "correct": 1,
            "time_limit": 60
        },
        {
            "id": 2,
            "text": "In Object-Oriented Programming, what does inheritance allow?",
            "options": [
                "A class to inherit attributes and methods from another class",
                "A class to override all methods",
                "A class to become abstract",
                "A class to hide its data"
            ],
            "correct": 0,
            "time_limit": 45
        },
        {
            "id": 3,
            "text": "Which Git command is used to save changes to the local repository?",
            "options": ["git add", "git commit", "git push", "git pull"],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "What does the HTTP status code 404 indicate in a RESTful API?",
            "options": ["Success", "Unauthorized", "Not Found", "Server Error"],
            "correct": 2,
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is the time complexity of a binary search algorithm?",
            "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 6,
            "text": "In Agile methodology, what is a 'sprint'?",
            "options": [
                "A long-term project phase",
                "A short, time-boxed period to complete work",
                "A meeting to assign tasks",
                "A retrospective analysis"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 7,
            "text": "What does Test-Driven Development (TDD) emphasize?",
            "options": [
                "Writing tests after coding",
                "Writing tests before coding",
                "Skipping tests for faster delivery",
                "Testing only at the end"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What SQL command is used to retrieve data from a database?",
            "options": ["INSERT", "UPDATE", "SELECT", "DELETE"],
            "correct": 2,
            "time_limit": 30
        },
        {
            "id": 9,
            "text": "Which CSS property is used to make text bold?",
            "options": ["font-style", "font-weight", "text-decoration", "font-size"],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 10,
            "text": "What is the primary purpose of AWS S3?",
            "options": [
                "Compute services",
                "Object storage",
                "Relational database",
                "Networking"
            ],
            "correct": 1,
            "time_limit": 30
        }
    ],
    "Data Science": [
        {
            "id": 1,
            "text": "What Python library is commonly used for data manipulation and analysis?",
            "options": ["NumPy", "Pandas", "Matplotlib", "Seaborn"],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What does a p-value less than 0.05 typically indicate in hypothesis testing?",
            "options": [
                "The null hypothesis is true",
                "The result is statistically significant",
                "The sample size is too small",
                "The test is inconclusive"
            ],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 3,
            "text": "Which algorithm is a supervised learning method for classification?",
            "options": ["K-Means", "Linear Regression", "Logistic Regression", "PCA"],
            "correct": 2,
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "Which tool is best suited for creating a bar chart in Python?",
            "options": ["Pandas", "NumPy", "Matplotlib", "Scikit-learn"],
            "correct": 2,
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is the first step in data wrangling?",
            "options": [
                "Data visualization",
                "Handling missing values",
                "Model training",
                "Feature selection"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 6,
            "text": "Which SQL clause is used to filter rows after grouping?",
            "options": ["WHERE", "HAVING", "GROUP BY", "ORDER BY"],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 7,
            "text": "What is Apache Spark primarily used for?",
            "options": [
                "Web development",
                "Big data processing",
                "Database management",
                "Graphic design"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What is feature engineering in machine learning?",
            "options": [
                "Selecting the best model",
                "Creating new features from existing data",
                "Reducing model complexity",
                "Testing the model"
            ],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 9,
            "text": "Which framework is commonly used for deep learning?",
            "options": ["Pandas", "TensorFlow", "Scikit-learn", "Flask"],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 10,
            "text": "What does ARIMA stand for in time series analysis?",
            "options": [
                "Auto-Regressive Integrated Moving Average",
                "Adaptive Random Iterative Model Analysis",
                "Automated Regression for Moving Averages",
                "Analysis of Random Integrated Models"
            ],
            "correct": 0,
            "time_limit": 45
        }
    ],
    "Graphic Design": [
        {
            "id": 1,
            "text": "What Photoshop tool is used to remove part of an image?",
            "options": ["Brush Tool", "Eraser Tool", "Clone Stamp Tool", "Magic Wand Tool"],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "In Adobe Illustrator, which tool creates shapes with anchor points?",
            "options": ["Pen Tool", "Brush Tool", "Gradient Tool", "Eyedropper Tool"],
            "correct": 0,
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "What does the color theory term 'complementary colors' mean?",
            "options": [
                "Colors that are similar in hue",
                "Colors opposite each other on the color wheel",
                "Colors that are monochromatic",
                "Colors that are neutral"
            ],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "What is the primary purpose of typography in design?",
            "options": [
                "To fill empty space",
                "To enhance readability and aesthetics",
                "To create complex patterns",
                "To replace images"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What are vector graphics primarily used for?",
            "options": [
                "Pixel-based images",
                "Scalable images without quality loss",
                "3D modeling",
                "Video editing"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 6,
            "text": "What does UX in UI/UX design stand for?",
            "options": [
                "User Experience",
                "User Extension",
                "Unique Experience",
                "User Exploration"
            ],
            "correct": 0,
            "time_limit": 30
        },
        {
            "id": 7,
            "text": "What is a key element of branding in design?",
            "options": [
                "Random color schemes",
                "Consistency in visual identity",
                "Using multiple logos",
                "Avoiding typography"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What Adobe software is best for creating motion graphics?",
            "options": ["Photoshop", "Illustrator", "After Effects", "InDesign"],
            "correct": 2,
            "time_limit": 30
        },
        {
            "id": 9,
            "text": "What is the standard resolution for print design?",
            "options": ["72 DPI", "150 DPI", "300 DPI", "600 DPI"],
            "correct": 2,
            "time_limit": 30
        },
        {
            "id": 10,
            "text": "Which tool is commonly used for UI prototyping?",
            "options": ["Photoshop", "Figma", "Illustrator", "Premiere Pro"],
            "correct": 1,
            "time_limit": 30
        }
    ],
    "Business Management": [
        {
            "id": 1,
            "text": "What does SWOT analysis stand for in strategic planning?",
            "options": [
                "Strengths, Weaknesses, Opportunities, Threats",
                "Strategy, Work, Operations, Trends",
                "Systems, Workflow, Objectives, Targets",
                "Strengths, Work, Opportunities, Trends"
            ],
            "correct": 0,
            "time_limit": 45
        },
        {
            "id": 2,
            "text": "What is the primary goal of financial forecasting?",
            "options": [
                "To spend the budget",
                "To predict future financial performance",
                "To reduce employee salaries",
                "To increase marketing costs"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "Which leadership style focuses on employee participation?",
            "options": [
                "Autocratic",
                "Democratic",
                "Transactional",
                "Laissez-faire"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "In project management, what does the Scrum framework emphasize?",
            "options": [
                "Long-term planning",
                "Iterative development and teamwork",
                "Individual tasks",
                "Top-down management"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is a key skill for effective negotiation?",
            "options": [
                "Ignoring the other party",
                "Active listening",
                "Dominating the conversation",
                "Avoiding compromise"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 6,
            "text": "What does Porter’s Five Forces analyze?",
            "options": [
                "Employee performance",
                "Competitive environment of a business",
                "Financial statements",
                "Marketing strategies"
            ],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 7,
            "text": "What is the goal of change management?",
            "options": [
                "To resist organizational changes",
                "To manage transitions effectively",
                "To increase employee turnover",
                "To reduce profits"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What is a common method for risk assessment?",
            "options": [
                "Ignoring risks",
                "SWOT analysis",
                "Probability and impact analysis",
                "Random guessing"
            ],
            "correct": 2,
            "time_limit": 45
        },
        {
            "id": 9,
            "text": "What does data-driven decision making rely on?",
            "options": [
                "Intuition",
                "Quantitative analysis",
                "Guesswork",
                "Employee opinions"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 10,
            "text": "Who is considered a stakeholder in a project?",
            "options": [
                "Only the project manager",
                "Anyone impacted by the project",
                "Only the CEO",
                "Only the employees"
            ],
            "correct": 1,
            "time_limit": 30
        }
    ]
}

LEARNING_RESOURCES = {
    "Software Development": [
        {"skill": "Proficiency in Python programming", "resource": "Learn Python on Codecademy", "link": "https://www.codecademy.com/learn/learn-python-3"},
        {"skill": "Experience with Git version control", "resource": "Git Tutorial on Atlassian", "link": "https://www.atlassian.com/git/tutorials"},
        {"skill": "Understanding of Object-Oriented Programming (OOP)", "resource": "OOP in Python on Real Python", "link": "https://realpython.com/python3-object-oriented-programming/"},
        {"skill": "Knowledge of RESTful API development", "resource": "REST API Tutorial on freeCodeCamp", "link": "https://www.freecodecamp.org/news/rest-api-tutorial-rest-client-rest-service-and-api-calls-explained-with-code-examples/"},
        {"skill": "Debugging and problem-solving skills", "resource": "Debugging in Python on Real Python", "link": "https://realpython.com/python-debugging-pdb/"},
        {"skill": "Familiarity with Agile methodologies", "resource": "Agile Methodology on Coursera", "link": "https://www.coursera.org/learn/agile-development"},
        {"skill": "Unit testing and Test-Driven Development (TDD)", "resource": "TDD in Python on TestDriven.io", "link": "https://testdriven.io/courses/tdd-python/"},
        {"skill": "Database management (e.g., SQL)", "resource": "SQL for Beginners on Khan Academy", "link": "https://www.khanacademy.org/computing/computer-programming/sql"},
        {"skill": "Frontend development (e.g., HTML, CSS, JavaScript)", "resource": "Frontend Development on freeCodeCamp", "link": "https://www.freecodecamp.org/learn/front-end-development/"},
        {"skill": "Cloud computing basics (e.g., AWS, Azure)", "resource": "AWS Fundamentals on Coursera", "link": "https://www.coursera.org/learn/aws-fundamentals"}
    ],
    "Data Science": [
        {"skill": "Proficiency in Python or R for data analysis", "resource": "Data Analysis with Python on Coursera", "link": "https://www.coursera.org/learn/data-analysis-python"},
        {"skill": "Statistical analysis and hypothesis testing", "resource": "Statistics with Python on Coursera", "link": "https://www.coursera.org/learn/statistics-with-python"},
        {"skill": "Experience with machine learning algorithms", "resource": "Machine Learning by Andrew Ng on Coursera", "link": "https://www.coursera.org/learn/machine-learning"},
        {"skill": "Data visualization (e.g., Matplotlib, Tableau)", "resource": "Data Visualization with Python on Coursera", "link": "https://www.coursera.org/learn/python-for-data-visualization"},
        {"skill": "Data wrangling and cleaning", "resource": "Data Wrangling with Pandas on DataCamp", "link": "https://www.datacamp.com/courses/data-manipulation-with-pandas"},
        {"skill": "Knowledge of SQL for data querying", "resource": "SQL for Data Science on Coursera", "link": "https://www.coursera.org/learn/sql-for-data-science"},
        {"skill": "Familiarity with big data tools (e.g., Hadoop, Spark)", "resource": "Big Data with Spark on Coursera", "link": "https://www.coursera.org/learn/big-data-spark"},
        {"skill": "Feature engineering for machine learning", "resource": "Feature Engineering on Kaggle", "link": "https://www.kaggle.com/learn/feature-engineering"},
        {"skill": "Understanding of deep learning frameworks (e.g., TensorFlow)", "resource": "Deep Learning with TensorFlow on Coursera", "link": "https://www.coursera.org/learn/deep-learning-tensorflow"},
        {"skill": "Time series analysis", "resource": "Time Series Analysis on Coursera", "link": "https://www.coursera.org/learn/practical-time-series-analysis"}
    ],
    "Graphic Design": [
        {"skill": "Proficiency in Adobe Photoshop", "resource": "Photoshop Tutorials on Adobe", "link": "https://www.adobe.com/products/photoshop/tutorials.html"},
        {"skill": "Proficiency in Adobe Illustrator", "resource": "Illustrator Tutorials on Adobe", "link": "https://www.adobe.com/products/illustrator/tutorials.html"},
        {"skill": "Understanding of color theory", "resource": "Color Theory on Coursera", "link": "https://www.coursera.org/learn/color-theory"},
        {"skill": "Typography and font selection", "resource": "Typography Basics on Skillshare", "link": "https://www.skillshare.com/classes/Introduction-to-Typography"},
        {"skill": "Creating vector graphics", "resource": "Vector Graphics with Illustrator on Udemy", "link": "https://www.udemy.com/course/adobe-illustrator-cc-for-beginners/"},
        {"skill": "UI/UX design principles", "resource": "UI/UX Design on Coursera", "link": "https://www.coursera.org/specializations/ui-ux-design"},
        {"skill": "Branding and logo design", "resource": "Logo Design on Skillshare", "link": "https://www.skillshare.com/classes/Logo-Design-Masterclass"},
        {"skill": "Motion graphics (e.g., After Effects)", "resource": "Motion Graphics with After Effects on Udemy", "link": "https://www.udemy.com/course/after-effects-motion-graphics/"},
        {"skill": "Print design and layout", "resource": "Print Design on Skillshare", "link": "https://www.skillshare.com/classes/Print-Design-Fundamentals"},
        {"skill": "Prototyping tools (e.g., Figma, Sketch)", "resource": "Figma for Beginners on Coursera", "link": "https://www.coursera.org/learn/figma-ux-ui"}
    ],
    "Business Management": [
        {"skill": "Strategic planning and goal setting", "resource": "Strategic Management on Coursera", "link": "https://www.coursera.org/learn/strategic-management"},
        {"skill": "Financial budgeting and forecasting", "resource": "Financial Management on Coursera", "link": "https://www.coursera.org/learn/financial-management"},
        {"skill": "Leadership and team management", "resource": "Leadership Skills on Udemy", "link": "https://www.udemy.com/topic/leadership/"},
        {"skill": "Project management (e.g., Agile, Scrum)", "resource": "Agile Project Management on Coursera", "link": "https://www.coursera.org/learn/agile-project-management"},
        {"skill": "Effective communication and negotiation", "resource": "Negotiation Skills on Coursera", "link": "https://www.coursera.org/learn/negotiation-skills"},
        {"skill": "Market analysis and competitive research", "resource": "Market Research on Coursera", "link": "https://www.coursera.org/learn/market-research"},
        {"skill": "Change management", "resource": "Change Management on Coursera", "link": "https://www.coursera.org/learn/change-management"},
        {"skill": "Risk assessment and mitigation", "resource": "Risk Management on Coursera", "link": "https://www.coursera.org/learn/risk-management"},
        {"skill": "Data-driven decision making", "resource": "Data-Driven Decision Making on Coursera", "link": "https://www.coursera.org/learn/data-driven-decision-making"},
        {"skill": "Stakeholder management", "resource": "Stakeholder Management on Coursera", "link": "https://www.coursera.org/learn/stakeholder-management"}
    ]
}