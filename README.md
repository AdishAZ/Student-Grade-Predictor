### Student-Grade-Predictor  ###
This tool analyzes a student's performance using marks, attendance, assignments, improvement, and extracurricular activity. Instead of only checking raw marks, it uses scoring logic similar to AI evaluation to generate a performance score and clear, easy-to-understand feedback.

 PROJECT OVERVIEW 

Traditional report cards only show final marks, which don’t reflect real performance factors like consistency, attendance, or improvement. Our analyzer works smarter by checking multiple parameters like assignment completion, attendance percentage, fail subjects, variance between marks, and improvement from the previous term.

This approach is inspired by AI-style evaluation, which looks beyond a single number and instead analyzes patterns. The analyzer then produces a performance score, and finally converts it into a rating, helping students understand where they truly stand.

FEATURES AND LOGICS

The analyzer assigns a score out of a total of 90 points (positive scoring), and deducts penalties where needed.

Scoring Criteria:

Base Marks (60 points)
The student’s average marks are converted into a scaled contribution to the total score.

Attendance Bonus (10 points)
Awarded when attendance is equal to or above the recommended percentage (75%).

Assignments Bonus (8 points)
Full bonus if all assignments are completed.
Partial bonus if some are done.
If no assignments were given, full bonus is awarded.

Improvement Bonus (7 points)
Awarded if the student performed better compared to the previous term.

Extracurricular Bonus (5 points)
Based on a score from 0–10.

Penalties:

Consistency Penalty (-10 points)
Applied if the marks vary too much across subjects (large variance).

Failing Subject Penalty (-15 per subject)
Applied for every subject below the passing mark (40).

RATING SYSTEMS

After calculating the performance score, the program converts it into a clear rating:

90%+ → EXCELLENT

70% – 89% → GOOD

50% – 69% → AVERAGE

30% – 49% → NEEDS IMPROVEMENT

Below 30% → CRITICAL – At Risk

This helps students quickly understand their current performance level.

TECHNOLOGIES / TOOLS USED

Core Language: Python 3.x

Standard Library Only
No external modules required.

CLI-based User Interaction
Simple text input and output.

STEPS TO RUN THE CODE

The project uses only basic Python, so nothing needs to be installed.

1. Save the Code

Save the full script as:

`student_grade_analyzer.py`

2. Run the Script

Open the terminal or command prompt and run:
```
python student_grade_analyzer.py
```
3. Enter Student Details

You will be prompted to enter:
```
Student name

Number of subjects

Marks for each subject

Attendance percentage

Assignment details

Extracurricular score

Previous term average (optional)
```
EXAMPLE OUTPUT

Sample output for an average student:
```
 Student Performance Report 
Name (masked): P****
Subjects: 4
Average marks: 62.00 / 100
Performance score: 45 / 90
Overall rating: AVERAGE

Suggestions:
 - Attendance below recommended level. Try to attend more classes.
 - Complete more assignments to improve your score.
 - Average dropped since previous term. Find weak topics and revise.
```

PROJECT STRUCTURE

`analyze(...)`
Core logic. Calculates performance score based on marks, attendance, assignments, improvement, extracurricular score, and penalties.

`mean(), variance()`
Basic helper functions to compute average and consistency.

`rate(score)`
Converts numeric score into a readable rating.

`show_result(...)`
Displays the final report, including score, rating, and suggestions.

`main()`
Handles user input and coordinates the workflow.
