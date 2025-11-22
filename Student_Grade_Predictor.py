# Student Grade Predictor / Performance Analyzer (Beginner style, tweaked)
# Assumptions:
#  - Marks are on a 0-100 scale
#  - Attendance is a percentage 0-100
#  - Extracurricular score is 0-10
#  - If no assignments were given, the student is not penalized

# ---------- Simple configuration ----------
WEIGHTS = {
    "base_marks": 60,          # how much average marks contribute (out of total positive)
    "attendance": 10,          # bonus for good attendance
    "assignments": 8,          # bonus for assignments completion
    "improvement": 7,          # bonus for improvement over previous term
    "extracurricular": 5,      # small bonus for extra activities
    "consistency_penalty": -10,# penalty if subject marks vary a lot
    "fail_penalty": -15        # penalty for each failed subject
}

PASS_MARK = 40      # below this is considered a fail
GOOD_ATTENDANCE = 75  # percentage considered good attendance

# ---------- tiny helper functions (very simple) ----------
def safe_float(s, default=0.0):
    """Try to convert to float; return default on failure."""
    try:
        return float(s)
    except:
        return default

def mean(numbers):
    """Return average of a list, or 0 if empty."""
    if len(numbers) == 0:
        return 0.0
    return sum(numbers) / len(numbers)

def variance(numbers):
    """Return simple population variance (beginner-friendly)."""
    if len(numbers) == 0:
        return 0.0
    m = mean(numbers)
    total = 0.0
    for x in numbers:
        total += (x - m) * (x - m)
    return total / len(numbers)

def mask_name(name):
    """Show first letter + stars, simple privacy."""
    name = name.strip()
    if name == "":
        return ""
    if len(name) <= 2:
        return name[0] + "*"
    return name[0] + "*" * (len(name)-1)

# ---------- core analysis (straightforward) ----------
def analyze(marks, attendance_pct, assignments_done, assignments_total,
            extracurricular_score, previous_avg):
    """
    marks: list of numeric marks (0-100)
    attendance_pct: 0-100
    assignments_done / assignments_total: integers
    extracurricular_score: 0-10
    previous_avg: float or None
    returns: (score, list_of_feedback_strings)
    """
    score = 0
    feedback = []

    # 1) base marks contribution
    avg = mean(marks)
    base = WEIGHTS["base_marks"]
    score += int((avg / 100.0) * base)

    # 2) attendance
    if attendance_pct >= GOOD_ATTENDANCE:
        score += int(WEIGHTS["attendance"])
    else:
        feedback.append("Attendance below recommended level. Try to attend more classes.")

    # 3) assignments
    # Tweak: if assignments_total == 0, assume no assignments were given -> give full assignments bonus
    if assignments_total <= 0:
        assignment_ratio = 1.0
    else:
        assignment_ratio = assignments_done / assignments_total
        if assignment_ratio < 0:
            assignment_ratio = 0.0
        if assignment_ratio > 1:
            assignment_ratio = 1.0

    score += int(assignment_ratio * WEIGHTS["assignments"])
    if assignments_total > 0 and assignment_ratio < 1.0:
        feedback.append("Complete more assignments to improve your score.")

    # 4) improvement over previous term
    # Tweak: previous_avg is None only when user skipped input; otherwise parsed with safe_float
    if previous_avg is not None:
        # ensure previous_avg is clamped 0-100
        if previous_avg < 0:
            previous_avg = 0.0
        if previous_avg > 100:
            previous_avg = 100.0

        if avg > previous_avg:
            score += int(WEIGHTS["improvement"])
            feedback.append("Average has improved since previous term. Keep it up!")
        elif avg < previous_avg:
            feedback.append("Average dropped since previous term. Find weak topics and revise.")
        else:
            feedback.append("Average unchanged from previous term.")

    # 5) extracurricular
    ec = extracurricular_score
    if ec < 0:
        ec = 0
    if ec > 10:
        ec = 10
    score += int((ec / 10.0) * WEIGHTS["extracurricular"])

    # 6) consistency penalty (if variance is large)
    var = variance(marks)
    if var >= 200:
        score += int(WEIGHTS["consistency_penalty"])
        feedback.append("Marks vary a lot between subjects. Work on weaker subjects.")

    # 7) fail penalty for each subject under PASS_MARK
    fails = 0
    for m in marks:
        if m < PASS_MARK:
            fails += 1
    if fails > 0:
        score += int(fails * WEIGHTS["fail_penalty"])
        feedback.append(str(fails) + " subject(s) are below pass mark. Clear them soon.")

    # keep final score readable (avoid huge negative numbers)
    if score < -50:
        score = -50

    return score, feedback

