APTITUDE_QUESTIONS = {
    "Mathematics": {
        "easy": [
            {
                "id": "M1-E",
                "type": "numerical",
                "text": "Solve: 15 + 8 × 3 ÷ 4",
                "options": ["21", "18.5", "19.5", "20.25"],
                "correct": 0,
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
            },
            {
                "id": "M7-E",
                "type": "arithmetic",
                "text": "What is 20% of 150?",
                "options": ["20", "25", "30", "35"],
                "correct": 2,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.8}
            },
            {
                "id": "M10-E",
                "type": "fractions",
                "text": "What is 1/2 + 1/4?",
                "options": ["1/4", "3/4", "1/2", "1"],
                "correct": 1,
                "time_limit": 50,
                "irt_params": {"difficulty": -1.1, "discrimination": 0.7}
            },
            {
                "id": "M11-E",
                "type": "number_system",
                "text": "Which is the smallest number: 45, 54, 35, 43?",
                "options": ["35", "43", "45", "54"],
                "correct": 0,
                "time_limit": 40,
                "irt_params": {"difficulty": -1.3, "discrimination": 0.9}
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
            },
            {
                "id": "M8-M",
                "type": "trigonometry",
                "text": "In a right triangle, if one angle is 30° and the hypotenuse is 10, what is the length of the opposite side?",
                "options": ["3", "5", "6", "8"],
                "correct": 1,
                "time_limit": 90,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.0}
            },
            {
                "id": "M12-M",
                "type": "geometry",
                "text": "What is the circumference of a circle with radius 7 cm? (Use π = 22/7)",
                "options": ["44 cm", "48 cm", "50 cm", "52 cm"],
                "correct": 0,
                "time_limit": 80,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.0}
            },
            {
                "id": "M13-M",
                "type": "arithmetic",
                "text": "A shop offers a 15% discount on a $200 item. What is the sale price?",
                "options": ["$160", "$170", "$180", "$190"],
                "correct": 1,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.5, "discrimination": 1.1}
            }
        ],
        "hard": [
            {
                "id": "M3-H",
                "type": "calculus",
                "text": "What is the derivative of f(x) = 3x² + 2x - 5?",
                "options": ["6x + 2", "6x + 5", "3x + 2", "6x - 5"],
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
            },
            {
                "id": "M9-H",
                "type": "linear algebra",
                "text": "What is the determinant of the matrix [[2, 3], [1, 4]]?",
                "options": ["5", "7", "8", "11"],
                "correct": 0,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.9, "discrimination": 1.3}
            },
            {
                "id": "M14-H",
                "type": "equations",
                "text": "Solve: x² - 5x + 6 = 0",
                "options": ["x = 2, 3", "x = 1, 4", "x = 3, 5", "x = 2, 4"],
                "correct": 0,
                "time_limit": 130,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            },
            {
                "id": "M15-H",
                "type": "geometry",
                "text": "What is the volume of a cylinder with radius 3 cm and height 5 cm? (Use π = 3.14)",
                "options": ["141.3 cm³", "144.2 cm³", "150.8 cm³", "153.6 cm³"],
                "correct": 0,
                "time_limit": 140,
                "irt_params": {"difficulty": 1.8, "discrimination": 1.3}
            }
        ]
    },
    "Logical Reasoning": {
        "easy": [
            {
                "id": "LR1-E",
                "type": "pattern",
                "text": "Complete the sequence: 2, 4, 6, 8, ___",
                "options": ["9", "10", "11", "12"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -1.0, "discrimination": 0.9}
            },
            {
                "id": "LR4-E",
                "type": "analogy",
                "text": "Pen is to Write as Spoon is to ___",
                "options": ["Eat", "Cook", "Stir", "Cut"],
                "correct": 0,
                "time_limit": 40,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.8}
            },
            {
                "id": "LR7-E",
                "type": "classification",
                "text": "Which does not belong: Cat, Dog, Bird, Car?",
                "options": ["Cat", "Dog", "Bird", "Car"],
                "correct": 3,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.8, "discrimination": 0.7}
            },
            {
                "id": "LR10-E",
                "type": "sequence",
                "text": "What comes next: 1, 3, 5, 7, ___?",
                "options": ["8", "9", "10", "11"],
                "correct": 1,
                "time_limit": 40,
                "irt_params": {"difficulty": -1.1, "discrimination": 0.8}
            },
            {
                "id": "LR11-E",
                "type": "relationship",
                "text": "If Monday is the 1st day, what day is the 4th?",
                "options": ["Tuesday", "Wednesday", "Thursday", "Friday"],
                "correct": 2,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.7}
            }
        ],
        "moderate": [
            {
                "id": "LR2-M",
                "type": "deductive",
                "text": "All birds have feathers. Some feathers are white. Therefore:",
                "options": [
                    "All birds are white",
                    "Some birds may have white feathers",
                    "No birds are white",
                    "Feathers cannot be white"
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
            },
            {
                "id": "LR8-M",
                "type": "coding-decoding",
                "text": "If 'BAT' is coded as 'DCV', how is 'RAT' coded?",
                "options": ["TCV", "UDX", "VDW", "WEX"],
                "correct": 1,
                "time_limit": 90,
                "irt_params": {"difficulty": 0.9, "discrimination": 1.0}
            },
            {
                "id": "LR12-M",
                "type": "pattern",
                "text": "Complete: 3, 6, 12, 24, ___",
                "options": ["36", "48", "60", "72"],
                "correct": 1,
                "time_limit": 80,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.1}
            },
            {
                "id": "LR13-M",
                "type": "logical_order",
                "text": "Arrange in order: Eat, Cook, Serve",
                "options": ["Cook, Eat, Serve", "Eat, Cook, Serve", "Serve, Cook, Eat", "Cook, Serve, Eat"],
                "correct": 0,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.0}
            }
        ],
        "hard": [
            {
                "id": "LR3-H",
                "type": "analytical",
                "text": "If 2★3 = 7, 4★5 = 23, then 3★4 = ___",
                "options": ["13", "14", "15", "16"],
                "correct": 2,
                "time_limit": 150,
                "irt_params": {"difficulty": 2.0, "discrimination": 1.4}
            },
            {
                "id": "LR6-H",
                "type": "logic_puzzle",
                "text": "Three students rank 1st, 2nd, 3rd in a quiz. A is not last, B is ahead of C. Who is 2nd?",
                "options": ["A", "B", "C", "Cannot determine"],
                "correct": 0,
                "time_limit": 180,
                "irt_params": {"difficulty": 2.2, "discrimination": 1.5}
            },
            {
                "id": "LR9-H",
                "type": "conditional",
                "text": "If P implies Q and Q implies R, which is true if P is true?",
                "options": ["R is false", "R is true", "Q is false", "Cannot determine"],
                "correct": 1,
                "time_limit": 150,
                "irt_params": {"difficulty": 2.1, "discrimination": 1.3}
            },
            {
                "id": "LR14-H",
                "type": "sequence",
                "text": "What’s next: 1, 4, 9, 16, ___?",
                "options": ["20", "25", "30", "36"],
                "correct": 1,
                "time_limit": 140,
                "irt_params": {"difficulty": 1.9, "discrimination": 1.4}
            },
            {
                "id": "LR15-H",
                "type": "puzzle",
                "text": "If 5 people shake hands once with each other, how many handshakes occur?",
                "options": ["10", "15", "20", "25"],
                "correct": 0,
                "time_limit": 160,
                "irt_params": {"difficulty": 2.0, "discrimination": 1.3}
            }
        ]
    },
    "Verbal Ability": {
        "easy": [
            {
                "id": "VA1-E",
                "type": "vocabulary",
                "text": "Select the antonym of HAPPY:",
                "options": ["Joyful", "Sad", "Excited", "Content"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.8, "discrimination": 0.7}
            },
            {
                "id": "VA4-E",
                "type": "synonym",
                "text": "Find a synonym for 'Quick':",
                "options": ["Fast", "Slow", "Lazy", "Quiet"],
                "correct": 0,
                "time_limit": 40,
                "irt_params": {"difficulty": -0.7, "discrimination": 0.8}
            },
            {
                "id": "VA7-E",
                "type": "sentence_correction",
                "text": "Choose the correct sentence: ",
                "options": [
                    "He run to school every day.",
                    "He runs to school every day.",
                    "He running to school every day.",
                    "He runned to school every day."
                ],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.6, "discrimination": 0.7}
            },
            {
                "id": "VA10-E",
                "type": "vocabulary",
                "text": "What does 'Bright' mean?",
                "options": ["Dark", "Shiny", "Dull", "Quiet"],
                "correct": 1,
                "time_limit": 40,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.8}
            },
            {
                "id": "VA11-E",
                "type": "spelling",
                "text": "Which is spelled correctly?",
                "options": ["Recieve", "Receive", "Receeve", "Recive"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.7, "discrimination": 0.7}
            }
        ],
        "moderate": [
            {
                "id": "VA2-M",
                "type": "comprehension",
                "text": "'The book was enthralling.' What does 'enthralling' mean?",
                "options": ["Boring", "Fascinating", "Confusing", "Long"],
                "correct": 1,
                "time_limit": 60,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.0}
            },
            {
                "id": "VA5-M",
                "type": "sentence_completion",
                "text": "The ___ weather forced us to cancel the picnic.",
                "options": ["pleasant", "stormy", "calm", "warm"],
                "correct": 1,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.1}
            },
            {
                "id": "VA8-M",
                "type": "reading_comprehension",
                "text": "Passage: 'Forests help regulate climate.' What is the main idea?",
                "options": [
                    "Forests are unimportant",
                    "Forests affect climate",
                    "Climate changes forests",
                    "Forests only store water"
                ],
                "correct": 1,
                "time_limit": 90,
                "irt_params": {"difficulty": 0.8, "discrimination": 1.0}
            },
            {
                "id": "VA12-M",
                "type": "idioms",
                "text": "What does 'Break the ice' mean?",
                "options": ["Start a fight", "Make people comfortable", "End a conversation", "Freeze something"],
                "correct": 1,
                "time_limit": 60,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.1}
            },
            {
                "id": "VA13-M",
                "type": "grammar",
                "text": "Which is correct: 'She ___ to the store yesterday.'?",
                "options": ["go", "goes", "went", "going"],
                "correct": 2,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.0}
            }
        ],
        "hard": [
            {
                "id": "VA3-H",
                "type": "critical_reasoning",
                "text": "Which weakens: 'Homework improves grades because students practice more'?",
                "options": [
                    "Practice time is short",
                    "Grades drop despite homework",
                    "Students enjoy homework",
                    "Teachers assign more homework"
                ],
                "correct": 1,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.5, "discrimination": 1.3}
            },
            {
                "id": "VA6-H",
                "type": "analogies",
                "text": "Rain : Wet :: Sun : ___",
                "options": ["Dry", "Hot", "Bright", "Cold"],
                "correct": 2,
                "time_limit": 100,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            },
            {
                "id": "VA9-H",
                "type": "inferences",
                "text": "If 'All students passed the exam,' what can be inferred?",
                "options": [
                    "Some failed",
                    "Every student passed",
                    "The exam was easy",
                    "Teachers helped"
                ],
                "correct": 1,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.6, "discrimination": 1.2}
            },
            {
                "id": "VA14-H",
                "type": "vocabulary",
                "text": "What does 'Ephemeral' mean?",
                "options": ["Lasting forever", "Short-lived", "Bright", "Complex"],
                "correct": 1,
                "time_limit": 100,
                "irt_params": {"difficulty": 1.8, "discrimination": 1.3}
            },
            {
                "id": "VA15-H",
                "type": "comprehension",
                "text": "Passage: 'The policy was contentious.' What does this imply?",
                "options": [
                    "Widely accepted",
                    "Caused disagreement",
                    "Simple to understand",
                    "Ineffective"
                ],
                "correct": 1,
                "time_limit": 130,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            }
        ]
    },
    "Science": {
        "easy": [
            {
                "id": "SC1-E",
                "type": "biology",
                "text": "Which gas do plants use for photosynthesis?",
                "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -1.0, "discrimination": 0.8}
            },
            {
                "id": "SC2-E",
                "type": "physics",
                "text": "What is the unit of force?",
                "options": ["Newton", "Watt", "Joule", "Meter"],
                "correct": 0,
                "time_limit": 40,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.7}
            },
            {
                "id": "SC3-E",
                "type": "chemistry",
                "text": "What is the chemical symbol for water?",
                "options": ["H₂O", "CO₂", "O₂", "N₂"],
                "correct": 0,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.8, "discrimination": 0.8}
            },
            {
                "id": "SC16-E",
                "type": "anatomy",
                "text": "Which organ pumps blood in the human body? (Relevant to Doctor, Nurse)",
                "options": ["Lungs", "Heart", "Brain", "Kidneys"],
                "correct": 1,
                "time_limit": 40,
                "irt_params": {"difficulty": -1.1, "discrimination": 0.7}
            },
            {
                "id": "SC17-E",
                "type": "ecology",
                "text": "What is the primary source of energy for Earth’s ecosystems? (Relevant to Wildlife Biologist)",
                "options": ["Moon", "Sun", "Wind", "Water"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.8}
            }
        ],
        "moderate": [
            {
                "id": "SC4-M",
                "type": "biology",
                "text": "What part of the cell contains DNA?",
                "options": ["Cytoplasm", "Nucleus", "Membrane", "Mitochondria"],
                "correct": 1,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.0}
            },
            {
                "id": "SC5-M",
                "type": "physics",
                "text": "If an object moves 20 meters in 4 seconds, what is its speed? (Relevant to Mechanical Engineer)",
                "options": ["5 m/s", "10 m/s", "15 m/s", "20 m/s"],
                "correct": 0,
                "time_limit": 90,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.1}
            },
            {
                "id": "SC6-M",
                "type": "chemistry",
                "text": "What gas, discovered on the sun before Earth, is second most abundant in the universe? (Relevant to Astrophysicist)",
                "options": ["Hydrogen", "Helium", "Oxygen", "Nitrogen"],
                "correct": 1,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.8, "discrimination": 1.0}
            },
            {
                "id": "SC18-M",
                "type": "anatomy",
                "text": "Which bone is the longest in the human body? (Relevant to Doctor, Nurse)",
                "options": ["Skull", "Femur", "Spine", "Humerus"],
                "correct": 1,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.1}
            },
            {
                "id": "SC19-M",
                "type": "environmental_science",
                "text": "What gas is most responsible for the greenhouse effect? (Relevant to Environmental Engineer)",
                "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"],
                "correct": 2,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.0}
            }
        ],
        "hard": [
            {
                "id": "SC7-H",
                "type": "biology",
                "text": "What process converts glucose into energy in cells?",
                "options": ["Photosynthesis", "Respiration", "Diffusion", "Osmosis"],
                "correct": 1,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.5, "discrimination": 1.3}
            },
            {
                "id": "SC8-H",
                "type": "physics",
                "text": "A 2 kg object accelerates at 3 m/s². What is the force? (Relevant to Mechanical Engineer)",
                "options": ["5 N", "6 N", "8 N", "10 N"],
                "correct": 1,
                "time_limit": 150,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            },
            {
                "id": "SC9-H",
                "type": "chemistry",
                "text": "What is the pH of a solution with [H⁺] = 10⁻⁸ M? (Relevant to Medical Researcher)",
                "options": ["6", "7", "8", "9"],
                "correct": 2,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.6, "discrimination": 1.2}
            },
            {
                "id": "SC20-H",
                "type": "astronomy",
                "text": "What force keeps planets in orbit around the Sun? (Relevant to Astrophysicist)",
                "options": ["Magnetism", "Gravity", "Friction", "Nuclear Force"],
                "correct": 1,
                "time_limit": 140,
                "irt_params": {"difficulty": 1.8, "discrimination": 1.3}
            },
            {
                "id": "SC21-H",
                "type": "anatomy",
                "text": "Which part of the brain controls balance and coordination? (Relevant to Doctor)",
                "options": ["Cerebrum", "Cerebellum", "Medulla", "Thalamus"],
                "correct": 1,
                "time_limit": 130,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            }
        ]
    },
    "Spatial Reasoning": {
        "easy": [
            {
                "id": "SR1-E",
                "type": "visualization",
                "text": "If you fold a square paper in half vertically, what shape do you get?",
                "options": ["Square", "Rectangle", "Triangle", "Circle"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -1.0, "discrimination": 0.8}
            },
            {
                "id": "SR2-E",
                "type": "rotation",
                "text": "If a cube is rotated 90° clockwise, how many faces are visible from the front?",
                "options": ["1", "2", "3", "4"],
                "correct": 0,
                "time_limit": 40,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.7}
            },
            {
                "id": "SR3-E",
                "type": "pattern",
                "text": "Which shape fits next: Circle, Square, Circle, ___?",
                "options": ["Triangle", "Square", "Circle", "Rectangle"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.8, "discrimination": 0.8}
            },
            {
                "id": "SR4-E",
                "type": "visualization",
                "text": "How many sides does a cube have?",
                "options": ["4", "6", "8", "12"],
                "correct": 1,
                "time_limit": 40,
                "irt_params": {"difficulty": -1.1, "discrimination": 0.7}
            },
            {
                "id": "SR5-E",
                "type": "spatial_relation",
                "text": "If a car is facing north and turns left, which direction is it now facing?",
                "options": ["East", "West", "South", "North"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.8}
            }
        ],
        "moderate": [
            {
                "id": "SR6-M",
                "type": "visualization",
                "text": "If a flat map is folded into a cube, how many edges will it have?",
                "options": ["6", "8", "12.ConcurrentModificationException", "16"],
                "correct": 2,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.0}
            },
            {
                "id": "SR7-M",
                "type": "rotation",
                "text": "A triangle is rotated 180°. How does its orientation change?",
                "options": ["Flips upside down", "Stays the same", "Shifts left", "Shrinks"],
                "correct": 0,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.1}
            },
            {
                "id": "SR8-M",
                "type": "spatial_relation",
                "text": "If you stack two cubes vertically, how many faces are visible?",
                "options": ["6", "8", "10", "12"],
                "correct": 2,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.8, "discrimination": 1.0}
            },
            {
                "id": "SR9-M",
                "type": "design",
                "text": "How many windows can fit on a wall 10m long if each window is 2m wide? (Relevant to Urban Planner)",
                "options": ["3", "4", "5", "6"],
                "correct": 2,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.1}
            },
            {
                "id": "SR10-M",
                "type": "visualization",
                "text": "If a cylinder is cut in half lengthwise, what shape is the cross-section?",
                "options": ["Circle", "Rectangle", "Triangle", "Oval"],
                "correct": 1,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.0}
            }
        ],
        "hard": [
            {
                "id": "SR11-H",
                "type": "rotation",
                "text": "A 3D object is rotated 90° around its vertical axis. How many faces change position?",
                "options": ["2", "4", "6", "All"],
                "correct": 1,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.5, "discrimination": 1.3}
            },
            {
                "id": "SR12-H",
                "type": "visualization",
                "text": "If a sphere is sliced through its center, what shape is the cross-section?",
                "options": ["Circle", "Ellipse", "Square", "Triangle"],
                "correct": 0,
                "time_limit": 130,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            },
            {
                "id": "SR13-H",
                "type": "spatial_relation",
                "text": "A building design has 4 floors, each with 6 windows. If 2 floors face north and 2 face south, how many windows face north?",
                "options": ["6", "12", "18", "24"],
                "correct": 1,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.6, "discrimination": 1.2}
            },
            {
                "id": "SR14-H",
                "type": "design",
                "text": "A gear with 12 teeth meshes with one having 36 teeth. How many turns does the smaller gear make for one turn of the larger? (Relevant to Mechanical Engineer)",
                "options": ["1", "2", "3", "4"],
                "correct": 2,
                "time_limit": 140,
                "irt_params": {"difficulty": 1.8, "discrimination": 1.3}
            },
            {
                "id": "SR15-H",
                "type": "visualization",
                "text": "If a cube is painted on all faces and cut into 27 smaller cubes, how many have 3 painted faces? (Relevant to Graphic Designer)",
                "options": ["6", "8", "12", "16"],
                "correct": 1,
                "time_limit": 130,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            }
        ]
    },
    "History": {
        "easy": [
            {
                "id": "H1-E",
                "type": "chronology",
                "text": "Who was the first President of the United States?",
                "options": ["Abraham Lincoln", "George Washington", "Thomas Jefferson", "John Adams"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -1.0, "discrimination": 0.8}
            },
            {
                "id": "H2-E",
                "type": "events",
                "text": "In which year did Christopher Columbus first reach the Americas?",
                "options": ["1492", "1519", "1607", "1776"],
                "correct": 0,
                "time_limit": 40,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.7}
            },
            {
                "id": "H3-E",
                "type": "figures",
                "text": "Which leader is known for uniting ancient Egypt?",
                "options": ["Cleopatra", "Narmer", "Ramses II", "Tutankhamun"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.8, "discrimination": 0.8}
            },
            {
                "id": "H16-E",
                "type": "events",
                "text": "Which war ended with the signing of the Treaty of Versailles? (Relevant to Lawyer)",
                "options": ["World War I", "World War II", "American Civil War", "Napoleonic Wars"],
                "correct": 0,
                "time_limit": 40,
                "irt_params": {"difficulty": -1.1, "discrimination": 0.7}
            },
            {
                "id": "H17-E",
                "type": "civilizations",
                "text": "Which ancient civilization built the pyramids of Giza?",
                "options": ["Romans", "Greeks", "Egyptians", "Mesopotamians"],
                "correct": 2,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.8}
            }
        ],
        "moderate": [
            {
                "id": "H6-M",
                "type": "events",
                "text": "Which event marked the beginning of the French Revolution?",
                "options": ["Storming of the Bastille", "Execution of Louis XVI", "Reign of Terror", "Napoleon’s Coup"],
                "correct": 0,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.0}
            },
            {
                "id": "H7-M",
                "type": "figures",
                "text": "Who was the leader of the Indian independence movement known for nonviolent resistance?",
                "options": ["Jawaharlal Nehru", "Subhas Chandra Bose", "Mahatma Gandhi", "Bhagat Singh"],
                "correct": 2,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.1}
            },
            {
                "id": "H8-M",
                "type": "chronology",
                "text": "In which century did the Industrial Revolution begin? (Relevant to Business Manager)",
                "options": ["16th", "17th", "18th", "19th"],
                "correct": 2,
                "time_limit": 60,
                "irt_params": {"difficulty": 0.5, "discrimination": 1.0}
            },
            {
                "id": "H18-M",
                "type": "events",
                "text": "Which battle in 1066 led to the Norman conquest of England?",
                "options": ["Battle of Agincourt", "Battle of Hastings", "Battle of Waterloo", "Battle of Bosworth"],
                "correct": 1,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.1}
            },
            {
                "id": "H19-M",
                "type": "legal_history",
                "text": "Which document, signed in 1215, limited the power of the English king? (Relevant to Lawyer)",
                "options": ["Bill of Rights", "Magna Carta", "Declaration of Independence", "Constitution"],
                "correct": 1,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.0}
            }
        ],
        "hard": [
            {
                "id": "H11-H",
                "type": "causation",
                "text": "What was a primary cause of the American Civil War?",
                "options": ["Tax disputes", "Slavery", "Foreign invasion", "Industrial decline"],
                "correct": 1,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.5, "discrimination": 1.3}
            },
            {
                "id": "H12-H",
                "type": "events",
                "text": "Which treaty ended the Thirty Years’ War in 1648?",
                "options": ["Treaty of Utrecht", "Peace of Westphalia", "Treaty of Paris", "Treaty of Tordesillas"],
                "correct": 1,
                "time_limit": 130,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            },
            {
                "id": "H13-H",
                "type": "figures",
                "text": "Who was the Russian leader during the October Revolution of 1917?",
                "options": ["Vladimir Lenin", "Joseph Stalin", "Nicholas II", "Leon Trotsky"],
                "correct": 0,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.6, "discrimination": 1.2}
            },
            {
                "id": "H20-H",
                "type": "chronology",
                "text": "Which event occurred first? (Relevant to Teacher)",
                "options": [
                    "Fall of the Roman Empire (476 CE)",
                    "Discovery of America (1492)",
                    "French Revolution (1789)",
                    "World War I (1914)"
                ],
                "correct": 0,
                "time_limit": 140,
                "irt_params": {"difficulty": 1.8, "discrimination": 1.3}
            },
            {
                "id": "H21-H",
                "type": "civilizations",
                "text": "Which dynasty built the Great Wall of China to its greatest extent?",
                "options": ["Qin", "Han", "Tang", "Ming"],
                "correct": 3,
                "time_limit": 130,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            }
        ]
    },
    "Geography": {
        "easy": [
            {
                "id": "G1-E",
                "type": "locations",
                "text": "Which continent is home to the Sahara Desert?",
                "options": ["Asia", "Africa", "Australia", "South America"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -1.0, "discrimination": 0.8}
            },
            {
                "id": "G2-E",
                "type": "landforms",
                "text": "What is the longest river in the world?",
                "options": ["Amazon", "Nile", "Yangtze", "Mississippi"],
                "correct": 1,
                "time_limit": 40,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.7}
            },
            {
                "id": "G3-E",
                "type": "countries",
                "text": "Which country has the largest population?",
                "options": ["India", "China", "United States", "Russia"],
                "correct": 1,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.8, "discrimination": 0.8}
            },
            {
                "id": "G16-E",
                "type": "locations",
                "text": "Which ocean lies between North America and Europe?",
                "options": ["Pacific", "Atlantic", "Indian", "Arctic"],
                "correct": 1,
                "time_limit": 40,
                "irt_params": {"difficulty": -1.1, "discrimination": 0.7}
            },
            {
                "id": "G17-E",
                "type": "climate",
                "text": "Which season follows winter in the Northern Hemisphere?",
                "options": ["Spring", "Summer", "Autumn", "Winter"],
                "correct": 0,
                "time_limit": 45,
                "irt_params": {"difficulty": -0.9, "discrimination": 0.8}
            }
        ],
        "moderate": [
            {
                "id": "G6-M",
                "type": "locations",
                "text": "Which country is both in Europe and Asia?",
                "options": ["Greece", "Turkey", "Italy", "Spain"],
                "correct": 1,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.0}
            },
            {
                "id": "G7-M",
                "type": "landforms",
                "text": "Which mountain range separates Europe from Asia?",
                "options": ["Alps", "Himalayas", "Ural", "Andes"],
                "correct": 2,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.1}
            },
            {
                "id": "G8-M",
                "type": "climate",
                "text": "Which biome is characterized by low rainfall and extreme temperatures? (Relevant to Wildlife Biologist)",
                "options": ["Tundra", "Desert", "Rainforest", "Grassland"],
                "correct": 1,
                "time_limit": 60,
                "irt_params": {"difficulty": 0.5, "discrimination": 1.0}
            },
            {
                "id": "G18-M",
                "type": "urban_geography",
                "text": "Which city is known for its planned urban grid system in the US? (Relevant to Urban Planner)",
                "options": ["Boston", "New York", "Philadelphia", "Washington D.C."],
                "correct": 3,
                "time_limit": 70,
                "irt_params": {"difficulty": 0.6, "discrimination": 1.1}
            },
            {
                "id": "G19-M",
                "type": "locations",
                "text": "Which river forms part of the border between the US and Mexico?",
                "options": ["Mississippi", "Colorado", "Rio Grande", "Columbia"],
                "correct": 2,
                "time_limit": 75,
                "irt_params": {"difficulty": 0.7, "discrimination": 1.0}
            }
        ],
        "hard": [
            {
                "id": "G11-H",
                "type": "locations",
                "text": "Which country has the longest coastline?",
                "options": ["Russia", "Canada", "Australia", "United States"],
                "correct": 1,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.5, "discrimination": 1.3}
            },
            {
                "id": "G12-H",
                "type": "landforms",
                "text": "What is the deepest point in the Earth’s oceans?",
                "options": ["Mariana Trench", "Puerto Rico Trench", "Tonga Trench", "Java Trench"],
                "correct": 0,
                "time_limit": 130,
                "irt_params": {"difficulty": 1.7, "discrimination": 1.4}
            },
            {
                "id": "G13-H",
                "type": "climate",
                "text": "Which phenomenon causes seasonal wind shifts in South Asia? (Relevant to Environmental Engineer)",
                "options": ["El Niño", "Monsoon", "Tornado", "Jet Stream"],
                "correct": 1,
                "time_limit": 120,
                "irt_params": {"difficulty": 1.6, "discrimination": 1.2}
            },
            {
                "id": "G20-H",
                "type": "urban_geography",
                "text": "Which city’s urban sprawl covers the most area globally? (Relevant to Urban Planner)",
                "options": ["Tokyo", "New York", "Los Angeles", "Mexico City"],
                "correct": 0,
                "time_limit": 140,
                "irt_params": {"difficulty": 1.8, "discrimination": 1.3}
            },
            {
                "id": "G21-H",
                "type": "ecology",
                "text": "Which region is home to the largest biodiversity hotspot? (Relevant to Wildlife Biologist)",
                "options": ["Amazon Rainforest", "Sahara Desert", "Arctic Tundra", "Great Barrier Reef"],
                "correct": 0,
                "time_limit": 130,
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
            "spatial": 50,
            "science": 40,
            "history": 20,
            "geography": 20
        },
        "skills": {"required": 75},
        "resources": [
            {"name": "Learn Python on Codecademy", "url": "https://www.codecademy.com/learn/learn-python-3"},
            {"name": "FreeCodeCamp", "url": "https://www.freecodecamp.org"}
        ],
        "interests": ["Software Development", "Technology"]
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
            "spatial": 40,
            "science": 60,
            "history": 20,
            "geography": 30
        },
        "skills": {"required": 80},
        "resources": [
            {"name": "Kaggle Competitions", "url": "https://www.kaggle.com/competitions"},
            {"name": "DataCamp", "url": "https://www.datacamp.com"}
        ],
        "interests": ["Data Science", "Analytics"]
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
            "spatial": 90,
            "science": 20,
            "history": 40,
            "geography": 30
        },
        "skills": {"required": 65},
        "resources": [
            {"name": "Adobe Creative Cloud Tutorials", "url": "https://helpx.adobe.com/creative-cloud/tutorials-explore.html"},
            {"name": "Canva Design School", "url": "https://www.canva.com/learn/"}
        ],
        "interests": ["Graphic Design", "Art"]
    },
    "Financial Analyst": {
        "description": "Financial Analysts evaluate financial data to guide investment decisions and business strategies.",
        "personality": {
            "Openness": 65,
            "Conscientiousness": 85,
            "Extraversion": 50,
            "Agreeableness": 55,
            "Neuroticism": 35
        },
        "aptitude": {
            "numerical": 90,
            "logical": 80,
            "verbal": 70,
            "spatial": 40,
            "science": 30,
            "history": 50,
            "geography": 40
        },
        "skills": {"required": 75},
        "resources": [
            {"name": "CFA Institute", "url": "https://www.cfainstitute.org/"},
            {"name": "Investopedia", "url": "https://www.investopedia.com/"}
        ],
        "interests": ["Finance", "Analysis"]
    },
    "Bank Manager": {
        "description": "Bank Managers oversee bank operations, manage staff, and ensure customer satisfaction.",
        "personality": {
            "Openness": 60,
            "Conscientiousness": 90,
            "Extraversion": 70,
            "Agreeableness": 65,
            "Neuroticism": 30
        },
        "aptitude": {
            "numerical": 80,
            "logical": 75,
            "verbal": 85,
            "spatial": 30,
            "science": 20,
            "history": 40,
            "geography": 50
        },
        "skills": {"required": 70},
        "resources": [
            {"name": "American Bankers Association", "url": "https://www.aba.com/"},
            {"name": "Coursera Banking Courses", "url": "https://www.coursera.org/courses?query=banking"}
        ],
        "interests": ["Banking", "Management"]
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
            "spatial": 60,
            "science": 95,
            "history": 40,
            "geography": 40
        },
        "skills": {"required": 85},
        "resources": [
            {"name": "Google Scholar", "url": "https://scholar.google.com/"},
            {"name": "ResearchGate", "url": "https://www.researchgate.net/"}
        ],
        "interests": ["Scientific Research", "Innovation"]
    },
    "Accountant": {
        "description": "Accountants prepare and examine financial records to ensure accuracy and compliance.",
        "personality": {
            "Openness": 55,
            "Conscientiousness": 90,
            "Extraversion": 40,
            "Agreeableness": 60,
            "Neuroticism": 25
        },
        "aptitude": {
            "numerical": 95,
            "logical": 80,
            "verbal": 65,
            "spatial": 30,
            "science": 20,
            "history": 40,
            "geography": 30
        },
        "skills": {"required": 70},
        "resources": [
            {"name": "AICPA", "url": "https://www.aicpa.org/"},
            {"name": "QuickBooks Training", "url": "https://quickbooks.intuit.com/learn-support/training/"}
        ],
        "interests": ["Accounting", "Finance"]
    },
    "Mathematician": {
        "description": "Mathematicians develop mathematical theories and solve complex problems.",
        "personality": {
            "Openness": 90,
            "Conscientiousness": 75,
            "Extraversion": 30,
            "Agreeableness": 45,
            "Neuroticism": 20
        },
        "aptitude": {
            "numerical": 95,
            "logical": 95,
            "verbal": 50,
            "spatial": 70,
            "science": 60,
            "history": 30,
            "geography": 20
        },
        "skills": {"required": 85},
        "resources": [
            {"name": "Khan Academy Math", "url": "https://www.khanacademy.org/math"},
            {"name": "Wolfram MathWorld", "url": "https://mathworld.wolfram.com/"}
        ],
        "interests": ["Mathematics", "Problem Solving"]
    },
    "Marketing Manager": {
        "description": "Marketing Managers plan and execute campaigns to promote products or services.",
        "personality": {
            "Openness": 85,
            "Conscientiousness": 70,
            "Extraversion": 80,
            "Agreeableness": 65,
            "Neuroticism": 35
        },
        "aptitude": {
            "numerical": 60,
            "logical": 70,
            "verbal": 90,
            "spatial": 50,
            "science": 30,
            "history": 50,
            "geography": 60
        },
        "skills": {"required": 75},
        "resources": [
            {"name": "HubSpot Academy", "url": "https://academy.hubspot.com/"},
            {"name": "Google Digital Garage", "url": "https://learndigital.withgoogle.com/digitalgarage"}
        ],
        "interests": ["Marketing", "Advertising"]
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
            "spatial": 40,
            "science": 30,
            "history": 50,
            "geography": 50
        },
        "skills": {"required": 70},
        "resources": [
            {"name": "Coursera Business Management Courses", "url": "https://www.coursera.org/courses?query=business%20management"},
            {"name": "Harvard Business Review", "url": "https://hbr.org/"}
        ],
        "interests": ["Business Management", "Leadership"]
    },
    "Cybersecurity Analyst": {
        "description": "Cybersecurity Analysts protect systems and networks from cyber threats and vulnerabilities.",
        "personality": {
            "Openness": 75,
            "Conscientiousness": 80,
            "Extraversion": 35,
            "Agreeableness": 50,
            "Neuroticism": 30
        },
        "aptitude": {
            "numerical": 70,
            "logical": 90,
            "verbal": 60,
            "spatial": 45,
            "science": 50,
            "history": 20,
            "geography": 20
        },
        "skills": {"required": 80},
        "resources": [
            {"name": "Cybrary Cybersecurity Courses", "url": "https://www.cybrary.it/"},
            {"name": "TryHackMe", "url": "https://tryhackme.com/"}
        ],
        "interests": ["Cybersecurity", "Technology"]
    },
    "Environmental Engineer": {
        "description": "Environmental Engineers design solutions to address environmental issues like pollution and sustainability.",
        "personality": {
            "Openness": 85,
            "Conscientiousness": 75,
            "Extraversion": 50,
            "Agreeableness": 70,
            "Neuroticism": 35
        },
        "aptitude": {
            "numerical": 80,
            "logical": 75,
            "verbal": 65,
            "spatial": 70,
            "science": 85,
            "history": 30,
            "geography": 75
        },
        "skills": {"required": 75},
        "resources": [
            {"name": "edX Environmental Engineering Courses", "url": "https://www.edx.org/learn/environmental-engineering"},
            {"name": "EPA Resources", "url": "https://www.epa.gov/"}
        ],
        "interests": ["Environmental Science", "Sustainability"]
    },
    "Ethical Hacker": {
        "description": "Ethical Hackers identify and fix security vulnerabilities in systems by simulating cyberattacks.",
        "personality": {
            "Openness": 80,
            "Conscientiousness": 70,
            "Extraversion": 30,
            "Agreeableness": 45,
            "Neuroticism": 25
        },
        "aptitude": {
            "numerical": 65,
            "logical": 95,
            "verbal": 55,
            "spatial": 50,
            "science": 45,
            "history": 20,
            "geography": 20
        },
        "skills": {"required": 85},
        "resources": [
            {"name": "Hack The Box", "url": "https://www.hackthebox.com/"},
            {"name": "Offensive Security Certifications", "url": "https://www.offsec.com/"}
        ],
        "interests": ["Cybersecurity", "Problem Solving"]
    },
    "Urban Planner": {
        "description": "Urban Planners design and manage land use in urban areas to create sustainable communities.",
        "personality": {
            "Openness": 80,
            "Conscientiousness": 70,
            "Extraversion": 60,
            " Agreeableness": 75,
            "Neuroticism": 35
        },
        "aptitude": {
            "numerical": 60,
            "logical": 70,
            "verbal": 75,
            "spatial": 85,
            "science": 50,
            "history": 60,
            "geography": 90
        },
        "skills": {"required": 70},
        "resources": [
            {"name": "Planetizen Courses", "url": "https://courses.planetizen.com/"},
            {"name": "American Planning Association", "url": "https://www.planning.org/"}
        ],
        "interests": ["Urban Development", "Community Planning"]
    },
    "Voice Actor": {
        "description": "Voice Actors provide voices for animated characters, audiobooks, commercials, and other media.",
        "personality": {
            "Openness": 85,
            "Conscientiousness": 60,
            "Extraversion": 75,
            "Agreeableness": 65,
            "Neuroticism": 45
        },
        "aptitude": {
            "numerical": 20,
            "logical": 40,
            "verbal": 90,
            "spatial": 30,
            "science": 20,
            "history": 40,
            "geography": 30
        },
        "skills": {"required": 60},
        "resources": [
            {"name": "Voices.com Learning Center", "url": "https://www.voices.com/learn"},
            {"name": "Backstage Voice Acting Guides", "url": "https://www.backstage.com/magazine/voiceover/"}
        ],
        "interests": ["Performing Arts", "Creative Expression"]
    },
    "Astrophysicist": {
        "description": "Astrophysicists study the physics of the universe, including stars, planets, and galaxies.",
        "personality": {
            "Openness": 95,
            "Conscientiousness": 80,
            "Extraversion": 25,
            "Agreeableness": 40,
            "Neuroticism": 20
        },
        "aptitude": {
            "numerical": 95,
            "logical": 90,
            "verbal": 65,
            "spatial": 80,
            "science": 95,
            "history": 30,
            "geography": 40
        },
        "skills": {"required": 90},
        "resources": [
            {"name": "NASA Astrophysics Resources", "url": "https://science.nasa.gov/astrophysics/"},
            {"name": "Coursera Astrophysics Courses", "url": "https://www.coursera.org/courses?query=astrophysics"}
        ],
        "interests": ["Astronomy", "Physics"]
    },
    "Wildlife Biologist": {
        "description": "Wildlife Biologists study animals and their ecosystems to support conservation efforts.",
        "personality": {
            "Openness": 85,
            "Conscientiousness": 75,
            "Extraversion": 45,
            "Agreeableness": 70,
            "Neuroticism": 30
        },
        "aptitude": {
            "numerical": 65,
            "logical": 70,
            "verbal": 70,
            "spatial": 75,
            "science": 90,
            "history": 30,
            "geography": 80
        },
        "skills": {"required": 70},
        "resources": [
            {"name": "Wildlife Society Resources", "url": "https://wildlife.org/"},
            {"name": "Khan Academy Biology", "url": "https://www.khanacademy.org/science/biology"}
        ],
        "interests": ["Wildlife Conservation", "Ecology"]
    },
    "Doctor (General Physician)": {
        "description": "Doctors diagnose and treat illnesses, injuries, and medical conditions in patients.",
        "personality": {
            "Openness": 70,
            "Conscientiousness": 90,
            "Extraversion": 60,
            "Agreeableness": 80,
            "Neuroticism": 30
        },
        "aptitude": {
            "numerical": 70,
            "logical": 85,
            "verbal": 80,
            "spatial": 60,
            "science": 95,
            "history": 40,
            "geography": 30
        },
        "skills": {"required": 85},
        "resources": [
            {"name": "Khan Academy Medicine", "url": "https://www.khanacademy.org/science/health-and-medicine"},
            {"name": "Medscape", "url": "https://www.medscape.com/"}
        ],
        "interests": ["Medicine", "Patient Care"]
    },
    "Nurse": {
        "description": "Nurses provide patient care, administer treatments, and support doctors in medical settings.",
        "personality": {
            "Openness": 65,
            "Conscientiousness": 85,
            "Extraversion": 70,
            "Agreeableness": 90,
            "Neuroticism": 35
        },
        "aptitude": {
            "numerical": 60,
            "logical": 70,
            "verbal": 85,
            "spatial": 50,
            "science": 85,
            "history": 30,
            "geography": 30
        },
        "skills": {"required": 75},
        "resources": [
            {"name": "Nursing Times Learning", "url": "https://www.nursingtimes.net/"},
            {"name": "American Nurses Association", "url": "https://www.nursingworld.org/"}
        ],
        "interests": ["Nursing", "Healthcare"]
    },
    "Medical Researcher": {
        "description": "Medical Researchers study diseases and develop treatments or cures through experiments.",
        "personality": {
            "Openness": 90,
            "Conscientiousness": 85,
            "Extraversion": 40,
            "Agreeableness": 60,
            "Neuroticism": 25
        },
        "aptitude": {
            "numerical": 85,
            "logical": 90,
            "verbal": 70,
            "spatial": 55,
            "science": 95,
            "history": 40,
            "geography": 30
        },
        "skills": {"required": 90},
        "resources": [
            {"name": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/"},
            {"name": "ClinicalTrials.gov", "url": "https://clinicaltrials.gov/"}
        ],
        "interests": ["Medical Research", "Science"]
    },
    "Teacher (Secondary Education)": {
        "description": "Teachers educate students in specific subjects at the secondary level.",
        "personality": {
            "Openness": 75,
            "Conscientiousness": 80,
            "Extraversion": 70,
            "Agreeableness": 85,
            "Neuroticism": 35
        },
        "aptitude": {
            "numerical": 50,
            "logical": 65,
            "verbal": 90,
            "spatial": 40,
            "science": 60,
            "history": 70,
            "geography": 60
        },
        "skills": {"required": 70},
        "resources": [
            {"name": "Edutopia", "url": "https://www.edutopia.org/"},
            {"name": "Teach.com", "url": "https://teach.com/"}
        ],
        "interests": ["Education", "Teaching"]
    },
    "Lawyer": {
        "description": "Lawyers advise and represent clients in legal matters and court proceedings.",
        "personality": {
            "Openness": 70,
            "Conscientiousness": 85,
            "Extraversion": 75,
            "Agreeableness": 60,
            "Neuroticism": 40
        },
        "aptitude": {
            "numerical": 50,
            "logical": 90,
            "verbal": 95,
            "spatial": 30,
            "science": 30,
            "history": 80,
            "geography": 40
        },
        "skills": {"required": 80},
        "resources": [
            {"name": "ABA Legal Education", "url": "https://www.americanbar.org/groups/legal_education/"},
            {"name": "Coursera Law Courses", "url": "https://www.coursera.org/courses?query=law"}
        ],
        "interests": ["Law", "Justice"]
    },
    "Mechanical Engineer": {
        "description": "Mechanical Engineers design and develop mechanical systems and machinery.",
        "personality": {
            "Openness": 80,
            "Conscientiousness": 75,
            "Extraversion": 50,
            "Agreeableness": 55,
            "Neuroticism": 30
        },
        "aptitude": {
            "numerical": 90,
            "logical": 85,
            "verbal": 60,
            "spatial": 85,
            "science": 90,
            "history": 30,
            "geography": 40
        },
        "skills": {"required": 80},
        "resources": [
            {"name": "ASME Learning", "url": "https://www.asme.org/learning-development"},
            {"name": "MIT OpenCourseWare - Mechanical Engineering", "url": "https://ocw.mit.edu/courses/mechanical-engineering/"}
        ],
        "interests": ["Engineering", "Mechanics"]
    }
}

