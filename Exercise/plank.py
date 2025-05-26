def detect(keypoints, state, reps, threshold=50):
    r_shoulder = keypoints[5]
    r_elbow = keypoints[7]
    r_hip = keypoints[11]

    if abs(r_shoulder[1] - r_hip[1]) < threshold and abs(r_elbow[1] - r_shoulder[1]) < threshold:
        return "Plank", reps, state  # static
    return "Plank", reps, state