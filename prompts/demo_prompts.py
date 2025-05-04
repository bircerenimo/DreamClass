DEMO_PROMPTS = {
    "star_wars": {
        "universe": "Star Wars",
        "topics": {
            "environmental_science": {
                "prompt": """Create an engaging lesson plan in the Star Wars universe for Environmental Science:
                1. Write a captivating story that integrates environmental concepts within the Star Wars universe
                2. Create 3 challenging quiz questions about ecosystem balance on different planets
                3. Suggest visual elements showing Tatooine's desert ecosystem vs Hoth's ice ecosystem
                4. Include interactive activities like "Design a sustainable moisture farm"
                5. Provide a "dream power score" based on creativity and engagement
                Target grade level: {grade}""",
                "example": {
                    "grade": "8",
                    "story": """On the desert planet Tatooine, moisture farmers face the challenge of preserving water resources...""",
                    "quiz": [
                        {"question": "What is the main environmental challenge on Tatooine?", "answer": "Water scarcity"},
                        {"question": "How do moisture farmers contribute to environmental sustainability?", "answer": "By collecting atmospheric moisture"},
                        {"question": "What is the relationship between Tatooine's ecosystem and moisture farming?", "answer": "Moisture farming helps maintain the planet's water cycle"}
                    ]
                }
            },
            "physics": {
                "prompt": """Create an engaging lesson plan in the Star Wars universe for Physics:
                1. Write a captivating story that integrates physics concepts within the Star Wars universe
                2. Create 3 challenging quiz questions about force fields and energy
                3. Suggest visual elements showing lightsaber physics and starship propulsion
                4. Include interactive activities like "Design a lightsaber using physics principles"
                5. Provide a "dream power score" based on creativity and engagement
                Target grade level: {grade}""",
                "example": {
                    "grade": "10",
                    "story": """In a secret Jedi training facility, young Padawans learn about the physics behind lightsabers...""",
                    "quiz": [
                        {"question": "What physics principle explains lightsaber energy containment?", "answer": "Plasma containment"},
                        {"question": "How does the Force relate to physics concepts?", "answer": "It manipulates energy fields"},
                        {"question": "What physics concept is used in hyperdrive technology?", "answer": "Warp field manipulation"}
                    ]
                }
            }
        }
    },
    "harry_potter": {
        "universe": "Harry Potter",
        "topics": {
            "math": {
                "prompt": """Create an engaging lesson plan in the Harry Potter universe for Mathematics:
                1. Write a captivating story that integrates math concepts within Hogwarts
                2. Create 3 challenging quiz questions about magical calculations
                3. Suggest visual elements showing magical arithmetic and potion measurements
                4. Include interactive activities like "Calculate the perfect potion ratio"
                5. Provide a "dream power score" based on creativity and engagement
                Target grade level: {grade}""",
                "example": {
                    "grade": "7",
                    "story": """In Professor Flitwick's classroom, students learn about magical ratios and proportions...""",
                    "quiz": [
                        {"question": "What is the correct ratio for Polyjuice Potion ingredients?", "answer": "1:3:2"},
                        {"question": "How many Galleons make up one Knut?", "answer": "29"},
                        {"question": "What mathematical concept explains the shrinking effect of a Shrinking Solution?", "answer": "Exponential decay"}
                    ]
                }
            },
            "history": {
                "prompt": """Create an engaging lesson plan in the Harry Potter universe for History:
                1. Write a captivating story that integrates historical concepts within the wizarding world
                2. Create 3 challenging quiz questions about magical history
                3. Suggest visual elements showing historical events in the wizarding world
                4. Include interactive activities like "Create a timeline of magical events"
                5. Provide a "dream power score" based on creativity and engagement
                Target grade level: {grade}""",
                "example": {
                    "grade": "9",
                    "story": """In the Room of Requirement, students explore the history of magical artifacts...""",
                    "quiz": [
                        {"question": "When was the International Statute of Secrecy established?", "answer": "1692"},
                        {"question": "What event marked the end of the First Wizarding War?", "answer": "Voldemort's first defeat"},
                        {"question": "Who founded Hogwarts School of Witchcraft and Wizardry?", "answer": "Four founders: Godric Gryffindor, Helga Hufflepuff, Rowena Ravenclaw, Salazar Slytherin"}
                    ]
                }
            }
        }
    }
}

def get_demo_prompt(universe, topic, grade):
    """Return a demo prompt for the given universe and topic"""
    if universe in DEMO_PROMPTS and topic in DEMO_PROMPTS[universe]["topics"]:
        prompt = DEMO_PROMPTS[universe]["topics"][topic]["prompt"].format(grade=grade)
        return prompt
    return None

def get_demo_example(universe, topic):
    """Return a demo example for the given universe and topic"""
    if universe in DEMO_PROMPTS and topic in DEMO_PROMPTS[universe]["topics"]:
        return DEMO_PROMPTS[universe]["topics"][topic]["example"]
    return None
