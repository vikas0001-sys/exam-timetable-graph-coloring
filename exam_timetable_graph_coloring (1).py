"""
Project 8: Exam Timetable Generation Using Graph Coloring
Algorithm: Backtracking Graph Coloring

How to run:
    python exam_timetable_graph_coloring.py

The sample data below represents students enrolled in each subject.
Two subjects conflict if at least one student is enrolled in both.
"""

def build_conflict_graph(subject_students):
    """Return an adjacency list: each subject maps to conflicting subjects."""
    subjects = list(subject_students.keys())
    graph = {subject: set() for subject in subjects}

    for i in range(len(subjects)):
        for j in range(i + 1, len(subjects)):
            subject_a = subjects[i]
            subject_b = subjects[j]

            # A shared student means these exams cannot be at the same time.
            if set(subject_students[subject_a]) & set(subject_students[subject_b]):
                graph[subject_a].add(subject_b)
                graph[subject_b].add(subject_a)

    return graph


def is_safe(subject, slot, assignment, graph):
    """Check whether a slot is free from conflicts for this subject."""
    for neighbour in graph[subject]:
        if assignment.get(neighbour) == slot:
            return False
    return True


def color_graph_backtracking(subjects, graph, max_slots, assignment, index=0):
    """Try assigning slots 1..max_slots using recursive backtracking."""
    if index == len(subjects):
        return True

    subject = subjects[index]

    for slot in range(1, max_slots + 1):
        if is_safe(subject, slot, assignment, graph):
            assignment[subject] = slot

            if color_graph_backtracking(
                subjects, graph, max_slots, assignment, index + 1
            ):
                return True

            # Undo the choice and try another slot.
            del assignment[subject]

    return False


def generate_timetable(graph):
    """
    Find a valid timetable using the minimum number of slots.
    The search starts at one slot and increases until a solution is found.
    """
    # Higher-degree subjects are considered first to improve search efficiency.
    subjects = sorted(graph, key=lambda subject: len(graph[subject]), reverse=True)

    for number_of_slots in range(1, len(subjects) + 1):
        assignment = {}
        if color_graph_backtracking(
            subjects, graph, number_of_slots, assignment
        ):
            return assignment, number_of_slots

    return {}, 0


def display_timetable(assignment, number_of_slots):
    """Print the generated examination timetable."""
    print("\\n========== EXAMINATION TIMETABLE ==========")
    for slot in range(1, number_of_slots + 1):
        exams = sorted(
            subject for subject, assigned_slot in assignment.items()
            if assigned_slot == slot
        )
        print(f"Slot {slot}: {', '.join(exams)}")
    print("-------------------------------------------")
    print(f"Minimum number of slots required: {number_of_slots}")


def main():
    # Sample student enrollment data.
    # Replace these lists with the actual students enrolled in each subject.
    subject_students = {
        "Mathematics": ["S1", "S2", "S3", "S4"],
        "Physics":     ["S2", "S5", "S6"],
        "Chemistry":   ["S1", "S5", "S7"],
        "Computer":    ["S3", "S6", "S8"],
        "English":     ["S4", "S7", "S8"],
        "Biology":     ["S9", "S10"]
    }

    graph = build_conflict_graph(subject_students)

    print("========== SUBJECT CONFLICT GRAPH ==========")
    for subject in graph:
        neighbours = sorted(graph[subject])
        print(f"{subject}: {', '.join(neighbours) if neighbours else 'No conflicts'}")

    assignment, number_of_slots = generate_timetable(graph)
    display_timetable(assignment, number_of_slots)


if __name__ == "__main__":
    main()
