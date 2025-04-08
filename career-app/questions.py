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
    {"id": 1, "trait": "O", "text": "I enjoy exploring new ideas and concepts.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.87, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 2, "trait": "O", "text": "I tend to avoid philosophical or abstract discussions.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 3, "trait": "O", "text": "I have a vivid and active imagination.", "direction": "positive", "source": "BFI-2", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 4, "trait": "O", "text": "I prefer familiar routines over new experiences.", "direction": "negative", "source": "NEO-PI-R", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 5, "trait": "O", "text": "I find beauty in abstract art and creative expressions.", "direction": "positive", "source": "IPIP-NEO", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 6, "trait": "O", "text": "I find complex theoretical concepts uninteresting.", "direction": "negative", "source": "BFI-2", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 7, "trait": "O", "text": "I enjoy experiencing new cultures and traditions.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.86, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 8, "trait": "O", "text": "I prefer practical tasks over creative or imaginative ones.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Conscientiousness (C)
    {"id": 9, "trait": "C", "text": "I am always well-prepared for tasks and responsibilities.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 10, "trait": "C", "text": "I often forget to organize or tidy my belongings.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 11, "trait": "C", "text": "I pay close attention to details in my work.", "direction": "positive", "source": "BFI-2", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 12, "trait": "C", "text": "I frequently leave tasks incomplete or unfinished.", "direction": "negative", "source": "NEO-PI-R", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 13, "trait": "C", "text": "I prefer to follow a structured schedule or plan.", "direction": "positive", "source": "IPIP-NEO", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 14, "trait": "C", "text": "I tend to be careless with my responsibilities.", "direction": "negative", "source": "BFI-2", "reliability": 0.80, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 15, "trait": "C", "text": "I consistently strive for excellence in everything I do.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.86, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 16, "trait": "C", "text": "I often procrastinate on important tasks or deadlines.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Extraversion (E)
    {"id": 17, "trait": "E", "text": "I am often the life of the party at social events.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.88, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 18, "trait": "E", "text": "I prefer to stay in the background during social gatherings.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 19, "trait": "E", "text": "I enjoy meeting and interacting with new people.", "direction": "positive", "source": "BFI-2", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 20, "trait": "E", "text": "I feel exhausted after spending time at social events.", "direction": "negative", "source": "NEO-PI-R", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 21, "trait": "E", "text": "I am talkative and enjoy engaging in conversations.", "direction": "positive", "source": "IPIP-NEO", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 22, "trait": "E", "text": "I tend to avoid large social gatherings or events.", "direction": "negative", "source": "BFI-2", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 23, "trait": "E", "text": "I am assertive and confident in social interactions.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 24, "trait": "E", "text": "I prefer spending time alone rather than socializing.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Agreeableness (A)
    {"id": 25, "trait": "A", "text": "I am genuinely concerned about the well-being of others.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.86, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 26, "trait": "A", "text": "I am often indifferent to the feelings of others.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 27, "trait": "A", "text": "I am always willing to help others when they need support.", "direction": "positive", "source": "BFI-2", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 28, "trait": "A", "text": "I can be harsh or critical when giving feedback.", "direction": "negative", "source": "NEO-PI-R", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 29, "trait": "A", "text": "I find it easy to trust others and their intentions.", "direction": "positive", "source": "IPIP-NEO", "reliability": 0.80, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 30, "trait": "A", "text": "I frequently find myself arguing with others.", "direction": "negative", "source": "BFI-2", "reliability": 0.79, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 31, "trait": "A", "text": "I work well with others and value cooperation in teams.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 32, "trait": "A", "text": "I tend to hold grudges when others wrong me.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Neuroticism (N)
    {"id": 33, "trait": "N", "text": "I get stressed out easily in challenging situations.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.87, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 34, "trait": "N", "text": "I remain calm and composed even under pressure.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.85, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 35, "trait": "N", "text": "I often feel anxious or nervous about things.", "direction": "positive", "source": "BFI-2", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 36, "trait": "N", "text": "I rarely feel sad or depressed.", "direction": "negative", "source": "NEO-PI-R", "reliability": 0.83, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 37, "trait": "N", "text": "I experience frequent mood swings.", "direction": "positive", "source": "IPIP-NEO", "reliability": 0.82, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 38, "trait": "N", "text": "I feel emotionally stable most of the time.", "direction": "negative", "source": "BFI-2", "reliability": 0.81, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 39, "trait": "N", "text": "I worry a lot about things that might go wrong.", "direction": "positive", "source": "NEO-PI-R", "reliability": 0.86, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 40, "trait": "N", "text": "I handle setbacks and challenges with ease.", "direction": "negative", "source": "IPIP-NEO", "reliability": 0.84, "likert": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]}
]

SCORING_KEY = {
    'personality': {
        'O': {'trait': 'Openness', 'direction': 'positive'},
        'C': {'trait': 'Conscientiousness', 'direction': 'positive'},
        'E': {'trait': 'Extraversion', 'direction': 'positive'},
        'A': {'trait': 'Agreeableness', 'direction': 'positive'},
        'N': {'trait': 'Neuroticism', 'direction': 'positive'}
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
        "description": "Software Developers design, develop, and maintain software applications or systems.",
        "personality": {
            "Openness": 80,
            "Conscientiousness": 70,
            "Extraversion": 40,
            "Agreeableness": 50,
            "Neuroticism": 30
        },
        "aptitude": {
            "numerical": 80,
            "logical": 90,
            "verbal": 60,
            "spatial": 50
        },
        "skills": {"required": 75},
        "resources": [
            {"name": "Learn Python on Codecademy", "url": "https://www.codecademy.com/learn/learn-python-3"},
            {"name": "FreeCodeCamp", "url": "https://www.freecodecamp.org"}
        ],
        "interests": ["Software Development"]
    },
    "Data Scientist": {
        "description": "Data Scientists analyze and interpret complex data to help organizations make decisions.",
        "personality": {
            "Openness": 85,
            "Conscientiousness": 75,
            "Extraversion": 35,
            "Agreeableness": 45,
            "Neuroticism": 25
        },
        "aptitude": {
            "numerical": 90,
            "logical": 85,
            "verbal": 55,
            "spatial": 40
        },
        "skills": {"required": 80},
        "resources": [
            {"name": "Kaggle Competitions", "url": "https://www.kaggle.com/competitions"},
            {"name": "DataCamp", "url": "https://www.datacamp.com"}
        ],
        "interests": ["Data Science"]
    },
    "Graphic Designer": {
        "description": "Graphic Designers create visual concepts to communicate ideas that inspire, inform, or captivate consumers.",
        "personality": {
            "Openness": 90,
            "Conscientiousness": 60,
            "Extraversion": 50,
            "Agreeableness": 70,
            "Neuroticism": 40
        },
        "aptitude": {
            "numerical": 30,
            "logical": 50,
            "verbal": 60,
            "spatial": 90
        },
        "skills": {"required": 65},
        "resources": [
            {"name": "Adobe Creative Cloud Tutorials", "url": "https://helpx.adobe.com/creative-cloud/tutorials-explore.html"},
            {"name": "Canva Design School", "url": "https://www.canva.com/learn/"}
        ],
        "interests": ["Graphic Design"]
    },
    "Business Manager": {
        "description": "Business Managers oversee operations, manage teams, and ensure organizational goals are met.",
        "personality": {
            "Openness": 60,
            "Conscientiousness": 85,
            "Extraversion": 75,
            "Agreeableness": 65,
            "Neuroticism": 35
        },
        "aptitude": {
            "numerical": 70,
            "logical": 75,
            "verbal": 80,
            "spatial": 40
        },
        "skills": {"required": 70},
        "resources": [
            {"name": "Coursera Business Management Courses", "url": "https://www.coursera.org/courses?query=business%20management"},
            {"name": "Harvard Business Review", "url": "https://hbr.org/"}
        ],
        "interests": ["Business Management"]
    },
    "Research Scientist": {
        "description": "Research Scientists conduct experiments and research to advance knowledge in their field.",
        "personality": {
            "Openness": 95,
            "Conscientiousness": 80,
            "Extraversion": 30,
            "Agreeableness": 50,
            "Neuroticism": 20
        },
        "aptitude": {
            "numerical": 85,
            "logical": 90,
            "verbal": 70,
            "spatial": 60
        },
        "skills": {"required": 85},
        "resources": [
            {"name": "Google Scholar", "url": "https://scholar.google.com/"},
            {"name": "ResearchGate", "url": "https://www.researchgate.net/"}
        ],
        "interests": ["Scientific"]
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
    "Software Development": {
        "basic": [
            {"name": "Learn Python on Codecademy", "url": "https://www.codecademy.com/learn/learn-python-3"},
            {"name": "FreeCodeCamp", "url": "https://www.freecodecamp.org"}
        ],
        "intermediate": [
            {"name": "Intermediate Python on Coursera", "url": "https://www.coursera.org/learn/intermediate-python"},
            {"name": "GitHub Learning Lab", "url": "https://lab.github.com/"}
        ],
        "advanced": [
            {"name": "Advanced Software Engineering on edX", "url": "https://www.edx.org/course/advanced-software-engineering"},
            {"name": "LeetCode", "url": "https://leetcode.com/"}
        ]
    },
    "Data Science": {
        "basic": [
            {"name": "Kaggle Competitions", "url": "https://www.kaggle.com/competitions"},
            {"name": "DataCamp", "url": "https://www.datacamp.com"}
        ],
        "intermediate": [
            {"name": "Intermediate Data Science on Coursera", "url": "https://www.coursera.org/learn/data-science-intermediate"},
            {"name": "Tableau Public", "url": "https://public.tableau.com/"}
        ],
        "advanced": [
            {"name": "Advanced Machine Learning on edX", "url": "https://www.edx.org/course/advanced-machine-learning"},
            {"name": "Fast.ai", "url": "https://www.fast.ai/"}
        ]
    },
    "Graphic Design": {
        "basic": [
            {"name": "Adobe Creative Cloud Tutorials", "url": "https://helpx.adobe.com/creative-cloud/tutorials-explore.html"},
            {"name": "Canva Design School", "url": "https://www.canva.com/learn/"}
        ],
        "intermediate": [
            {"name": "Intermediate Graphic Design on Udemy", "url": "https://www.udemy.com/topic/graphic-design/"},
            {"name": "Behance Portfolio", "url": "https://www.behance.net/"}
        ],
        "advanced": [
            {"name": "Advanced Typography on Skillshare", "url": "https://www.skillshare.com/classes/advanced-typography"},
            {"name": "Dribbble", "url": "https://dribbble.com/"}
        ]
    },
    "Business Management": {
        "basic": [
            {"name": "Coursera Business Management Courses", "url": "https://www.coursera.org/courses?query=business%20management"},
            {"name": "Harvard Business Review", "url": "https://hbr.org/"}
        ],
        "intermediate": [
            {"name": "Intermediate Leadership on LinkedIn Learning", "url": "https://www.linkedin.com/learning/topics/leadership"},
            {"name": "MindTools", "url": "https://www.mindtools.com/"}
        ],
        "advanced": [
            {"name": "Advanced Business Strategy on edX", "url": "https://www.edx.org/course/advanced-business-strategy"},
            {"name": "McKinsey Insights", "url": "https://www.mckinsey.com/insights"}
        ]
    },
    "Scientific": {
        "basic": [
            {"name": "Google Scholar", "url": "https://scholar.google.com/"},
            {"name": "ResearchGate", "url": "https://www.researchgate.net/"}
        ],
        "intermediate": [
            {"name": "Intermediate Research Methods on Coursera", "url": "https://www.coursera.org/learn/research-methods"},
            {"name": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/"}
        ],
        "advanced": [
            {"name": "Advanced Scientific Writing on edX", "url": "https://www.edx.org/course/scientific-writing"},
            {"name": "arXiv", "url": "https://arxiv.org/"}
        ]
    }
}
SCORING_WEIGHTS = {
    'base_weights': {
        'aptitude': 0.6,
        'personality': 0.4
    },
    'enhanced_weights': {
        'aptitude': 0.4,
        'personality': 0.3,
        'skill_gap': 0.3
    },
    'category_weights': {
        'aptitude': {
            'verbal': 0.25,
            'numerical': 0.35,
            'logical': 0.4
        },
        'personality': {
            'Openness': 0.2,
            'Conscientiousness': 0.25,
            'Extraversion': 0.15,
            'Agreeableness': 0.2,
            'Neuroticism': 0.2
        }
    }
}