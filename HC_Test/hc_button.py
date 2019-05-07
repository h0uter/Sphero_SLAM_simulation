def start():
    global pose, control, constraints, loop, radius, wall_width, world_size, flag, lw
    scale = 520
    loop = not(loop)
    t = 0
    pmeasurement = []
    while loop:# and i <=300:
        posep = pose 
        pose = fs.predict(pose,control)
        past_orient = pose[0][2]
        pose = s.check_collision(constraints, pose[0], posep, flag)# flag = wall_correction; measurement to be included as prior
        f=s.draw(pose[0])
        if pose[1] != -1:
            measurement = array([pose[0][0],pose[0][1],tan(pose[1]-past_orient)])
            w, wall, lw = fs.correct(measurement,pmeasurement)
            for i in range(len(wall)):
                if i==2 or i==4:
                    wall[i] = list(reversed(wall[i]))
            robot_map(wall,t)
            root.update()
            pmeasurement = measurement
        pose = pose[0]
#         i = i + 1

def stop():
    global loop, lw
    loop = not(loop)
    print "Tree",lw

def boost():
    global control
    control[0] = control[0] + 50
    if control[0] <= 0:
        control[0] =0

def slow():
    global control
    control[0] = control[0] - 50
    if control[0] <= 0:
        control[0] =0