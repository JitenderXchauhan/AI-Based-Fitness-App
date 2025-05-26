import numpy as np

def calculate_angle(p1, p2, p3):
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle

def detect(keypoints, state, reps, threshold=50):
    r_shoulder = keypoints[5]
    r_elbow = keypoints[7]
    r_hip = keypoints[11]

    angle = calculate_angle(r_shoulder, r_elbow, r_hip)

    if angle < 90:
        if angle > 150 and state == "down":
            state = "up"
            reps += 1
        elif angle < 90 and state == "up":
            state = "down"
    return "Bicep Curls", reps, state