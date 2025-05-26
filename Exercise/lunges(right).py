def detect(keypoints, state, reps, threshold=50):
    r_knee = keypoints[13]
    l_knee = keypoints[14]
    r_hip = keypoints[11]

    if r_knee[1] > l_knee[1] + threshold and r_knee[0] > r_hip[0]:
        if r_knee[1] > r_hip[1] + threshold and state == "up":
            state = "down"
        elif r_knee[1] < r_hip[1] - threshold and state == "down":
            state = "up"
            reps += 1
    return "Lunges (Right)", reps, state