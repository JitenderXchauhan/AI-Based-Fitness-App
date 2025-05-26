def detect(keypoints, state, reps, threshold=50):
    r_elbow = keypoints[7]
    r_shoulder = keypoints[5]
    r_hip = keypoints[11]

    if r_elbow[1] > r_shoulder[1] + threshold and state == "up":
        state = "down"
    elif r_elbow[1] < r_shoulder[1] - threshold and state == "down":
        state = "up"
        reps += 1

    return "Push-ups", reps, state
