def detect(keypoints, state, reps, threshold=50):
    r_knee = keypoints[13]
    l_knee = keypoints[14]
    l_hip = keypoints[12]

    if l_knee[1] > r_knee[1] + threshold and l_knee[0] > l_hip[0]:
        if l_knee[1] > l_hip[1] + threshold and state == "up":
            state = "down"
        elif l_knee[1] < l_hip[1] - threshold and state == "down":
            state = "up"
            reps += 1
    return "Lunges (Left)", reps, state