def detect(keypoints, state, reps, threshold=50):
    r_knee = keypoints[13]
    l_knee = keypoints[14]
    r_hip = keypoints[11]
    l_hip = keypoints[12]

    if r_knee[1] < r_hip[1] - threshold * 2:
        if l_knee[1] < l_hip[1] - threshold * 2 and state == "right":
            state = "left"
            reps += 1
        elif r_knee[1] < r_hip[1] - threshold * 2 and state == "left":
            state = "right"
    return "High Knees", reps, state
