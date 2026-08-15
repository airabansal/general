class Tutor:

    def __init__(self, name, subjects, available_slots, max_students=2):
        self.name = name
        self.subjects = set(subjects)  # e.g., {'Chemistry', 'Algebra'}
        self.available_slots = set(available_slots)  # e.g., {'Mon-P7', 'Wed-P7'}
        self.max_students = max_students
        self.assigned_tutees = []  # List of tuples: (tutee_name, subject, slot)

    def can_teach(self, subject, slot):
        """Checks if tutor is qualified and free at the requested time."""
        return (
            subject in self.subjects
            and slot in self.available_slots
            and len(self.assigned_tutees) < self.max_students
        )


class Tutee:

    def __init__(self, name, subject_needed, preferred_slots):
        self.name = name
        self.subject_needed = subject_needed
        self.preferred_slots = preferred_slots  # List of preferred time slots


class TutoringMatcher:

    def __init__(self, tutors, tutees):
        self.tutors = tutors
        self.tutees = tutees

    def match_students(self):
        """Greedy matching algorithm prioritizing tutees with fewer available slots."""
        matches = []
        unmatched = []

        # Sort tutees so those with fewer available time slots get matched first
        sorted_tutees = sorted(
            self.tutees, key=lambda t: len(t.preferred_slots)
        )

        for tutee in sorted_tutees:
            matched = False
            for slot in tutee.preferred_slots:
                # Find an available tutor for this subject and slot
                for tutor in self.tutors:
                    if tutor.can_teach(tutee.subject_needed, slot):
                        tutor.assigned_tutees.append(
                            (tutee.name, tutee.subject_needed, slot)
                        )
                        # Remove slot from tutor's availability so they aren't double-booked
                        tutor.available_slots.remove(slot)
                        matches.append(
                            {
                                "tutee": tutee.name,
                                "tutor": tutor.name,
                                "subject": tutee.subject_needed,
                                "slot": slot,
                            }
                        )
                        matched = True
                        break
                if matched:
                    break

            if not matched:
                unmatched.append(tutee)

        return matches, unmatched


# --- Sample Data ---
if __name__ == "__main__":
    tutors = [
        Tutor("Alex", ["Chemistry", "Biology"], ["Mon-P7", "Wed-P7"]),
        Tutor("Jordan", ["Algebra", "Chemistry"], ["Tue-P7", "Wed-P7"]),
        Tutor("Taylor", ["Spanish", "Algebra"], ["Mon-P7", "Thu-P7"]),
    ]

    tutees = [
        Tutee("Aira Bansal", "Chemistry", ["Wed-P7", "Tue-P7"]),  # Added student
        Tutee("Sam", "Chemistry", ["Wed-P7"]),
        Tutee("Maya", "Algebra", ["Mon-P7", "Thu-P7"]),
        Tutee("Chris", "Chemistry", ["Mon-P7", "Wed-P7"]),
        Tutee("Jamie", "Physics", ["Tue-P7"]),
    ]

    matcher = TutoringMatcher(tutors, tutees)
    successful_matches, unmatched_students = matcher.match_students()

    print("==================================================")
    print("      HIGH SCHOOL PEER-TUTORING MATCH RESULTS     ")
    print("==================================================")

    print("\n✅ Successful Matches:")
    print("-" * 50)
    for m in successful_matches:
        print(
            f"• {m['tutee']}  -->  Tutor: {m['tutor']} | Subject: {m['subject']} | Slot: {m['slot']}"
        )

    print("\n⚠️ Unmatched Students (Need Follow-up):")
    print("-" * 50)
    for u in unmatched_students:
        print(
            f"• {u.name} (Needs: {u.subject_needed} | Requested: {', '.join(u.preferred_slots)})"
        )
