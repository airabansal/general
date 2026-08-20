import math
import re
from collections import Counter


class EssayAnalyzer:

    DEFAULT_CLICHES = [
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
        "at the end of the day",
        "sparked my interest",
    ]

    COMMON_STOPWORDS = {
        "a",
        "an",
        "the",
        "and",
        "or",
        "but",
        "if",
        "because",
        "as",
        "what",
        "when",
        "where",
        "how",
        "who",
        "which",
        "this",
        "that",
        "these",
        "those",
        "then",
        "just",
        "so",,
        "than",
        "such",
        "both",
        "through",
        "about",
        "into",
        "over",,
        "after",
        "with",
        "for",
        "to",
        "of",,
        "in",
        "on",
        "at",
        "by",
        "from",
        "is",,
        "am",
        "are",
        "was",
        "were",
        "be",
        "been",,
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",,
        "did",
        "can",
        "could",
        "will",
        "would",,
        "should",
        "i",
        "my",
        "me",
        "myself",,
        "we",
        "our",
        "us",
        "you",
        "your",
    }

    def __init__(self, min_words=250, max_words=650, custom_cliches=None):
        self.min_words = min_words
        self.max_words = max_words
        self.cliches = (
            custom_cliches if custom_cliches is not None else self.DEFAULT_CLICHES
        )

    def _count_syllables(self, word):
        """Estimates syllable count of an individual word using vowel-group heuristics."""
        word = word.lower()
        if len(word) <= 3:
            return 1
        word = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", word)
        word = re.sub(r"^y", "", word)
        syllables = len(re.findall(r"[aeiouy]{1,2}", word))
        return max(1, syllables)

    def _detect_passive_voice(self, sentences):
        """Flags candidate passive voice sentences using Auxiliary Verb + Past Participle patterns."""
        passive_patterns = r"\b(am|is|are|was|were|be|been|being)\b\s+(\w+ed|\w+en|made|done|built|given|taken|led)\b"
        matches = []
        for sent in sentences:
            found = re.findall(
                passive_patterns, sent, re.IGNORECASE
            )
            if found:
                matches.append(sent.strip())
        return matches

    def analyze(self, essay_text):
        """Runs complete linguistic analysis on the provided essay string."""
        # 1. Clean Tokenization
        raw_words = re.findall(r"\b[a-zA-Z']+\b", essay_text)
        sentences = [
            s.strip()
            for s in re.split(r"[.!?]+", essay_text)
            if s.strip()
        ]

        word_count = len(raw_words)
        sentence_count = max(1, len(sentences))
        total_syllables = sum(self._count_syllables(w) for w in raw_words)

        # 2. Length Status
        if word_count < self.min_words:
            status = f"TOO SHORT ({word_count}/{self.min_words} min words)"
            is_valid = False
        elif word_count > self.max_words:
            status = f"TOO LONG ({word_count}/{self.max_words} max words)"
            is_valid = False
        else:
            status = f"VALID ({word_count} words)"
            is_valid = True

        # 3. Readability Index (Flesch-Kincaid)
        # Formula: 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
        words_per_sentence = word_count / sentence_count
        syllables_per_word = (
            total_syllables / word_count if word_count > 0 else 0
        )
        flesch_score = round(
            206.835
            - (1.015 * words_per_sentence)
            - (84.6 * syllables_per_word),
            1,
        )

        grade_level = round(
            (0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59,
            1,
        )

        # 4. Cliché Detection
        essay_lower = essay_text.lower()
        found_cliches = []
        for c in self.cliches:
            pattern = r"\b" + re.escape(c.lower()) + r"\b"
            occurrences = len(re.findall(pattern, essay_lower))
            if occurrences > 0:
                found_cliches.append((c, occurrences))

        # 5. Overused Words (excluding common stopwords)
        content_words = [
            w.lower()
            for w in raw_words
            if w.lower() not in self.COMMON_STOPWORDS
        ]
        top_repeated = Counter(content_words).most_common(5)

        # 6. Passive Voice Detection
        passive_instances = self._detect_passive_voice(sentences)

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "length_status": status,
            "is_valid_length": is_valid,
            "flesch_score": flesch_score,
            "grade_level": max(0.0, grade_level),
            "found_cliches": found_cliches,
            "top_repeated_words": top_repeated,
            "passive_sentences": passive_instances,
        }

    def print_dashboard(self, essay_text):
        """Prints a formatted report dashboard to terminal."""
        res = self.analyze(essay_text)

        print("=" * 65)
        print("          COLLEGE COMMON APP ESSAY ANALYZER v2.0         ")
        print("=" * 65)

        # Section 1: Overview & Limits
        length_icon = "✅" if res["is_valid_length"] else "❌"
        print(f"\n📊 ESSAY LENGTH METRICS")
        print(f"   • Total Word Count : {res['word_count']} words")
        print(f"   • Sentence Count   : {res['sentence_count']} sentences")
        print(f"   • Validation Status: {length_icon} {res['length_status']}")

        # Section 2: Readability
        print(f"\n📖 READABILITY & COMPLEXITY")
        print(f"   • Flesch Reading Ease : {res['flesch_score']} / 100")
        print(
            f"   • Grade Level         : Grade {res['grade_level']} (Ideal for Common App: 8-11)"
        )

        # Section 3: Clichés
        print(f"\n⚠️  CLICHÉ & BUZZWORD DETECTION")
        if res["found_cliches"]:
            for phrase, count in res["found_cliches"]:
                print(f"   ❌ '{phrase}' (found {count}x)")
        else:
            print("   ✅ No common admissions clichés detected.")

        # Section 4: Passive Voice
        print(f"\n🔍 PASSIVE VOICE INSTANCES ({len(res['passive_sentences'])})")
        if res["passive_sentences"]:
            for i, sent in enumerate(res["passive_sentences"][:3], 1):
                print(f'   {i}. "{sent}"')
        else:
            print("   ✅ Strong active voice throughout.")

        # Section 5: Word Repetition
        print(f"\n🔁 TOP REPEATED CONTENT WORDS")
        for word, count in res["top_repeated_words"]:
            print(f"   • {word:<12} : {count} times")

        print("\n" + "=" * 65)


# --- Execution Example ---
if __name__ == "__main__":
    sample_essay = """
    Since the dawn of time, human curiosity has driven discovery. Growing up in Oregon, 
    I spent my weekends exploring local parks and fixing broken household electronics. 
    Entering high school pushed me way outside my comfort zone, forcing me to take risks.
    
    In my junior year, the annual science fair was organized by our student committee. 
    A low-cost solar water heater was built by our team using recycled copper pipes and wood. 
    It was a life-changing experience that sparked my interest in renewable energy engineering.
    
    Through this project, I developed a true passion for sustainable design. I learned that 
    engineering is not just about solving isolated equations, but about creating tools that 
    broaden my horizons and directly support people in today's society.
    """

    analyzer = EssayAnalyzer(min_words=250, max_words=650)
    analyzer.print_dashboard(sample_essay)
