class APExamEstimator:

    # Official College Board scoring curves and weighted composite limits
    EXAM_CONFIGS = {
        "AP Computer Science A": {
            "mc_max": 40,
            "mc_weight": 1.0,  # 50% of exam (40 composite pts)
            "frq_sections": [
                {"name": "Q1: Methods & Control Structures", "max": 9},
                {"name": "Q2: Class Design", "max": 9},
                {"name": "Q3: Array/ArrayList", "max": 9},
                {"name": "Q4: 2D Array", "max": 9},
            ],
            "frq_weight": 1.1111,  # 36 raw pts * 1.1111 = 40 composite pts
            "max_composite": 80,
            "cutoffs": {5: 62, 4: 49, 3: 37, 2: 26},  # Estimated composite thresholds
        },
        "AP Calculus AB": {
            "mc_max": 45,
            "mc_weight": 1.2,  # 45 raw pts * 1.2 = 54 composite pts (50%)
            "frq_sections": [
                {"name": "FRQ 1 (Graphing Calculator)", "max": 6},
                {"name": "FRQ 2 (Graphing Calculator)", "max": 6},
                {"name": "FRQ 3 (No Calculator)", "max": 6},
                {"name": "FRQ 4 (No Calculator)", "max": 6},
                {"name": "FRQ 5 (No Calculator)", "max": 6},
                {"name": "FRQ 6 (No Calculator)", "max": 6},
            ],
            "frq_weight": 1.5,  # 36 raw pts * 1.5 = 54 composite pts (50%)
            "max_composite": 108,
            "cutoffs": {5: 68, 4: 54, 3: 41, 2: 30},
        },
        "AP US History": {
            "mc_max": 55,
            "mc_weight": 1.0,  # 40% of exam
            "frq_sections": [
                {"name": "Short Answer Questions (SAQs)", "max": 9},  # 20%
                {"name": "Document-Based Question (DBQ)", "max": 7},  # 25%
                {"name": "Long Essay Question (LEQ)", "max": 6},  # 15%
            ],
            # Custom Section Weighting for APUSH FRQs
            "custom_frq_weights": [2.22, 3.57, 2.5],
            "max_composite": 100,
            "cutoffs": {5: 72, 4: 60, 3: 48, 2: 36},
        },
    }

    def __init__(self, exam_name):
        if exam_name not in self.EXAM_CONFIGS:
            raise ValueError(
                f"Exam '{exam_name}' not supported. Choose from: {list(self.EXAM_CONFIGS.keys())}"
            )
        self.exam_name = exam_name
        self.config = self.EXAM_CONFIGS[exam_name]

    def estimate_score(self, mc_correct, frq_scores):
        """Calculates composite score and estimates AP 1-5 grade.

        :param mc_correct: int (Number of multiple choice questions correct)
        :param frq_scores: list of ints (Raw points for each FRQ section)
        """
        # 1. Validate inputs
        if mc_correct < 0 or mc_correct > self.config["mc_max"]:
            raise ValueError(
                f"MC score must be between 0 and {self.config['mc_max']}"
            )

        if len(frq_scores) != len(self.config["frq_sections"]):
            raise ValueError(
                f"Expected {len(self.config['frq_sections'])} FRQ scores, got {len(frq_scores)}"
            )

        # 2. Calculate Weighted MC Composite
        mc_composite = mc_correct * self.config["mc_weight"]

        # 3. Calculate Weighted FRQ Composite
        frq_composite = 0.0
        if "custom_frq_weights" in self.config:
            for score, weight in zip(
                frq_scores, self.config["custom_frq_weights"]
            ):
                frq_composite += score * weight
        else:
            total_raw_frq = sum(frq_scores)
            frq_composite = total_raw_frq * self.config["frq_weight"]

        # 4. Total Composite Score
        total_composite = round(mc_composite + frq_composite)

        # 5. Determine AP Grade (1–5) based on composite cutoffs
        ap_score = 1
        for score, cutoff in sorted(
            self.config["cutoffs"].items(), key=lambda x: x[1], reverse=True
        ):
            if total_composite >= cutoff:
                ap_score = score
                break

        return {
            "exam_name": self.exam_name,
            "mc_correct": mc_correct,
            "mc_max": self.config["mc_max"],
            "mc_composite": round(mc_composite, 1),
            "frq_composite": round(frq_composite, 1),
            "total_composite": total_composite,
            "max_composite": self.config["max_composite"],
            "ap_score": ap_score,
            "cutoffs": self.config["cutoffs"],
        }

    def print_diagnostic_report(self, mc_correct, frq_scores):
        """Prints a detailed diagnostic score breakdown."""
        res = self.estimate_score(mc_correct, frq_scores)

        print("\n" + "=" * 65)
        print(f"      AP EXAM SCORE ESTIMATOR & DIAGNOSTIC: {self.exam_name.upper()}")
        print("=" * 65)

        print(f"📊 SECTION BREAKDOWN")
        print(
            f"   • Multiple Choice : {res['mc_correct']} / {res['mc_max']} correct "
            f"({res['mc_correct']/res['mc_max']*100:.1f}%) ➔ {res['mc_composite']} composite pts"
        )

        print(f"\n✍️  FREE RESPONSE BREAKDOWN")
        for section, score in zip(self.config["frq_sections"], frq_scores):
            pct = (score / section["max"]) * 100
            print(
                f"   • {section['name']:<35} : {score:>2}/{section['max']} pts ({pct:>5.1f}%)"
            )
        print(f"   ➔ Weighted FRQ Composite Subtotal: {res['frq_composite']} pts")

        # Projected AP Score Result
        print("-" * 65)
        print(
            f"🎯 TOTAL COMPOSITE SCORE : {res['total_composite']} / {res['max_composite']} pts"
        )

        score_emojis = {5: "🏆 5 (Extremely Well Qualified)", 4: "🌟 4 (Well Qualified)", 3: "✅ 3 (Qualified - Passing)", 2: "⚠️ 2 (Possibly Qualified)", 1: "❌ 1 (No Recommendation)"}
        print(f"🔥 PROJECTED AP SCORE   : {score_emojis[res['ap_score']]}")
        print("-" * 65)

        # Cutoff Context
        print("📈 SCORE THRESHOLD REFERENCE")
        for score_val, cutoff in sorted(
            res["cutoffs"].items(), reverse=True
        ):
            indicator = "👈 YOUR RANGE" if res["ap_score"] == score_val else ""
            print(f"   • AP {score_val} : {cutoff}+ composite pts {indicator}")

        print("=" * 65 + "\n")


# --- Demonstration Run ---
if __name__ == "__main__":
    # Example 1: AP Computer Science A
    csa_estimator = APExamEstimator("AP Computer Science A")
    # MC: 32/40 correct | FRQ Scores: Q1=7/9, Q2=8/9, Q3=6/9, Q4=7/9
    csa_estimator.print_diagnostic_report(
        mc_correct=32, frq_scores=[7, 8, 6, 7]
    )

    # Example 2: AP Calculus AB
    calc_estimator = APExamEstimator("AP Calculus AB")
    # MC: 28/45 correct | FRQ Scores: [4, 5, 3, 4, 2, 5] out of 6
    calc_estimator.print_diagnostic_report(
        mc_correct=28, frq_scores=[4, 5, 3, 4, 2, 5]
    )
