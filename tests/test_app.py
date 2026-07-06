from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)

INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    "Basketball Team": {
        "description": "Train for interschool basketball games and build team skills",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "jamie@mergington.edu"],
    },
    "Swimming Club": {
        "description": "Develop swimming techniques, endurance, and safety in the pool",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["sydney@mergington.edu", "mason@mergington.edu"],
    },
    "Art Club": {
        "description": "Explore painting, drawing, and mixed-media art projects",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["zara@mergington.edu", "noah@mergington.edu"],
    },
    "Drama Club": {
        "description": "Practice acting, stagecraft, and prepare school theater productions",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["maria@mergington.edu", "henry@mergington.edu"],
    },
    "Science Olympiad": {
        "description": "Compete in STEM challenges and build problem-solving skills",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["lucas@mergington.edu", "sophie@mergington.edu"],
    },
    "Debate Team": {
        "description": "Prepare for debate tournaments and strengthen research and speaking skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["ethan@mergington.edu", "alexa@mergington.edu"],
    },
}


def setup_function():
    activities.clear()
    for activity_name, activity_data in INITIAL_ACTIVITIES.items():
        activities[activity_name] = {
            "description": activity_data["description"],
            "schedule": activity_data["schedule"],
            "max_participants": activity_data["max_participants"],
            "participants": list(activity_data["participants"]),
        }


def test_root_redirects_to_static_index_html():
    # Arrange
    setup_function()

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities():
    # Arrange
    setup_function()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12
    assert payload["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_adds_participant():
    # Arrange
    setup_function()
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess%20Club/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for Chess Club"}
    assert new_email in activities["Chess Club"]["participants"]


def test_signup_for_missing_activity_returns_404():
    # Arrange
    setup_function()
    missing_activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{missing_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_unsubscribes_student():
    # Arrange
    setup_function()
    student_email = "daniel@mergington.edu"

    # Act
    response = client.delete("/activities/Chess%20Club/participants", params={"email": student_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {student_email} from Chess Club"}
    assert student_email not in activities["Chess Club"]["participants"]