SKILL_GAP_QUESTIONS = {
    "Software Development": [
        {
            "id": 1,
            "text": "What will be the output of the following Python code? \n\n```python\nx = [1, 2, 3]\ny = x\ny[0] = 5\nprint(x)\n```",
            "options": ["[1, 2, 3]", "[5, 2, 3]", "[5, 5, 5]", "Error"],
            "correct": 1,  # Tests understanding of list mutability
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
            "correct": 0,  # Tests OOP fundamentals
            "time_limit": 45
        },
        {
            "id": 3,
            "text": "Which Git command is used to save changes to the local repository?",
            "options": ["git add", "git commit", "git push", "git pull"],
            "correct": 1,  # Tests version control knowledge
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "What does the HTTP status code 404 indicate in a RESTful API?",
            "options": ["Success", "Unauthorized", "Not Found", "Server Error"],
            "correct": 2,  # Tests API understanding
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is the time complexity of a binary search algorithm?",
            "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
            "correct": 1,  # Tests algorithm efficiency
            "time_limit": 45
        },
        {
            "id": 6,
            "text": "Which SQL clause retrieves unique records from a database?",
            "options": ["GROUP BY", "DISTINCT", "ORDER BY", "LIMIT"],
            "correct": 1,  # Tests database querying
            "time_limit": 30
        },
        {
            "id": 7,
            "text": "What is the purpose of a Docker container?",
            "options": [
                "To compile code",
                "To package apps with dependencies",
                "To manage databases",
                "To design UI"
            ],
            "correct": 1,  # Tests containerization knowledge
            "time_limit": 45
        },
        {
            "id": 8,
            "text": "Which testing type ensures new code doesn’t break existing functionality?",
            "options": ["Unit", "Integration", "Regression", "Stress"],
            "correct": 2,  # Tests software testing skills
            "time_limit": 30
        },
        {
            "id": 9,
            "text": "What does CI/CD stand for in DevOps?",
            "options": [
                "Code Integration/Code Delivery",
                "Continuous Integration/Continuous Deployment",
                "Compile Install/Compile Deploy",
                "Continuous Improvement/Code Debugging"
            ],
            "correct": 1,  # Tests DevOps basics
            "time_limit": 45
        },
        {
            "id": 10,
            "text": "Which Python library is used for unit testing?",
            "options": ["NumPy", "Pandas", "unittest", "Requests"],
            "correct": 2,  # Tests debugging skills
            "time_limit": 30
        }
    ],
    "Data Science": [
        {
            "id": 1,
            "text": "What Python library is commonly used for data manipulation and analysis?",
            "options": ["NumPy", "Pandas", "Matplotlib", "Seaborn"],
            "correct": 1,  # Tests data handling
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
            "correct": 1,  # Tests statistical knowledge
            "time_limit": 45
        },
        {
            "id": 3,
            "text": "Which algorithm is a supervised learning method for classification?",
            "options": ["K-Means", "Linear Regression", "Logistic Regression", "PCA"],
            "correct": 2,  # Tests machine learning basics
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "Which tool is best suited for creating a bar chart in Python?",
            "options": ["Pandas", "NumPy", "Matplotlib", "Scikit-learn"],
            "correct": 2,  # Tests visualization skills
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What technique reduces dataset dimensionality?",
            "options": ["Feature Selection", "Cross-Validation", "Regularization", "Gradient Descent"],
            "correct": 0,  # Tests data preprocessing
            "time_limit": 45
        },
        {
            "id": 6,
            "text": "What does overfitting mean in machine learning?",
            "options": [
                "Model performs well on all data",
                "Model learns noise in training data",
                "Model is too simple",
                "Model ignores training data"
            ],
            "correct": 1,  # Tests model evaluation
            "time_limit": 45
        },
        {
            "id": 7,
            "text": "Which SQL function calculates the average of a column?",
            "options": ["SUM()", "AVG()", "COUNT()", "MAX()"],
            "correct": 1,  # Tests database skills
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What is the purpose of a confusion matrix?",
            "options": [
                "To visualize data",
                "To evaluate classification performance",
                "To normalize data",
                "To select features"
            ],
            "correct": 1,  # Tests model assessment
            "time_limit": 45
        },
        {
            "id": 9,
            "text": "Which Python library is used for natural language processing?",
            "options": ["NLTK", "Pandas", "Seaborn", "TensorFlow"],
            "correct": 0,  # Tests NLP knowledge
            "time_limit": 30
        },
        {
            "id": 10,
            "text": "What is a common method to handle missing data?",
            "options": [
                "Drop all rows",
                "Impute with mean/median",
                "Ignore missing values",
                "Replace with outliers"
            ],
            "correct": 1,  # Tests data cleaning
            "time_limit": 45
        }
    ],
    "Graphic Design": [
        {
            "id": 1,
            "text": "What Photoshop tool is used to remove part of an image?",
            "options": ["Brush Tool", "Eraser Tool", "Clone Stamp Tool", "Magic Wand Tool"],
            "correct": 1,  # Tests Photoshop basics
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "In Adobe Illustrator, which tool creates shapes with anchor points?",
            "options": ["Pen Tool", "Brush Tool", "Gradient Tool", "Eyedropper Tool"],
            "correct": 0,  # Tests Illustrator skills
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
            "correct": 1,  # Tests color theory
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "What is kerning in typography?",
            "options": [
                "Adjusting space between letters",
                "Changing font size",
                "Aligning text to the left",
                "Adding shadows"
            ],
            "correct": 0,  # Tests typography skills
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "Which file format supports transparency?",
            "options": ["JPEG", "PNG", "GIF", "BMP"],
            "correct": 1,  # Tests file format knowledge
            "time_limit": 30
        },
        {
            "id": 6,
            "text": "What is the purpose of a mood board in design?",
            "options": [
                "To finalize a logo",
                "To gather visual inspiration",
                "To code a website",
                "To print designs"
            ],
            "correct": 1,  # Tests design process
            "time_limit": 45
        },
        {
            "id": 7,
            "text": "What does UI design primarily focus on?",
            "options": [
                "Backend coding",
                "User interface aesthetics and functionality",
                "Hardware optimization",
                "Database management"
            ],
            "correct": 1,  # Tests UI/UX knowledge
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "Which Adobe tool is best for layout design?",
            "options": ["Photoshop", "Illustrator", "InDesign", "After Effects"],
            "correct": 2,  # Tests software proficiency
            "time_limit": 30
        },
        {
            "id": 9,
            "text": "What is a wireframe in web design?",
            "options": [
                "A final website design",
                "A basic layout blueprint",
                "A color palette",
                "A coding framework"
            ],
            "correct": 1,  # Tests web design skills
            "time_limit": 45
        },
        {
            "id": 10,
            "text": "What is the golden ratio in design?",
            "options": [
                "1:1", "1:1.618", "1:2", "2:3"],
                "correct": 1,  # Tests design principles
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
            "correct": 0,  # Tests strategic planning
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
            "correct": 1,  # Tests financial skills
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
            "correct": 1,  # Tests leadership knowledge
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "What does a Gantt chart visualize?",
            "options": [
                "Employee performance",
                "Project timelines and tasks",
                "Financial profits",
                "Market trends"
            ],
            "correct": 1,  # Tests project management
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is a key element of effective team communication?",
            "options": [
                "Withholding information",
                "Active listening",
                "Avoiding feedback",
                "Using jargon"
            ],
            "correct": 1,  # Tests communication skills
            "time_limit": 30
        },
        {
            "id": 6,
            "text": "What does CRM stand for in business?",
            "options": [
                "Customer Relationship Management",
                "Corporate Revenue Model",
                "Client Resource Management",
                "Cost Reduction Method"
            ],
            "correct": 0,  # Tests customer management
            "time_limit": 30
        },
        {
            "id": 7,
            "text": "What is the purpose of a balanced scorecard?",
            "options": [
                "To track financial and non-financial performance",
                "To design marketing campaigns",
                "To hire employees",
                "To manage inventory"
            ],
            "correct": 0,  # Tests performance metrics
            "time_limit": 45
        },
        {
            "id": 8,
            "text": "What is a common conflict resolution strategy?",
            "options": [
                "Ignoring the issue",
                "Collaborative problem-solving",
                "Dictating a solution",
                "Avoiding discussion"
            ],
            "correct": 1,  # Tests conflict management
            "time_limit": 45
        },
        {
            "id": 9,
            "text": "What does KPI stand for?",
            "options": [
                "Key Project Initiative",
                "Key Performance Indicator",
                "Knowledge Process Integration",
                "Key Profit Index"
            ],
            "correct": 1,  # Tests metrics knowledge
            "time_limit": 30
        },
        {
            "id": 10,
            "text": "What is the purpose of stakeholder analysis?",
            "options": [
                "To identify and prioritize project influencers",
                "To calculate profits",
                "To design products",
                "To reduce costs"
            ],
            "correct": 0,  # Tests stakeholder management
            "time_limit": 45
        }
    ],
    "Scientific": [
        {
            "id": 1,
            "text": "What is the first step in the scientific method?",
            "options": [
                "Conduct an experiment",
                "Form a hypothesis",
                "Ask a question",
                "Analyze data"
            ],
            "correct": 2,  # Tests research basics
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What does a p-value indicate in research?",
            "options": [
                "Sample size",
                "Statistical significance",
                "Effect size",
                "Correlation strength"
            ],
            "correct": 1,  # Tests statistical skills
            "time_limit": 45
        },
        {
            "id": 3,
            "text": "What is a control group in an experiment?",
            "options": [
                "The group receiving the treatment",
                "The group not receiving the treatment",
                "The group with no data",
                "The group with random variables"
            ],
            "correct": 1,  # Tests experimental design
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "Which software is commonly used for statistical analysis?",
            "options": ["Excel", "SPSS", "Photoshop", "Illustrator"],
            "correct": 1,  # Tests research tools
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is peer review in scientific publishing?",
            "options": [
                "Editing by the author",
                "Evaluation by experts in the field",
                "Public voting",
                "Automated grammar checking"
            ],
            "correct": 1,  # Tests publication process
            "time_limit": 45
        },
        {
            "id": 6,
            "text": "What is a confounding variable?",
            "options": [
                "A variable that influences both dependent and independent variables",
                "A variable that is controlled",
                "A variable that is ignored",
                "A variable that is constant"
            ],
            "correct": 0,  # Tests research methodology
            "time_limit": 45
        },
        {
            "id": 7,
            "text": "What does ANOVA stand for in statistics?",
            "options": [
                "Analysis of Variance",
                "Average of Numbers",
                "Assessment of Values",
                "Analysis of Variables"
            ],
            "correct": 0,  # Tests advanced statistics
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What is the purpose of a literature review?",
            "options": [
                "To summarize existing research",
                "To conduct experiments",
                "To publish results",
                "To design surveys"
            ],
            "correct": 0,  # Tests research preparation
            "time_limit": 45
        },
        {
            "id": 9,
            "text": "Which citation style is common in scientific research?",
            "options": ["MLA", "APA", "Chicago", "Harvard"],
            "correct": 1,  # Tests academic writing
            "time_limit": 30
        },
        {
            "id": 10,
            "text": "What is a hypothesis in research?",
            "options": [
                "A proven fact",
                "A testable prediction",
                "A final conclusion",
                "A random guess"
            ],
            "correct": 1,  # Tests hypothesis formation
            "time_limit": 30
        }
    ],
    "Cybersecurity": [
        {
            "id": 1,
            "text": "What does a firewall primarily do?",
            "options": [
                "Encrypts data",
                "Filters network traffic",
                "Backs up files",
                "Runs antivirus scans"
            ],
            "correct": 1,  # Tests network security
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What is phishing in cybersecurity?",
            "options": [
                "A hardware attack",
                "A social engineering attack via fake emails",
                "A virus infection",
                "A firewall breach"
            ],
            "correct": 1,  # Tests threat knowledge
            "time_limit": 45
        },
        {
            "id": 3,
            "text": "Which protocol ensures secure web browsing?",
            "options": ["HTTP", "FTP", "HTTPS", "SMTP"],
            "correct": 2,  # Tests web security
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "What is the purpose of two-factor authentication?",
            "options": [
                "To speed up login",
                "To add an extra layer of security",
                "To simplify passwords",
                "To share credentials"
            ],
            "correct": 1,  # Tests authentication
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What tool is used for network packet analysis?",
            "options": ["Wireshark", "Photoshop", "Excel", "Git"],
            "correct": 0,  # Tests cybersecurity tools
            "time_limit": 30
        },
        {
            "id": 6,
            "text": "What is a common encryption standard for data?",
            "options": ["AES", "JPEG", "MP4", "HTML"],
            "correct": 0,  # Tests encryption knowledge
            "time_limit": 30
        },
        {
            "id": 7,
            "text": "What does a VPN do?",
            "options": [
                "Speeds up internet",
                "Encrypts internet traffic",
                "Blocks websites",
                "Installs software"
            ],
            "correct": 1,  # Tests privacy tools
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What is a zero-day vulnerability?",
            "options": [
                "A known software bug",
                "An unknown exploit before patching",
                "A hardware failure",
                "A user error"
            ],
            "correct": 1,  # Tests advanced threats
            "time_limit": 45
        },
        {
            "id": 9,
            "text": "Which Linux command lists open ports?",
            "options": ["ls", "netstat", "pwd", "chmod"],
            "correct": 1,  # Tests system administration
            "time_limit": 30
        },
        {
            "id": 10,
            "text": "What is the purpose of penetration testing?",
            "options": [
                "To design networks",
                "To identify security weaknesses",
                "To install software",
                "To monitor traffic"
            ],
            "correct": 1,  # Tests security assessment
            "time_limit": 45
        }
    ],
    "Environmental Engineering": [
        {
            "id": 1,
            "text": "What is the primary goal of wastewater treatment?",
            "options": [
                "To produce drinking water",
                "To remove contaminants",
                "To generate energy",
                "To irrigate crops"
            ],
            "correct": 1,  # Tests water management
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What gas is primarily responsible for global warming?",
            "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"],
            "correct": 2,  # Tests climate knowledge
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "What does BOD stand for in water quality?",
            "options": [
                "Biological Oxygen Demand",
                "Basic Organic Data",
                "Biodegradable Organic Deposit",
                "Bacterial Oxygen Density"
            ],
            "correct": 0,  # Tests water quality metrics
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "Which renewable energy source uses turbines?",
            "options": ["Solar", "Wind", "Geothermal", "Biomass"],
            "correct": 1,  # Tests energy systems
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is the purpose of an Environmental Impact Assessment?",
            "options": [
                "To promote projects",
                "To evaluate environmental effects",
                "To reduce costs",
                "To hire engineers"
            ],
            "correct": 1,  # Tests regulatory knowledge
            "time_limit": 45
        },
        {
            "id": 6,
            "text": "What is bioremediation?",
            "options": [
                "Using organisms to clean pollutants",
                "Building dams",
                "Recycling plastics",
                "Mining resources"
            ],
            "correct": 0,  # Tests pollution control
            "time_limit": 45
        },
        {
            "id": 7,
            "text": "What software is used for environmental modeling?",
            "options": ["AutoCAD", "MATLAB", "Photoshop", "Word"],
            "correct": 1,  # Tests technical tools
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What is a common method to reduce air pollution?",
            "options": [
                "Increase emissions",
                "Use scrubbers in factories",
                "Burn more coal",
                "Ignore regulations"
            ],
            "correct": 1,  # Tests air quality solutions
            "time_limit": 30
        },
        {
            "id": 9,
            "text": "What does LEED certification relate to?",
            "options": [
                "Sustainable building design",
                "Software development",
                "Food safety",
                "Medical research"
            ],
            "correct": 0,  # Tests green engineering
            "time_limit": 45
        },
        {
            "id": 10,
            "text": "What is the purpose of a stormwater management plan?",
            "options": [
                "To increase flooding",
                "To control runoff and pollution",
                "To build roads",
                "To plant crops"
            ],
            "correct": 1,  # Tests water management
            "time_limit": 45
        }
    ],
    "Ethical Hacking": [
        {
            "id": 1,
            "text": "What is the primary goal of ethical hacking?",
            "options": [
                "To exploit systems",
                "To improve system security",
                "To steal data",
                "To disrupt services"
            ],
            "correct": 1,  # Tests ethical hacking purpose
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What tool is used for vulnerability scanning?",
            "options": ["Nmap", "Photoshop", "Excel", "Git"],
            "correct": 0,  # Tests hacking tools
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "What is SQL injection?",
            "options": [
                "A database backup method",
                "A code injection attack",
                "A hardware exploit",
                "A network protocol"
            ],
            "correct": 1,  # Tests web vulnerabilities
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "What does a brute force attack target?",
            "options": [
                "Passwords",
                "Hardware",
                "Firewalls",
                "Databases"
            ],
            "correct": 0,  # Tests attack methods
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "Which Linux command checks running processes?",
            "options": ["ls", "top", "pwd", "chmod"],
            "correct": 1,  # Tests system monitoring
            "time_limit": 30
        },
        {
            "id": 6,
            "text": "What is the purpose of a packet sniffer?",
            "options": [
                "To encrypt data",
                "To capture network traffic",
                "To install software",
                "To design websites"
            ],
            "correct": 1,  # Tests network analysis
            "time_limit": 45
        },
        {
            "id": 7,
            "text": "What is social engineering in hacking?",
            "options": [
                "Manipulating people to gain access",
                "Writing code",
                "Breaking hardware",
                "Encrypting data"
            ],
            "correct": 0,  # Tests non-technical skills
            "time_limit": 45
        },
        {
            "id": 8,
            "text": "What is a common wireless security protocol?",
            "options": ["WEP", "WPA3", "FTP", "HTTP"],
            "correct": 1,  # Tests wireless security
            "time_limit": 30
        },
        {
            "id": 9,
            "text": "What does OWASP stand for?",
            "options": [
                "Open Web Application Security Project",
                "Online Wireless Attack Software Project",
                "Open World Application Standards Protocol",
                "Operational Web Analysis Security Program"
            ],
            "correct": 0,  # Tests security standards
            "time_limit": 45
        },
        {
            "id": 10,
            "text": "What is a man-in-the-middle attack?",
            "options": [
                "Intercepting communication between two parties",
                "Stealing hardware",
                "Crashing servers",
                "Encrypting files"
            ],
            "correct": 0,  # Tests advanced attacks
            "time_limit": 45
        }
    ],
    "Urban Planning": [
        {
            "id": 1,
            "text": "What is the primary goal of urban planning?",
            "options": [
                "To maximize profits",
                "To create sustainable communities",
                "To reduce population",
                "To build skyscrapers"
            ],
            "correct": 1,  # Tests planning objectives
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What does GIS stand for in urban planning?",
            "options": [
                "Geographic Information System",
                "Global Infrastructure Standards",
                "General Impact Study",
                "Geological Integration Software"
            ],
            "correct": 0,  # Tests planning tools
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "What is mixed-use development?",
            "options": [
                "Building only residential areas",
                "Combining residential, commercial, and recreational spaces",
                "Focusing on industrial zones",
                "Creating parks only"
            ],
            "correct": 1,  # Tests land use knowledge
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "What is a zoning ordinance?",
            "options": [
                "A law regulating land use",
                "A tax policy",
                "A building permit",
                "A transportation plan"
            ],
            "correct": 0,  # Tests regulatory knowledge
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is the purpose of a master plan?",
            "options": [
                "To guide long-term community development",
                "To design individual buildings",
                "To manage daily traffic",
                "To fund projects"
            ],
            "correct": 0,  # Tests strategic planning
            "time_limit": 45
        },
        {
            "id": 6,
            "text": "What is walkability in urban design?",
            "options": [
                "Ease of pedestrian movement",
                "Building tall structures",
                "Increasing car usage",
                "Reducing green spaces"
            ],
            "correct": 0,  # Tests design principles
            "time_limit": 30
        },
        {
            "id": 7,
            "text": "What software is used for urban modeling?",
            "options": ["AutoCAD", "SketchUp", "Photoshop", "Excel"],
            "correct": 1,  # Tests technical skills
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What is gentrification?",
            "options": [
                "Urban decay",
                "Displacement due to wealthier residents",
                "Building low-income housing",
                "Preserving historic sites"
            ],
            "correct": 1,  # Tests social impact knowledge
            "time_limit": 45
        },
        {
            "id": 9,
            "text": "What is a common goal of transit-oriented development?",
            "options": [
                "Increase car usage",
                "Promote public transit use",
                "Build isolated communities",
                "Reduce housing"
            ],
            "correct": 1,  # Tests transportation planning
            "time_limit": 45
        },
        {
            "id": 10,
            "text": "What does LEED-ND certify?",
            "options": [
                "Neighborhood development sustainability",
                "Individual buildings",
                "Highways",
                "Factories"
            ],
            "correct": 0,  # Tests green planning
            "time_limit": 45
        }
    ],
    "Voice Acting": [
        {
            "id": 1,
            "text": "What is the primary role of a voice actor?",
            "options": [
                "To design sound effects",
                "To provide vocal performances",
                "To write scripts",
                "To edit audio"
            ],
            "correct": 1,  # Tests role understanding
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What is diction in voice acting?",
            "options": [
                "Clear pronunciation",
                "Singing ability",
                "Script writing",
                "Audio mixing"
            ],
            "correct": 0,  # Tests vocal skills
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "What is a common warm-up for voice actors?",
            "options": [
                "Running",
                "Vocal exercises",
                "Typing practice",
                "Drawing sketches"
            ],
            "correct": 1,  # Tests preparation skills
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "What does ADR stand for in voice acting?",
            "options": [
                "Automated Dialogue Replacement",
                "Audio Design Recording",
                "Advanced Diction Review",
                "Adaptive Dialogue Reading"
            ],
            "correct": 0,  # Tests industry terms
            "time_limit": 45
        },
        {
            "id": 5,
            "text": "What software is used for audio recording?",
            "options": ["Photoshop", "Audacity", "Illustrator", "Excel"],
            "correct": 1,  # Tests technical skills
            "time_limit": 30
        },
        {
            "id": 6,
            "text": "What is pacing in voice acting?",
            "options": [
                "Running speed",
                "Timing and rhythm of delivery",
                "Volume control",
                "Script editing"
            ],
            "correct": 1,  # Tests performance skills
            "time_limit": 30
        },
        {
            "id": 7,
            "text": "What is a demo reel?",
            "options": [
                "A final project",
                "A showcase of voice samples",
                "A script draft",
                "A sound effect library"
            ],
            "correct": 1,  # Tests portfolio knowledge
            "time_limit": 45
        },
        {
            "id": 8,
            "text": "What is the purpose of a pop filter?",
            "options": [
                "To reduce plosive sounds",
                "To increase volume",
                "To edit audio",
                "To write scripts"
            ],
            "correct": 0,  # Tests recording setup
            "time_limit": 30
        },
        {
            "id": 9,
            "text": "What skill helps voice actors convey emotion?",
            "options": [
                "Typing",
                "Acting techniques",
                "Coding",
                "Graphic design"
            ],
            "correct": 1,  # Tests emotional delivery
            "time_limit": 30
        },
        {
            "id": 10,
            "text": "What is a common microphone type for voice acting?",
            "options": [
                "Dynamic",
                "Condenser",
                "Ribbon",
                "Lavalier"
            ],
            "correct": 1,  # Tests equipment knowledge
            "time_limit": 30
        }
    ],
    "Astronomy": [
        {
            "id": 1,
            "text": "What is a light-year?",
            "options": [
                "A unit of time",
                "A unit of distance",
                "A type of star",
                "A telescope lens"
            ],
            "correct": 1,  # Tests basic astronomy
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What causes a supernova?",
            "options": [
                "A planet’s orbit",
                "A star’s explosion",
                "A comet’s tail",
                "A moon’s eclipse"
            ],
            "correct": 1,  # Tests stellar phenomena
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "What is the Doppler effect in astronomy?",
            "options": [
                "Change in light wavelength due to motion",
                "A star’s brightness",
                "A planet’s rotation",
                "A telescope’s focus"
            ],
            "correct": 0,  # Tests observational skills
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "Which software is used for astrophysical simulations?",
            "options": ["MATLAB", "Photoshop", "Excel", "Word"],
            "correct": 0,  # Tests technical tools
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is a black hole?",
            "options": [
                "A bright star",
                "A region with extreme gravity",
                "A type of galaxy",
                "A meteor shower"
            ],
            "correct": 1,  # Tests advanced concepts
            "time_limit": 45
        },
        {
            "id": 6,
            "text": "What is redshift in cosmology?",
            "options": [
                "Light shifting to shorter wavelengths",
                "Light shifting to longer wavelengths",
                "A star’s color change",
                "A planet’s rotation"
            ],
            "correct": 1,  # Tests cosmology
            "time_limit": 45
        },
        {
            "id": 7,
            "text": "What is the primary source of a star’s energy?",
            "options": [
                "Nuclear fusion",
                "Chemical reactions",
                "Gravitational pull",
                "Magnetic fields"
            ],
            "correct": 0,  # Tests stellar physics
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What telescope type uses mirrors?",
            "options": [
                "Refracting",
                "Reflecting",
                "Radio",
                "Infrared"
            ],
            "correct": 1,  # Tests observational tools
            "time_limit": 30
        },
        {
            "id": 9,
            "text": "What is Kepler’s First Law?",
            "options": [
                "Planets orbit in ellipses",
                "Planets orbit in circles",
                "Planets have equal speeds",
                "Planets rotate daily"
            ],
            "correct": 0,  # Tests orbital mechanics
            "time_limit": 45
        },
        {
            "id": 10,
            "text": "What is a common data analysis language in astronomy?",
            "options": ["Python", "HTML", "CSS", "SQL"],
            "correct": 0,  # Tests programming skills
            "time_limit": 30
        }
    ],
    "Wildlife Conservation": [
        {
            "id": 1,
            "text": "What is the primary goal of wildlife conservation?",
            "options": [
                "To hunt animals",
                "To protect species and habitats",
                "To urbanize forests",
                "To farm animals"
            ],
            "correct": 1,  # Tests conservation goals
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What is an endangered species?",
            "options": [
                "A species with a large population",
                "A species at risk of extinction",
                "A species in zoos",
                "A species with no predators"
            ],
            "correct": 1,  # Tests species knowledge
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "What is a keystone species?",
            "options": [
                "A species with no impact",
                "A species critical to ecosystem balance",
                "A species that migrates",
                "A species that is extinct"
            ],
            "correct": 1,  # Tests ecology
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "What tool is used to track animal migration?",
            "options": ["GPS tags", "Microscopes", "Cameras", "Drones"],
            "correct": 0,  # Tests field tools
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What is habitat fragmentation?",
            "options": [
                "Building new habitats",
                "Dividing habitats into smaller parts",
                "Planting trees",
                "Cleaning rivers"
            ],
            "correct": 1,  # Tests environmental impact
            "time_limit": 45
        },
        {
            "id": 6,
            "text": "What is the purpose of a biodiversity hotspot?",
            "options": [
                "To promote tourism",
                "To identify high-diversity areas for protection",
                "To urbanize regions",
                "To mine resources"
            ],
            "correct": 1,  # Tests conservation strategy
            "time_limit": 45
        },
        {
            "id": 7,
            "text": "What is a common method to study animal behavior?",
            "options": [
                "Ethology",
                "Geology",
                "Astrology",
                "Anthropology"
            ],
            "correct": 0,  # Tests research methods
            "time_limit": 30
        },
        {
            "id": 8,
            "text": "What does IUCN stand for?",
            "options": [
                "International Union for Conservation of Nature",
                "Institute for Urban Conservation Networks",
                "International University of Conservation",
                "Integrated Urban Nature Council"
            ],
            "correct": 0,  # Tests organizations
            "time_limit": 45
        },
        {
            "id": 9,
            "text": "What is ex-situ conservation?",
            "options": [
                "Protecting species in their natural habitat",
                "Protecting species outside their natural habitat",
                "Hunting species",
                "Ignoring species"
            ],
            "correct": 1,  # Tests conservation types
            "time_limit": 45
        },
        {
            "id": 10,
            "text": "What software is used for ecological data analysis?",
            "options": ["R", "Photoshop", "Word", "PowerPoint"],
            "correct": 0,  # Tests data skills
            "time_limit": 30
        }
    ],
        "Medicine": [
        {
            "id": 1,
            "text": "What is the primary function of red blood cells?",
            "options": ["Fight infection", "Carry oxygen", "Clot blood", "Produce energy"],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What does CPR stand for?",
            "options": [
                "Cardiac Pulse Recovery",
                "Cardiopulmonary Resuscitation",
                "Cerebral Pressure Relief",
                "Critical Patient Response"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "Which organ filters blood and produces urine?",
            "options": ["Liver", "Kidneys", "Heart", "Lungs"],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "What is a common symptom of hypoglycemia?",
            "options": ["High fever", "Shakiness", "Increased thirst", "Chest pain"],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 5,
            "text": "What does an ECG measure?",
            "options": [
                "Blood pressure",
                "Heart electrical activity",
                "Oxygen levels",
                "Brain waves"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 6,
            "text": "Which vitamin is essential for blood clotting?",
            "options": ["Vitamin A", "Vitamin C", "Vitamin K", "Vitamin D"],
            "correct": 2,
            "time_limit": 30
        },
        {
            "id": 7,
            "text": "What is the normal range for adult blood pressure?",
            "options": ["120/80 mmHg", "140/90 mmHg", "100/60 mmHg", "160/100 mmHg"],
            "correct": 0,
            "time_limit": 45
        },
        {
            "id": 8,
            "text": "What is the purpose of an antibiotic?",
            "options": [
                "To reduce pain",
                "To treat bacterial infections",
                "To boost immunity",
                "To lower blood sugar"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 9,
            "text": "What is a differential diagnosis?",
            "options": [
                "A single confirmed diagnosis",
                "A list of possible conditions",
                "A surgical procedure",
                "A lab test result"
            ],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 10,
            "text": "Which system regulates body temperature?",
            "options": ["Nervous", "Endocrine", "Integumentary", "Respiratory"],
            "correct": 2,
            "time_limit": 45
        }
        ],
        "Education": [
        {
            "id": 1,
            "text": "What is the primary goal of formative assessment?",
            "options": [
                "To assign final grades",
                "To monitor student progress",
                "To rank students",
                "To test memory"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What does scaffolding mean in teaching?",
            "options": [
                "Building physical structures",
                "Providing temporary support for learning",
                "Testing students",
                "Assigning homework"
            ],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 3,
            "text": "Which learning theory emphasizes rewards and punishments?",
            "options": ["Constructivism", "Behaviorism", "Cognitivism", "Humanism"],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 4,
            "text": "What is a lesson plan?",
            "options": [
                "A student essay",
                "A structured teaching guide",
                "A grading rubric",
                "A parent meeting"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 5,
            "text": "What tool is used for interactive classroom quizzes?",
            "options": ["Kahoot", "Photoshop", "Excel", "Word"],
            "correct": 0,
            "time_limit": 30
        }
    ],
    "Law": [
        {
            "id": 1,
            "text": "What is the primary source of law in common law systems?",
            "options": ["Statutes", "Precedents", "Regulations", "Constitutions"],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 2,
            "text": "What does 'habeas corpus' mean?",
            "options": [
                "Right to appeal",
                "Produce the body",
                "Guilty plea",
                "Beyond reasonable doubt"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "What is a tort?",
            "options": [
                "A criminal act",
                "A civil wrong",
                "A contract breach",
                "A legal opinion"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "What is the purpose of cross-examination?",
            "options": [
                "To present evidence",
                "To question a witness’s credibility",
                "To deliver a verdict",
                "To draft a contract"
            ],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 5,
            "text": "What does ‘pro bono’ mean in legal practice?",
            "options": [
                "For profit",
                "Free of charge",
                "Court-ordered",
                "Confidential"
            ],
            "correct": 1,
            "time_limit": 30
        }
    ],
    "Mechanical Engineering": [
        {
            "id": 1,
            "text": "What is the primary function of a gear?",
            "options": [
                "To generate heat",
                "To transmit motion or torque",
                "To store energy",
                "To reduce noise"
            ],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 2,
            "text": "What does CAD stand for?",
            "options": [
                "Computer-Aided Design",
                "Calculated Axial Dynamics",
                "Controlled Assembly Device",
                "Computerized Analysis Data"
            ],
            "correct": 0,
            "time_limit": 30
        },
        {
            "id": 3,
            "text": "What is the unit of stress?",
            "options": ["Newton", "Pascal", "Joule", "Watt"],
            "correct": 1,
            "time_limit": 30
        },
        {
            "id": 4,
            "text": "What law relates force, mass, and acceleration?",
            "options": [
                "Newton’s First Law",
                "Newton’s Second Law",
                "Hooke’s Law",
                "Ohm’s Law"
            ],
            "correct": 1,
            "time_limit": 45
        },
        {
            "id": 5,
            "text": "What is the purpose of a bearing?",
            "options": [
                "To increase friction",
                "To reduce friction between moving parts",
                "To store energy",
                "To cool systems"
            ],
            "correct": 1,
            "time_limit": 30
        }
    ]
}

LEARNING_RESOURCES = {
    "Software Developer": {
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
    "Data Scientist": {
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
    "Graphic Designer": {
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
    "Financial Analyst": {
        "basic": [
            {"name": "CFA Institute", "url": "https://www.cfainstitute.org/"},
            {"name": "Investopedia", "url": "https://www.investopedia.com/"}
        ],
        "intermediate": [
            {"name": "Financial Modeling on Coursera", "url": "https://www.coursera.org/learn/financial-modeling"},
            {"name": "Morningstar Learning Center", "url": "https://www.morningstar.com/learn"}
        ],
        "advanced": [
            {"name": "Advanced Financial Analysis on edX", "url": "https://www.edx.org/course/advanced-financial-analysis"},
            {"name": "Bloomberg Terminal Training", "url": "https://www.bloomberg.com/professional/training/"}
        ]
    },
    "Bank Manager": {
        "basic": [
            {"name": "American Bankers Association", "url": "https://www.aba.com/"},
            {"name": "Coursera Banking Courses", "url": "https://www.coursera.org/courses?query=banking"}
        ],
        "intermediate": [
            {"name": "Bank Management on LinkedIn Learning", "url": "https://www.linkedin.com/learning/topics/bank-management"},
            {"name": "Bank Administration Institute", "url": "https://www.bai.org/"}
        ],
        "advanced": [
            {"name": "Advanced Banking Strategy on edX", "url": "https://www.edx.org/course/advanced-banking-strategy"},
            {"name": "Federal Reserve Education", "url": "https://www.federalreserveeducation.org/"}
        ]
    },
    "Research Scientist": {
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
    },
    "Accountant": {
        "basic": [
            {"name": "AICPA", "url": "https://www.aicpa.org/"},
            {"name": "QuickBooks Training", "url": "https://quickbooks.intuit.com/learn-support/training/"}
        ],
        "intermediate": [
            {"name": "Intermediate Accounting on Coursera", "url": "https://www.coursera.org/learn/intermediate-accounting"},
            {"name": "CPA Exam Prep", "url": "https://www.cpaexam.com/"}
        ],
        "advanced": [
            {"name": "Advanced Accounting on edX", "url": "https://www.edx.org/course/advanced-accounting"},
            {"name": "IASB Resources", "url": "https://www.ifrs.org/"}
        ]
    },
    "Mathematician": {
        "basic": [
            {"name": "Khan Academy Math", "url": "https://www.khanacademy.org/math"},
            {"name": "Wolfram MathWorld", "url": "https://mathworld.wolfram.com/"}
        ],
        "intermediate": [
            {"name": "Intermediate Algebra on Coursera", "url": "https://www.coursera.org/learn/intermediate-algebra"},
            {"name": "Project Euler", "url": "https://projecteuler.net/"}
        ],
        "advanced": [
            {"name": "Advanced Mathematics on edX", "url": "https://www.edx.org/course/advanced-mathematics"},
            {"name": "MathOverflow", "url": "https://mathoverflow.net/"}
        ]
    },
    "Marketing Manager": {
        "basic": [
            {"name": "HubSpot Academy", "url": "https://academy.hubspot.com/"},
            {"name": "Google Digital Garage", "url": "https://learndigital.withgoogle.com/digitalgarage"}
        ],
        "intermediate": [
            {"name": "Intermediate Marketing on Coursera", "url": "https://www.coursera.org/learn/marketing-strategy"},
            {"name": "MarketingProfs", "url": "https://www.marketingprofs.com/"}
        ],
        "advanced": [
            {"name": "Advanced Marketing on edX", "url": "https://www.edx.org/course/advanced-marketing"},
            {"name": "Nielsen Insights", "url": "https://www.nielsen.com/insights/"}
        ]
    },
    "Business Manager": {
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
    "Cybersecurity Analyst": {
        "basic": [
            {"name": "Cybrary Cybersecurity Courses", "url": "https://www.cybrary.it/"},
            {"name": "TryHackMe", "url": "https://tryhackme.com/"}
        ],
        "intermediate": [
            {"name": "Intermediate Cybersecurity on Coursera", "url": "https://www.coursera.org/learn/cybersecurity-intermediate"},
            {"name": "SANS Institute", "url": "https://www.sans.org/"}
        ],
        "advanced": [
            {"name": "Advanced Cybersecurity on edX", "url": "https://www.edx.org/course/advanced-cybersecurity"},
            {"name": "EC-Council", "url": "https://www.eccouncil.org/"}
        ]
    },
    "Environmental Engineer": {
        "basic": [
            {"name": "edX Environmental Engineering Courses", "url": "https://www.edx.org/learn/environmental-engineering"},
            {"name": "EPA Resources", "url": "https://www.epa.gov/"}
        ],
        "intermediate": [
            {"name": "Intermediate Environmental Engineering on Coursera", "url": "https://www.coursera.org/learn/environmental-engineering-intermediate"},
            {"name": "ASCE Learning", "url": "https://www.asce.org/learning/"}
        ],
        "advanced": [
            {"name": "Advanced Environmental Engineering on edX", "url": "https://www.edx.org/course/advanced-environmental-engineering"},
            {"name": "Green Building Council", "url": "https://www.usgbc.org/"}
        ]
    },
    "Ethical Hacker": {
        "basic": [
            {"name": "Hack The Box", "url": "https://www.hackthebox.com/"},
            {"name": "Offensive Security Certifications", "url": "https://www.offsec.com/"}
        ],
        "intermediate": [
            {"name": "Intermediate Ethical Hacking on Coursera", "url": "https://www.coursera.org/learn/ethical-hacking-intermediate"},
            {"name": "CEH Training", "url": "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/"}
        ],
        "advanced": [
            {"name": "Advanced Penetration Testing on edX", "url": "https://www.edx.org/course/advanced-penetration-testing"},
            {"name": "Black Hat Training", "url": "https://www.blackhat.com/training/"}
        ]
    },
    "Urban Planner": {
        "basic": [
            {"name": "Planetizen Courses", "url": "https://courses.planetizen.com/"},
            {"name": "American Planning Association", "url": "https://www.planning.org/"}
        ],
        "intermediate": [
            {"name": "Intermediate Urban Planning on Coursera", "url": "https://www.coursera.org/learn/urban-planning-intermediate"},
            {"name": "Urban Land Institute", "url": "https://uli.org/"}
        ],
        "advanced": [
            {"name": "Advanced Urban Design on edX", "url": "https://www.edx.org/course/advanced-urban-design"},
            {"name": "CNU Resources", "url": "https://www.cnu.org/"}
        ]
    },
    "Voice Actor": {
        "basic": [
            {"name": "Voices.com Learning Center", "url": "https://www.voices.com/learn"},
            {"name": "Backstage Voice Acting Guides", "url": "https://www.backstage.com/magazine/voiceover/"}
        ],
        "intermediate": [
            {"name": "Intermediate Voice Acting on Udemy", "url": "https://www.udemy.com/topic/voice-acting/"},
            {"name": "Voice123 Academy", "url": "https://academy.voice123.com/"}
        ],
        "advanced": [
            {"name": "Advanced Voiceover on Skillshare", "url": "https://www.skillshare.com/classes/advanced-voiceover"},
            {"name": "Actors Connection", "url": "https://actorsconnection.com/"}
        ]
    },
    "Astrophysicist": {
        "basic": [
            {"name": "NASA Astrophysics Resources", "url": "https://science.nasa.gov/astrophysics/"},
            {"name": "Coursera Astrophysics Courses", "url": "https://www.coursera.org/courses?query=astrophysics"}
        ],
        "intermediate": [
            {"name": "Intermediate Astrophysics on Coursera", "url": "https://www.coursera.org/learn/astrophysics-intermediate"},
            {"name": "Astronomy Magazine", "url": "https://www.astronomy.com/"}
        ],
        "advanced": [
            {"name": "Advanced Astrophysics on edX", "url": "https://www.edx.org/course/advanced-astrophysics"},
            {"name": "American Astronomical Society", "url": "https://aas.org/"}
        ]
    },
    "Wildlife Biologist": {
        "basic": [
            {"name": "Wildlife Society Resources", "url": "https://wildlife.org/"},
            {"name": "Khan Academy Biology", "url": "https://www.khanacademy.org/science/biology"}
        ],
        "intermediate": [
            {"name": "Intermediate Ecology on Coursera", "url": "https://www.coursera.org/learn/ecology-intermediate"},
            {"name": "National Geographic Education", "url": "https://www.nationalgeographic.org/education/"}
        ],
        "advanced": [
            {"name": "Advanced Conservation on edX", "url": "https://www.edx.org/course/advanced-conservation"},
            {"name": "IUCN Resources", "url": "https://www.iucn.org/"}
        ]
    },
    "Doctor (General Physician)": {
        "basic": [
            {"name": "Khan Academy Medicine", "url": "https://www.khanacademy.org/science/health-and-medicine"},
            {"name": "Medscape", "url": "https://www.medscape.com/"}
        ],
        "intermediate": [
            {"name": "Coursera Medical Courses", "url": "https://www.coursera.org/courses?query=medicine"},
            {"name": "Osmosis", "url": "https://www.osmosis.org/"}
        ],
        "advanced": [
            {"name": "UpToDate", "url": "https://www.uptodate.com/"},
            {"name": "NEJM Knowledge+", "url": "https://knowledgeplus.nejm.org/"}
        ]
    },
    "Nurse": {
        "basic": [
            {"name": "Nursing Times Learning", "url": "https://www.nursingtimes.net/"},
            {"name": "American Nurses Association", "url": "https://www.nursingworld.org/"}
        ],
        "intermediate": [
            {"name": "Intermediate Nursing on Coursera", "url": "https://www.coursera.org/learn/nursing-intermediate"},
            {"name": "NCLEX Prep", "url": "https://www.nclex.com/"}
        ],
        "advanced": [
            {"name": "Advanced Nursing on edX", "url": "https://www.edx.org/course/advanced-nursing"},
            {"name": "AACN Resources", "url": "https://www.aacnnursing.org/"}
        ]
    },
    "Medical Researcher": {
        "basic": [
            {"name": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/"},
            {"name": "ClinicalTrials.gov", "url": "https://clinicaltrials.gov/"}
        ],
        "intermediate": [
            {"name": "Intermediate Research Methods on Coursera", "url": "https://www.coursera.org/learn/research-methods"},
            {"name": "NIH Training", "url": "https://www.nih.gov/research-training"}
        ],
        "advanced": [
            {"name": "Advanced Scientific Writing on edX", "url": "https://www.edx.org/course/scientific-writing"},
            {"name": "Nature Research", "url": "https://www.nature.com/"}
        ]
    },
    "Teacher (Secondary Education)": {
        "basic": [
            {"name": "Edutopia", "url": "https://www.edutopia.org/"},
            {"name": "Teach.com", "url": "https://teach.com/"}
        ],
        "intermediate": [
            {"name": "Coursera Education Courses", "url": "https://www.coursera.org/courses?query=education"},
            {"name": "Classroom Management on EdX", "url": "https://www.edx.org/course/classroom-management"}
        ],
        "advanced": [
            {"name": "TESOL Certification", "url": "https://www.tesol.org/"},
            {"name": "ASCD Resources", "url": "https://www.ascd.org/"}
        ]
    },
    "Lawyer": {
        "basic": [
            {"name": "ABA Legal Education", "url": "https://www.americanbar.org/groups/legal_education/"},
            {"name": "Coursera Law Courses", "url": "https://www.coursera.org/courses?query=law"}
        ],
        "intermediate": [
            {"name": "LexisNexis Tutorials", "url": "https://www.lexisnexis.com/en-us/training"},
            {"name": "Westlaw Basics", "url": "https://www.westlaw.com/"}
        ],
        "advanced": [
            {"name": "Harvard Law Online", "url": "https://online-learning.harvard.edu/subject/law"},
            {"name": "BarPrep Courses", "url": "https://www.barbri.com/"}
        ]
    },
    "Mechanical Engineer": {
        "basic": [
            {"name": "ASME Learning", "url": "https://www.asme.org/learning-development"},
            {"name": "MIT OpenCourseWare - Mechanical Engineering", "url": "https://ocw.mit.edu/courses/mechanical-engineering/"}
        ],
        "intermediate": [
            {"name": "SolidWorks Tutorials", "url": "https://www.solidworks.com/support/tutorials"},
            {"name": "Coursera Mechanical Engineering", "url": "https://www.coursera.org/courses?query=mechanical%20engineering"}
        ],
        "advanced": [
            {"name": "ANSYS Learning Hub", "url": "https://www.ansys.com/training-center"},
            {"name": "Engineering Toolbox", "url": "https://www.engineeringtoolbox.com/"}
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
APTITUDE_MAPPING ={
    'Mathematics': 'numerical',
    'Logical Reasoning': 'logical',
    'Verbal Ability': 'verbal',
    'Science': 'science',
    'Spatial Reasoning': 'spatial',
    'History': 'history',
    'Geography': 'geography'
}