import re


def analyze_essay(essay_text, cda_cliches=None):
    """Analyzes a college essay for word count validity, cliché usage, and basic readability stats.

    :param essay_text: str, the body of the essay
    :param cda_cliches: list of str, optional list of cliché phrases to flag
    :return: dict containing word count status, flagged clichés, and essay stats
    """
    if cda_cliches is None:
        cda_cliches = [
            "outside my comfort zone",
            "since the dawn of time",
            "passion for",
            "make a difference",
            "broaden my horizons",
            "think outside the box",
            "life-changing experience",
            "rollercoaster of emotions",
            "in today's society",
            "always been my dream",
        ]

    # 1. Clean and count words using regex (matches sequence of word characters and apostrophes)
    words = re.findall(r"\b[\w']+\b", essay_text)
    word_count = len(words)

    # 2. Check Common App Word Bounds (250 to 650 words)
    MIN_WORDS, MAX_WORDS = 250, 650
    if word_count < MIN_WORDS:
        word_status = (
            f"Too Short ({word_count} words). Need at least {MIN_WORDS} words."
        )
        is_valid_length = False
    elif word_count > MAX_WORDS:
        word_status = f"Too Long ({word_count} words). Exceeds limit of {MAX_WORDS} words by {word_count - MAX_WORDS}."
        is_valid_length = False
    else:
        word_status = f"Valid ({word_count} words)."
        is_valid_length = True

    # 3. Detect Clichés using Case-Insensitive Regex
    detected_cliches = []
    essay_lower = essay_text.lower()

    for cliche in cda_cliches:
        # Match cliché phrase as whole words
        pattern = r"\b" + re.escape(cliche.lower()) + r"\b"
        matches = re.findall(pattern, essay_lower)
        if matches:
            detected_cliches.append(
                {"phrase": cliche, "occurrences": len(matches)}
            )

    return {
        "word_count": word_count,
        "is_valid_length": is_valid_length,
        "word_status": word_status,
        "cliches_found": detected_cliches,
        "total_cliches_count": sum(c["occurrences"] for c in detected_cliches),
    }


# --- Demonstration & Test Suite ---
if __name__ == "__main__":
    sample_essay = """
    Since the dawn of time, humans have strived to overcome obstacles. Growing up in my hometown, 
    I always thought my path was clear, but entering high school pushed me way outside my comfort zone. 
    Joining the robotics team was a life-changing experience that changed how I solve problems.
    
    Before joining the team, I was terrified of public speaking and technical leadership. 
    However, running our outreach event showed me how to think outside the box when resources were low. 
    I developed a true passion for software engineering through long hours in the lab.
    
    This journey taught me that failure is simply a stepping stone to success. I know that attending 
    college will allow me to broaden my horizons and continue to make a difference in my community.
    """

    results = analyze_essay(sample_essay)

    print("==================================================")
    print("      COLLEGE ESSAY ANALYZER RESULTS              ")
    print("==================================================")
    print(f"📄 Word Count: {results['word_count']}")
    print(f"📊 Length Status: {results['word_status']}")
    print(f"⚠️  Clichés Detected: {results['total_cliches_count']}")
    print("-" * 50)

    if results["cliches_found"]:
        print("Flagged Overused Phrases:")
        for item in results["cliches_found"]:
            print(
                f"  • '{item['phrase']}' (found {item['occurrences']} time(s))"
            )
    else:
        print("🎉 No common clichés detected!")
