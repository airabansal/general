class GraduationAuditor:

    def __init__(self, student_name, target_diploma="Standard High School"):
        self.student_name = student_name
        self.target_diploma = target_diploma

        # Core graduation credit requirements (1 credit = 1 full year / 2 semesters)
        self.requirements = {
            "English": 4.0,
            "Mathematics": 3.0,
            "Science": 3.0,  # e.g., 1 Life, 1 Physical, 1 Advanced
            "Social Studies": 3.0,  # e.g., World History, US History, Gov/Econ
            "Foreign Language": 2.0,  # Same language
            "Visual & Performing Arts": 1.0,  # Category F
            "Physical Education": 2.0,
            "Electives": 4.0,
        }

        self.transcript = []

    def add_course(
        self, course_name, category, credits, grade, status="Completed"
    ):
        """Adds a completed or in-progress course to the student's transcript.

        :param course_name: str (e.g., "AP English Literature")
        :param category: str (e.g., "English", "Mathematics", "Science")
        :param credits: float (e.g., 1.0 for full year, 0.5 for semester)
        :param grade: str ("A", "B", "C", "D", "F", or "IP" for In-Progress)
        :param status: str ("Completed" or "In-Progress")
        """
        # Failing grades do not grant earned credit
        earned_credits = 0.0 if grade in ["F", "NP"] else float(credits)

        self.transcript.append({
            "course": course_name,
            "category": category,
            "credits": earned_credits,
            "grade": grade,
            "status": status,
        })

    def audit_transcript(self):
        """Audits transcript against degree requirements and calculates missing credits."""
        category_totals = {cat: 0.0 for cat in self.requirements}
        overflow_electives = 0.0

        # Sum earned credits per category
        for entry in self.transcript:
            cat = entry["category"]
            credits = entry["credits"]

            if cat in category_totals:
                # If category requirement is already fulfilled, extra credits roll into Electives
                current_req = self.requirements[cat]
                current_total = category_totals[cat]

                if current_total + credits > current_req:
                    overflow = (current_total + credits) - current_req
                    category_totals[cat] = current_req
                    category_totals["Electives"] += overflow
                else:
                    category_totals[cat] += credits
            else:
                # Any unrecognized category defaults to Electives
                category_totals["Electives"] += credits

        return category_totals

    def print_audit_report(self):
        """Prints a comprehensive graduation eligibility report."""
        earned_totals = self.audit_transcript()

        total_req_credits = sum(self.requirements.values())
        total_earned_credits = sum(earned_totals.values())

        print("\n" + "=" * 68)
        print(f"   GRADUATION CREDIT AUDIT REPORT: {self.student_name.upper()}")
        print(f"   Diploma Track: {self.target_diploma}")
        print("=" * 68)

        print(
            f"\n{'Subject Category':<26} | {'Earned':<8} | {'Required':<8} | {'Status'}"
        )
        print("-" * 68)

        missing_requirements = []

        for cat, req_credits in self.requirements.items():
            earned = earned_totals.get(cat, 0.0)
            diff = req_credits - earned

            if diff <= 0:
                status_str = "✅ COMPLETE"
            else:
                status_str = f"❌ NEED {diff:.1f} MORE"
                missing_requirements.append((cat, diff))

            print(
                f"{cat:<26} | {earned:>6.1f}   | {req_credits:>6.1f}   | {status_str}"
            )

        print("-" * 68)
        print(
            f"{'TOTAL CREDITS':<26} | {total_earned_credits:>6.1f}   | {total_req_credits:>6.1f}   |"
        )
        print("=" * 68)

        # Final Graduation Verdict
        if not missing_requirements:
            print(
                "\n🎓 ELIGIBILITY STATUS: ON TRACK TO GRADUATE! All core requirements met."
            )
        else:
            print(
                f"\n⚠️  ELIGIBILITY STATUS: INCOMPLETE ({len(missing_requirements)} category deficiency/deficiencies detected)"
            )
            print("   Action Plan - Required Courses Needed:")
            for cat, missing in missing_requirements:
                print(f"    • {cat}: Complete {missing:.1f} additional credit(s)")

        print("=" * 68 + "\n")


# --- Example Usage ---
if __name__ == "__main__":
    # Initialize auditor for a 12th-grade student
    student_audit = GraduationAuditor(
        student_name="Alex Rivera", target_diploma="College Prep / A-G Track"
    )

    # Populate Transcript Data
    # English (3.0 earned / 4.0 needed)
    student_audit.add_course(
        "English 9", "English", 1.0, "A", status="Completed"
    )
    student_audit.add_course(
        "English 10", "English", 1.0, "B", status="Completed"
    )
    student_audit.add_course(
        "AP English Language", "English", 1.0, "B", status="Completed"
    )

    # Mathematics (3.0 earned / 3.0 needed)
    student_audit.add_course(
        "Algebra 1", "Mathematics", 1.0, "B", status="Completed"
    )
    student_audit.add_course(
        "Geometry", "Mathematics", 1.0, "A", status="Completed"
    )
    student_audit.add_course(
        "Algebra 2", "Mathematics", 1.0, "B", status="Completed"
    )
    student_audit.add_course(
        "AP Calculus AB", "Mathematics", 1.0, "A", status="Completed"
    )  # Extra Math rolls to Electives

    # Science (2.0 earned / 3.0 needed)
    student_audit.add_course(
        "Biology", "Science", 1.0, "A", status="Completed"
    )
    student_audit.add_course(
        "Chemistry", "Science", 1.0, "C", status="Completed"
    )

    # Social Studies (3.0 earned / 3.0 needed)
    student_audit.add_course(
        "World History", "Social Studies", 1.0, "A", status="Completed"
    )
    student_audit.add_course(
        "US History", "Social Studies", 1.0, "B", status="Completed"
    )
    student_audit.add_course(
        "US Government", "Social Studies", 0.5, "A", status="Completed"
    )
    student_audit.add_course(
        "Economics", "Social Studies", 0.5, "A", status="Completed"
    )

    # Foreign Language & Arts
    student_audit.add_course(
        "Spanish 1", "Foreign Language", 1.0, "B", status="Completed"
    )
    student_audit.add_course(
        "Spanish 2", "Foreign Language", 1.0, "B", status="Completed"
    )
    student_audit.add_course(
        "Symphonic Band",
        "Visual & Performing Arts",
        1.0,
        "A",
        status="Completed",
    )

    # Physical Education & Electives
    student_audit.add_course(
        "PE 9", "Physical Education", 1.0, "A", status="Completed"
    )
    student_audit.add_course(
        "PE 10", "Physical Education", 1.0, "A", status="Completed"
    )
    student_audit.add_course(
        "Intro to Computer Science", "Electives", 1.0, "A", status="Completed"
    )
    student_audit.add_course(
        "Journalism", "Electives", 1.0, "A", status="Completed"
    )

    # Run audit report
    student_audit.print_audit_report()
