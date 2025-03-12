# data/personality_questions.py

CATEGORIES = {
    "O": "Openness",
    "C": "Conscientiousness",
    "E": "Extraversion",
    "A": "Agreeableness",
    "N": "Neuroticism"
}

QUESTIONS = [
    {
        "id": 1,
        "question": "When making important decisions, you tend to:",
        "options": [
            {"text": "Analyze all possible outcomes systematically", "dimensions": {"C": 4}},
            {"text": "Consult with multiple people", "dimensions": {"E": 3}},
            {"text": "Go with your gut feeling", "dimensions": {"O": 2}},
            {"text": "Consider others' needs first", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 2,
        "question": "Your approach to deadlines is typically:",
        "options": [
            {"text": "Complete tasks weeks in advance (C)", "dimensions": {"C": 4}},
            {"text": "Work best under pressure (N)", "dimensions": {"N": 3}},
            {"text": "Adjust timelines as needed (O)", "dimensions": {"O": 2}},
            {"text": "Collaborate to meet targets (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 3,
        "question": "In social gatherings, you usually:",
        "options": [
            {"text": "Initiate conversations (E)", "dimensions": {"E": 4}},
            {"text": "Observe before participating (N)", "dimensions": {"N": 3}},
            {"text": "Discuss abstract ideas (O)", "dimensions": {"O": 2}},
            {"text": "Ensure everyone feels included (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 4,
        "question": "When faced with criticism, you:",
        "options": [
            {"text": "Objectively analyze its validity (C)", "dimensions": {"C": 4}},
            {"text": "Take it personally (N)", "dimensions": {"N": 3}},
            {"text": "Consider alternative perspectives (O)", "dimensions": {"O": 2}},
            {"text": "Focus on maintaining harmony (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 5,
        "question": "Your ideal weekend involves:",
        "options": [
            {"text": "Structured activities (C)", "dimensions": {"C": 4}},
            {"text": "Social events (E)", "dimensions": {"E": 3}},
            {"text": "Creative exploration (O)", "dimensions": {"O": 2}},
            {"text": "Helping community (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 6,
        "question": "When learning something new, you prefer:",
        "options": [
            {"text": "Step-by-step instructions (C)", "dimensions": {"C": 4}},
            {"text": "Group learning (E)", "dimensions": {"E": 3}},
            {"text": "Experimental approach (O)", "dimensions": {"O": 2}},
            {"text": "Mentorship relationships (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 7,
        "question": "Your reaction to sudden changes is typically:",
        "options": [
            {"text": "Create contingency plans (C)", "dimensions": {"C": 4}},
            {"text": "Experience anxiety (N)", "dimensions": {"N": 3}},
            {"text": "Find it exciting (O)", "dimensions": {"O": 2}},
            {"text": "Adapt to maintain peace (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 8,
        "question": "In team projects, you usually:",
        "options": [
            {"text": "Organize workflow (C)", "dimensions": {"C": 4}},
            {"text": "Motivate team members (E)", "dimensions": {"E": 3}},
            {"text": "Propose innovative solutions (O)", "dimensions": {"O": 2}},
            {"text": "Resolve conflicts (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 9,
        "question": "Your approach to personal goals:",
        "options": [
            {"text": "Detailed 5-year plan (C)", "dimensions": {"C": 4}},
            {"text": "Flexible aspirations (O)", "dimensions": {"O": 3}},
            {"text": "Socially influenced (E)", "dimensions": {"E": 2}},
            {"text": "Altruistically motivated (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 10,
        "question": "When experiencing stress, you tend to:",
        "options": [
            {"text": "Systematically address causes (C)", "dimensions": {"C": 4}},
            {"text": "Become emotionally overwhelmed (N)", "dimensions": {"N": 3}},
            {"text": "Seek novel solutions (O)", "dimensions": {"O": 2}},
            {"text": "Focus on others' needs (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 11,
        "question": "When encountering cultural differences, you typically:",
        "options": [
            {"text": "Analyze underlying social structures (O)", "dimensions": {"O": 4}},
            {"text": "Feel uncomfortable initially (N)", "dimensions": {"N": 3}},
            {"text": "Seek common ground (A)", "dimensions": {"A": 2}},
            {"text": "Organize cross-cultural exchanges (C)", "dimensions": {"C": 1}}
        ]
    },
    {
        "id": 12,
        "question": "Your approach to personal finances:",
        "options": [
            {"text": "Meticulous budgeting (C)", "dimensions": {"C": 4}},
            {"text": "Impulsive purchases (N)", "dimensions": {"N": 3}},
            {"text": "Ethical investing (A)", "dimensions": {"A": 2}},
            {"text": "Innovative wealth strategies (O)", "dimensions": {"O": 1}}
        ]
    },
    {
        "id": 13,
        "question": "When someone disagrees with you, you usually:",
        "options": [
            {"text": "Present logical counterarguments (C)", "dimensions": {"C": 4}},
            {"text": "Avoid confrontation (A)", "dimensions": {"A": 3}},
            {"text": "Enjoy the debate (E)", "dimensions": {"E": 2}},
            {"text": "Re-examine your position (O)", "dimensions": {"O": 1}}
        ]
    },
    {
        "id": 14,
        "question": "Your ideal learning environment:",
        "options": [
            {"text": "Structured curriculum (C)", "dimensions": {"C": 4}},
            {"text": "Social workshops (E)", "dimensions": {"E": 3}},
            {"text": "Self-directed exploration (O)", "dimensions": {"O": 2}},
            {"text": "Community-based projects (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 15,
        "question": "When facing ethical dilemmas:",
        "options": [
            {"text": "Apply universal principles (C)", "dimensions": {"C": 4}},
            {"text": "Consider emotional impacts (A)", "dimensions": {"A": 3}},
            {"text": "Seek innovative solutions (O)", "dimensions": {"O": 2}},
            {"text": "Consult others' opinions (E)", "dimensions": {"E": 1}}
        ]
    },
    {
        "id": 16,
        "question": "Your response to routine tasks:",
        "options": [
            {"text": "Systematize for efficiency (C)", "dimensions": {"C": 4}},
            {"text": "Find them calming (N)", "dimensions": {"N": 3}},
            {"text": "Seek to innovate processes (O)", "dimensions": {"O": 2}},
            {"text": "Delegate when possible (E)", "dimensions": {"E": 1}}
        ]
    },
    {
        "id": 17,
        "question": "When mentoring others:",
        "options": [
            {"text": "Create detailed development plans (C)", "dimensions": {"C": 4}},
            {"text": "Focus on emotional support (A)", "dimensions": {"A": 3}},
            {"text": "Encourage creative approaches (O)", "dimensions": {"O": 2}},
            {"text": "Build networking opportunities (E)", "dimensions": {"E": 1}}
        ]
    },
    {
        "id": 18,
        "question": "Your approach to health and fitness:",
        "options": [
            {"text": "Strict regimen (C)", "dimensions": {"C": 4}},
            {"text": "Social activities (E)", "dimensions": {"E": 3}},
            {"text": "Experimental techniques (O)", "dimensions": {"O": 2}},
            {"text": "Community wellness (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 19,
        "question": "When experiencing failure:",
        "options": [
            {"text": "Analyze mistakes systematically (C)", "dimensions": {"C": 4}},
            {"text": "Doubt future efforts (N)", "dimensions": {"N": 3}},
            {"text": "Seek alternative approaches (O)", "dimensions": {"O": 2}},
            {"text": "Seek reassurance (E)", "dimensions": {"E": 1}}
        ]
    },
    {
        "id": 20,
        "question": "Your approach to team leadership:",
        "options": [
            {"text": "Detailed role assignments (C)", "dimensions": {"C": 4}},
            {"text": "Democratic decision-making (E)", "dimensions": {"E": 3}},
            {"text": "Visionary direction (O)", "dimensions": {"O": 2}},
            {"text": "Harmony maintenance (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 21,
        "question": "When processing emotions:",
        "options": [
            {"text": "Logical analysis (C)", "dimensions": {"C": 4}},
            {"text": "Expressive sharing (E)", "dimensions": {"E": 3}},
            {"text": "Creative expression (O)", "dimensions": {"O": 2}},
            {"text": "Empathic consideration (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 22,
        "question": "Your approach to problem-solving:",
        "options": [
            {"text": "Step-by-step methodology (C)", "dimensions": {"C": 4}},
            {"text": "Brainstorming sessions (E)", "dimensions": {"E": 3}},
            {"text": "Lateral thinking (O)", "dimensions": {"O": 2}},
            {"text": "Consensus building (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 23,
        "question": "When learning new technology:",
        "options": [
            {"text": "Master official documentation (C)", "dimensions": {"C": 4}},
            {"text": "Learn through social interaction (E)", "dimensions": {"E": 3}},
            {"text": "Experiment freely (O)", "dimensions": {"O": 2}},
            {"text": "Help others learn (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 24,
        "question": "Your vacation preference:",
        "options": [
            {"text": "Detailed itinerary (C)", "dimensions": {"C": 4}},
            {"text": "Group tours (E)", "dimensions": {"E": 3}},
            {"text": "Adventure travel (O)", "dimensions": {"O": 2}},
            {"text": "Volunteer tourism (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 25,
        "question": "When managing conflicts:",
        "options": [
            {"text": "Establish clear protocols (C)", "dimensions": {"C": 4}},
            {"text": "Facilitate open dialogue (E)", "dimensions": {"E": 3}},
            {"text": "Find innovative compromises (O)", "dimensions": {"O": 2}},
            {"text": "Prioritize relationships (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 26,
        "question": "Your approach to personal growth:",
        "options": [
            {"text": "Structured learning plans (C)", "dimensions": {"C": 4}},
            {"text": "Social learning networks (E)", "dimensions": {"E": 3}},
            {"text": "Experimental self-discovery (O)", "dimensions": {"O": 2}},
            {"text": "Community service (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 27,
        "question": "When facing ambiguous situations:",
        "options": [
            {"text": "Create clear frameworks (C)", "dimensions": {"C": 4}},
            {"text": "Seek social validation (E)", "dimensions": {"E": 3}},
            {"text": "Explore possibilities (O)", "dimensions": {"O": 2}},
            {"text": "Follow group norms (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 28,
        "question": "Your response to artistic works:",
        "options": [
            {"text": "Analyze technical aspects (C)", "dimensions": {"C": 4}},
            {"text": "Share interpretations socially (E)", "dimensions": {"E": 3}},
            {"text": "Seek novel perspectives (O)", "dimensions": {"O": 2}},
            {"text": "Focus on emotional impact (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 29,
        "question": "When making career choices:",
        "options": [
            {"text": "Follow structured progression (C)", "dimensions": {"C": 4}},
            {"text": "Seek high-visibility roles (E)", "dimensions": {"E": 3}},
            {"text": "Pursue unconventional paths (O)", "dimensions": {"O": 2}},
            {"text": "Prioritize social impact (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 30,
        "question": "Your approach to time management:",
        "options": [
            {"text": "Detailed scheduling (C)", "dimensions": {"C": 4}},
            {"text": "Collaborative planning (E)", "dimensions": {"E": 3}},
            {"text": "Flexible adaptation (O)", "dimensions": {"O": 2}},
            {"text": "Accommodating others (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 39,
        "question": "When evaluating success:",
        "options": [
            {"text": "Measurable achievements (C)", "dimensions": {"C": 4}},
            {"text": "Social recognition (E)", "dimensions": {"E": 3}},
            {"text": "Personal growth (O)", "dimensions": {"O": 2}},
            {"text": "Community benefit (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 31,
        "question": "When receiving unexpected feedback:",
        "options": [
            {"text": "Systematically evaluate its validity (C)", "dimensions": {"C": 4}},
            {"text": "Seek second opinions (E)", "dimensions": {"E": 3}},
            {"text": "Consider alternative interpretations (O)", "dimensions": {"O": 2}},
            {"text": "Focus on the feedback giver's intentions (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 32,
        "question": "Your approach to professional development:",
        "options": [
            {"text": "Certification roadmaps (C)", "dimensions": {"C": 4}},
            {"text": "Networking events (E)", "dimensions": {"E": 3}},
            {"text": "Experimental learning (O)", "dimensions": {"O": 2}},
            {"text": "Mentorship programs (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 33,
        "question": "When encountering bureaucratic processes:",
        "options": [
            {"text": "Optimize for efficiency (C)", "dimensions": {"C": 4}},
            {"text": "Build relationships to navigate (E)", "dimensions": {"E": 3}},
            {"text": "Challenge established protocols (O)", "dimensions": {"O": 2}},
            {"text": "Ensure fair implementation (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 34,
        "question": "Your response to abstract concepts:",
        "options": [
            {"text": "Analyze logical structures (C)", "dimensions": {"C": 4}},
            {"text": "Discuss with colleagues (E)", "dimensions": {"E": 3}},
            {"text": "Explore metaphorical meanings (O)", "dimensions": {"O": 2}},
            {"text": "Connect to human experiences (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 35,
        "question": "When managing competing priorities:",
        "options": [
            {"text": "Create detailed matrices (C)", "dimensions": {"C": 4}},
            {"text": "Delegate strategically (E)", "dimensions": {"E": 3}},
            {"text": "Reinvent workflow systems (O)", "dimensions": {"O": 2}},
            {"text": "Align with team needs (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 36,
        "question": "Your approach to risk assessment:",
        "options": [
            {"text": "Quantitative models (C)", "dimensions": {"C": 4}},
            {"text": "Group consensus (E)", "dimensions": {"E": 3}},
            {"text": "Intuitive evaluation (O)", "dimensions": {"O": 2}},
            {"text": "Social impact analysis (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 37,
        "question": "When interpreting data patterns:",
        "options": [
            {"text": "Statistical verification (C)", "dimensions": {"C": 4}},
            {"text": "Collaborative sense-making (E)", "dimensions": {"E": 3}},
            {"text": "Speculative hypotheses (O)", "dimensions": {"O": 2}},
            {"text": "Ethical implications (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 38,
        "question": "Your strategy for complex negotiations:",
        "options": [
            {"text": "Detailed contingency planning (C)", "dimensions": {"C": 4}},
            {"text": "Persuasive communication (E)", "dimensions": {"E": 3}},
            {"text": "Creative problem-solving (O)", "dimensions": {"O": 2}},
            {"text": "Win-win solutions (A)", "dimensions": {"A": 1}}
        ]
    },
    {
        "id": 40,
        "question": "Your approach to moral dilemmas:",
        "options": [
            {"text": "Follow established principles (C)", "dimensions": {"C": 4}},
            {"text": "Consider emotional impacts (A)", "dimensions": {"A": 3}},
            {"text": "Explore philosophical aspects (O)", "dimensions": {"O": 2}},
            {"text": "Seek group consensus (E)", "dimensions": {"E": 1}}
        ]
    }
]