# ---------- rating (very simple ranges) ----------
def rate(score):
    # compute maximum positive sum for reference (sum positive weights)
    max_pos = 0
    for k, v in WEIGHTS.items():
        if v > 0:
            max_pos += v

    if max_pos == 0:
        return "UNKNOWN"

    percent = (score / max_pos) * 100

    if score < 0 or percent < 30:
        return "CRITICAL - At risk"
    if percent < 50:
        return "NEEDS IMPROVEMENT"
    if percent < 70:
        return "AVERAGE"
    if percent < 90:
        return "GOOD"
    return "EXCELLENT"

# ---------- result printing ----------
def show_result(name, marks, score, feedback):
    avg = mean(marks)
    positive_total = 0
    for k, v in WEIGHTS.items():
        if v > 0:
            positive_total += v

    print("\n--- Student Performance Report ---")
    print("Name (masked):", mask_name(name))
    print("Subjects:", len(marks))
    print("Average marks: {:.2f} / 100".format(avg))
    print("Performance score: {} / {}".format(score, positive_total))
    print("Overall rating:", rate(score))
    if len(feedback) > 0:
        print("\nSuggestions:")
        for f in feedback:
            print(" -", f)
    else:
        print("\nNo suggestions. Good work!")

# ---------- main program (user I/O) ----------
def main():
    print("Simple Student Grade Predictor")
    name = input("Enter student name: ").strip()

    # get number of subjects
    try:
        n = int(input("How many subjects? ").strip())
    except:
        n = 0

    if n <= 0:
        print("You must enter at least one subject. Exiting.")
        return

    marks = []
    for i in range(1, n+1):
        s = input("Enter marks for subject {} (0-100): ".format(i)).strip()
        m = safe_float(s)
        # clamp to 0-100 and handle invalid input
        if m < 0 or m > 100:
            print("Invalid marks, setting to 0.")
            m = 0.0
        marks.append(m)

    # attendance
    try:
        att = float(input("Attendance percentage (0-100): ").strip())
    except:
        att = 0.0
    if att < 0:
        att = 0.0
    if att > 100:
        att = 100.0

    # assignments
    try:
        total_assign = int(input("Total assignments given (enter 0 if none): ").strip())
    except:
        total_assign = 0
    try:
        done_assign = int(input("Assignments completed: ").strip())
    except:
        done_assign = 0
    if total_assign < 0:
        total_assign = 0
    if done_assign < 0:
        done_assign = 0
    if done_assign > total_assign and total_assign > 0:
        done_assign = total_assign

    # extracurricular (0-10)
    try:
        ec = float(input("Extracurricular score (0-10, optional): ").strip())
    except:
        ec = 0.0
    if ec < 0:
        ec = 0.0
    if ec > 10:
        ec = 10.0

    # previous term average (optional)
    prev_raw = input("Previous term average (0-100, press enter to skip): ").strip()
    if prev_raw == "":
        prev = None
    else:
        prev = safe_float(prev_raw, None)

    # analyze
    score, feedback = analyze(marks, att, done_assign, total_assign, ec, prev)

    # show result
    show_result(name, marks, score, feedback)

# run the program
if __name__ == "__main__":
    main()
