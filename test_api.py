from agent import analyze_project


project = """
Our project is an AI-based attendance system.

The system uses face recognition to automatically
mark student attendance.

We plan to use Python, OpenCV and machine learning.

The system will store attendance records
and allow teachers to view attendance.

The project aims to reduce manual attendance work
and save time for teachers.
"""


print("🤖 ProjectLens is analyzing the project...")

result = analyze_project(project)


print("\n========== PROJECTLENS RESULT ==========\n")

print("Project Name:")
print(result.get("project_name"))

print("\nSummary:")
print(result.get("summary"))

print("\nProject Health:")
print(result.get("project_health"), "/ 100")

print("\nScores:")
print(result.get("scores"))

print("\nStrengths:")
for item in result.get("strengths", []):
    print("-", item)

print("\nCritical Issues:")
for item in result.get("critical_issues", []):
    print("-", item)

print("\nMissing Components:")
for item in result.get("missing_components", []):
    print("-", item)

print("\nRecommended Features:")
for item in result.get("recommended_features", []):
    print("-", item)

print("\nFinal Summary:")
print(result.get("final_summary"))