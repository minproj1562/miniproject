CATEGORIES = {
    "O": "Openness",
    "C": "Conscientiousness",
    "E": "Extraversion",
    "A": "Agreeableness",
    "N": "Neuroticism"
}
PERSONALITY_QUESTIONS = [ { "id": 1,
        "question": "When making important decisions, you tend to:",
        "options": [
            "Analyze all possible outcomes systematically (C)",
            "Consult with multiple people (E)",
            "Go with your gut feeling (O)",
            "Consider others' needs first (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {"id": 2,
        "question": "Your approach to deadlines is typically:",
        "options": [
            "Complete tasks weeks in advance (C)",
            "Work best under pressure (N)",
            "Adjust timelines as needed (O)",
            "Collaborate to meet targets (A)"
        ],
        "dimensions": {"C": 4, "N": 3, "O": 2, "A": 1}
    },
{
        "id": 3,
        "question": "In social gatherings, you usually:",
        "options": [
            "Initiate conversations (E)",
            "Observe before participating (N)",
            "Discuss abstract ideas (O)",
            "Ensure everyone feels included (A)"
        ],
        "dimensions": {"E": 4, "N": 3, "O": 2, "A": 1}
    },
    {
        "id": 4,
        "question": "When faced with criticism, you:",
        "options": [
            "Objectively analyze its validity (C)",
            "Take it personally (N)",
            "Consider alternative perspectives (O)",
            "Focus on maintaining harmony (A)"
        ],
        "dimensions": {"C": 4, "N": 3, "O": 2, "A": 1}
    },
    {
        "id": 5,
        "question": "Your ideal weekend involves:",
        "options": [
            "Structured activities (C)",
            "Social events (E)",
            "Creative exploration (O)",
            "Helping community (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 6,
        "question": "When learning something new, you prefer:",
        "options": [
            "Step-by-step instructions (C)",
            "Group learning (E)",
            "Experimental approach (O)",
            "Mentorship relationships (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 7,
        "question": "Your reaction to sudden changes is typically:",
        "options": [
            "Create contingency plans (C)",
            "Experience anxiety (N)",
            "Find it exciting (O)",
            "Adapt to maintain peace (A)"
        ],
        "dimensions": {"C": 4, "N": 3, "O": 2, "A": 1}
    },
    {
        "id": 8,
        "question": "In team projects, you usually:",
        "options": [
            "Organize workflow (C)",
            "Motivate team members (E)",
            "Propose innovative solutions (O)",
            "Resolve conflicts (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 9,
        "question": "Your approach to personal goals:",
        "options": [
            "Detailed 5-year plan (C)",
            "Flexible aspirations (O)",
            "Socially influenced (E)",
            "Altruistically motivated (A)"
        ],
        "dimensions": {"C": 4, "O": 3, "E": 2, "A": 1}
    },
    {
        "id": 10,
        "question": "When experiencing stress, you tend to:",
        "options": [
            "Systematically address causes (C)",
            "Become emotionally overwhelmed (N)",
            "Seek novel solutions (O)",
            "Focus on others' needs (A)"
        ],
        "dimensions": {"C": 4, "N": 3, "O": 2, "A": 1}
    },
    {
        "id": 11,
        "question": "When encountering cultural differences, you typically:",
        "options": [
            "Analyze underlying social structures (O)",
            "Feel uncomfortable initially (N)",
            "Seek common ground (A)",
            "Organize cross-cultural exchanges (C)"
        ],
        "dimensions": {"O": 4, "N": 3, "A": 2, "C": 1}
    },
    {
        "id": 12,
        "question": "Your approach to personal finances:",
        "options": [
            "Meticulous budgeting (C)",
            "Impulsive purchases (N)",
            "Ethical investing (A)",
            "Innovative wealth strategies (O)"
        ],
        "dimensions": {"C": 4, "N": 3, "A": 2, "O": 1}
    },
    {
        "id": 13,
        "question": "When someone disagrees with you, you usually:",
        "options": [
            "Present logical counterarguments (C)",
            "Avoid confrontation (A)",
            "Enjoy the debate (E)",
            "Re-examine your position (O)"
        ],
        "dimensions": {"C": 4, "A": 3, "E": 2, "O": 1}
    },
    {
        "id": 14,
        "question": "Your ideal learning environment:",
        "options": [
            "Structured curriculum (C)",
            "Social workshops (E)",
            "Self-directed exploration (O)",
            "Community-based projects (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 15,
        "question": "When facing ethical dilemmas:",
        "options": [
            "Apply universal principles (C)",
            "Consider emotional impacts (A)",
            "Seek innovative solutions (O)",
            "Consult others' opinions (E)"
        ],
        "dimensions": {"C": 4, "A": 3, "O": 2, "E": 1}
    },
    {
        "id": 16,
        "question": "Your response to routine tasks:",
        "options": [
            "Systematize for efficiency (C)",
            "Find them calming (N)",
            "Seek to innovate processes (O)",
            "Delegate when possible (E)"
        ],
        "dimensions": {"C": 4, "N": 3, "O": 2, "E": 1}
    },
    {
        "id": 17,
        "question": "When mentoring others:",
        "options": [
            "Create detailed development plans (C)",
            "Focus on emotional support (A)",
            "Encourage creative approaches (O)",
            "Build networking opportunities (E)"
        ],
        "dimensions": {"C": 4, "A": 3, "O": 2, "E": 1}
    },
    {
        "id": 18,
        "question": "Your approach to health and fitness:",
        "options": [
            "Strict regimen (C)",
            "Social activities (E)",
            "Experimental techniques (O)",
            "Community wellness (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 19,
        "question": "When experiencing failure:",
        "options": [
            "Analyze mistakes systematically (C)",
            "Doubt future efforts (N)",
            "Seek alternative approaches (O)",
            "Seek reassurance (E)"
        ],
        "dimensions": {"C": 4, "N": 3, "O": 2, "E": 1}
    },
    {
        "id": 20,
        "question": "Your approach to team leadership:",
        "options": [
            "Detailed role assignments (C)",
            "Democratic decision-making (E)",
            "Visionary direction (O)",
            "Harmony maintenance (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 21,
        "question": "When processing emotions:",
        "options": [
            "Logical analysis (C)",
            "Expressive sharing (E)",
            "Creative expression (O)",
            "Empathic consideration (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 22,
        "question": "Your approach to problem-solving:",
        "options": [
            "Step-by-step methodology (C)",
            "Brainstorming sessions (E)",
            "Lateral thinking (O)",
            "Consensus building (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 23,
        "question": "When learning new technology:",
        "options": [
            "Master official documentation (C)",
            "Learn through social interaction (E)",
            "Experiment freely (O)",
            "Help others learn (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 24,
        "question": "Your vacation preference:",
        "options": [
            "Detailed itinerary (C)",
            "Group tours (E)",
            "Adventure travel (O)",
            "Volunteer tourism (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 25,
        "question": "When managing conflicts:",
        "options": [
            "Establish clear protocols (C)",
            "Facilitate open dialogue (E)",
            "Find innovative compromises (O)",
            "Prioritize relationships (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 26,
        "question": "Your approach to personal growth:",
        "options": [
            "Structured learning plans (C)",
            "Social learning networks (E)",
            "Experimental self-discovery (O)",
            "Community service (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 27,
        "question": "When facing ambiguous situations:",
        "options": [
            "Create clear frameworks (C)",
            "Seek social validation (E)",
            "Explore possibilities (O)",
            "Follow group norms (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 28,
        "question": "Your response to artistic works:",
        "options": [
            "Analyze technical aspects (C)",
            "Share interpretations socially (E)",
            "Seek novel perspectives (O)",
            "Focus on emotional impact (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 29,
        "question": "When making career choices:",
        "options": [
            "Follow structured progression (C)",
            "Seek high-visibility roles (E)",
            "Pursue unconventional paths (O)",
            "Prioritize social impact (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 30,
        "question": "Your approach to time management:",
        "options": [
            "Detailed scheduling (C)",
            "Collaborative planning (E)",
            "Flexible adaptation (O)",
            "Accommodating others (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 39,
        "question": "When evaluating success:",
        "options": [
            "Measurable achievements (C)",
            "Social recognition (E)",
            "Personal growth (O)",
            "Community benefit (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
        {
        "id": 31,
        "question": "When receiving unexpected feedback:",
        "options": [
            "Systematically evaluate its validity (C)",
            "Seek second opinions (E)", 
            "Consider alternative interpretations (O)",
            "Focus on the feedback giver's intentions (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 32,
        "question": "Your approach to professional development:",
        "options": [
            "Certification roadmaps (C)",
            "Networking events (E)",
            "Experimental learning (O)",
            "Mentorship programs (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 33,
        "question": "When encountering bureaucratic processes:",
        "options": [
            "Optimize for efficiency (C)",
            "Build relationships to navigate (E)",
            "Challenge established protocols (O)",
            "Ensure fair implementation (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 34,
        "question": "Your response to abstract concepts:",
        "options": [
            "Analyze logical structures (C)",
            "Discuss with colleagues (E)",
            "Explore metaphorical meanings (O)",
            "Connect to human experiences (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 35, 
        "question": "When managing competing priorities:",
        "options": [
            "Create detailed matrices (C)",
            "Delegate strategically (E)",
            "Reinvent workflow systems (O)",
            "Align with team needs (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 36,
        "question": "Your approach to risk assessment:",
        "options": [
            "Quantitative models (C)",
            "Group consensus (E)",
            "Intuitive evaluation (O)",
            "Social impact analysis (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 37,
        "question": "When interpreting data patterns:",
        "options": [
            "Statistical verification (C)",
            "Collaborative sense-making (E)",
            "Speculative hypotheses (O)",
            "Ethical implications (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 38,
        "question": "Your strategy for complex negotiations:",
        "options": [
            "Detailed contingency planning (C)",
            "Persuasive communication (E)",
            "Creative problem-solving (O)",
            "Win-win solutions (A)"
        ],
        "dimensions": {"C": 4, "E": 3, "O": 2, "A": 1}
    },
    {
        "id": 40,
        "question": "Your approach to moral dilemmas:",
        "options": [
            "Follow established principles (C)",
            "Consider emotional impacts (A)",
            "Explore philosophical aspects (O)",
            "Seek group consensus (E)"
        ],
        "dimensions": {"C": 4, "A": 3, "O": 2, "E": 1}
    }]