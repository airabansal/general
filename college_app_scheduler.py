from datetime import datetime, timedelta
import heapq


class ApplicationTask:

    def __init__(self, college_name, task_name, deadline_str, priority=2):
        """Represents an application task or submission milestone.

        :param college_name: str (e.g., "University of Oregon")
        :param task_name: str (e.g., "Submit Common App Essay", "Request LOR")
        :param deadline_str: str in "YYYY-MM-DD" format
        :param priority: int (1 = Highest/Critical, 2 = Normal, 3 = Low)
        """
        self.college_name = college_name
        self.task_name = task_name
        self.deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        self.priority = priority
        self.completed = False

    def __lt__(self, other):
        """Defines priority comparison for the Min-Heap.

        Sorts strictly by earliest deadline first, then by highest priority (lowest number).
        """
        if self.deadline == other.deadline:
            return self.priority < other.priority
        return self.deadline < other.deadline

    def days_remaining(self, current_date):
        """Calculates days left until deadline."""
        return (self.deadline - current_date).days


class DeadlineScheduler:

    def __init__(self):
        self.task_queue = []  # Min-heap storage
        self.completed_tasks = []

    def add_task(self, college_name, task_name, deadline_str, priority=2):
        """Adds a new task into the priority heap."""
        task = ApplicationTask(
            college_name, task_name, deadline_str, priority
        )
        heapq.heappush(self.task_queue, task)

    def get_upcoming_dashboard(self, current_date_str, lookahead_days=30):
        """Returns ordered list of upcoming active tasks within the lookahead window."""
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d").date()

        # Extract sorted copy from heap without destroying state
        ordered_tasks = sorted(self.task_queue)
        upcoming = []

        for task in ordered_tasks:
            days_left = task.days_remaining(current_date)
            if 0 <= days_left <= lookahead_days:
                upcoming.append((task, days_left))

        return upcoming, current_date

    def complete_next_urgent_task(self):
        """Pops and completes the single most urgent task off the heap."""
        if not self.task_queue:
            return None
        task = heapq.heappop(self.task_queue)
        task.completed = True
        self.completed_tasks.append(task)
        return task


# --- Execution & Demonstration ---
if __name__ == "__main__":
    scheduler = DeadlineScheduler()

    # Add sample college application milestones
    scheduler.add_task(
        "University of Oregon",
        "Submit Early Action Common App",
        "2026-11-01",
        priority=1,
    )
    scheduler.add_task(
        "Oregon State University",
        "Request Counselor Recommendation",
        "2026-10-15",
        priority=1,
    )
    scheduler.add_task(
        "Portland State University",
        "Submit FAFSA Financial Aid Form",
        "2026-12-01",
        priority=2,
    )
    scheduler.add_task(
        "UW Seattle",
        "Draft Supplemental Essay",
        "2026-10-25",
        priority=2,
    )
    scheduler.add_task(
        "Stanford University",
        "Submit Regular Decision Application",
        "2027-01-05",
        priority=1,
    )

    # Simulated Today's Date
    simulated_today = "2026-10-01"

    print("=" * 65)
    print("      COLLEGE APPLICATION DEADLINE PRIORITY SCHEDULER      ")
    print("=" * 65)
    print(f"📅 Simulated Today's Date: {simulated_today}\n")

    # 1. View Upcoming Schedule Dashboard (30-day window)
    upcoming_tasks, today = scheduler.get_upcoming_dashboard(
        simulated_today, lookahead_days=45
    )

    print(
        f"📋 UPCOMING TASKS (Next 45 Days) — Total Active: {len(scheduler.task_queue)}"
    )
    print("-" * 65)

    for task, days_left in upcoming_tasks:
        urgency_flag = "🚨 CRITICAL" if days_left <= 14 else "⏱️  UPCOMING"
        prio_label = "P1" if task.priority == 1 else "P2"
        print(
            f"[{urgency_flag}] {task.deadline} ({days_left:2d} days left) | [{prio_label}] {task.college_name}"
        )
        print(f"             Task: {task.task_name}\n")

    # 2. Complete the top priority task
    print("-" * 65)
    completed = scheduler.complete_next_urgent_task()
    if completed:
        print(
            f"✅ COMPLETED TOP TASK: '{completed.task_name}' for {completed.college_name}"
        )

    print(f"📊 Remaining Tasks in Heap: {len(scheduler.task_queue)}")
