# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Ben Santana                                                  #
# 	Created:      4/17/2025, 4:46:03 PM                                        #
# 	Description:  Final Demo                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# ================= Constants ================= #

LINE_FOLLOW_SPEED = 100 # Speed of motors for when it is following a line
LINE_K_P = 200 # K_P for when line tracking
ON_LINE_VAL = 10 # Reflectivity detected from line trackers when they are fully on the line
TURN_SPEED = 100 # Speed of motors when turning
TURN_MARGIN = 5 # Margin to check if reached target angle when turning

# ================= Hardware ================= #

brain=Brain()
left_motor = Motor(Ports.PORT10, 18_1, True)
right_motor = Motor(Ports.PORT1, 18_1, False)
inertial_sensor = Inertial(Ports.PORT5)
left_line_tracker = Line(brain.three_wire_port.a)
right_line_tracker = Line(brain.three_wire_port.b)
camera = AiVision(Ports.PORT3)
camera.tag_detection(True)

# ================= Basic Movement ================= #

def stopMotors():
    left_motor.stop()
    right_motor.stop()

def drive(speed, direction):

    # Drive the robot with specified speed and direction.
    # Negative direction turns right, positive turns left.
    left_motor.set_velocity(speed - direction, RPM)
    right_motor.set_velocity(speed + direction, RPM)
    left_motor.spin(FORWARD)
    right_motor.spin(FORWARD)

def shake(times: int, secPhase: float, switchPerSec: float, speed: int):
    perSec = switchPerSec
    half_period_ms = int(1000.0 / (2 * perSec))

    # Set motor speeds
    left_motor.set_velocity(speed, RPM)
    right_motor.set_velocity(speed, RPM)

    def shake(mode: str):
        for _ in range(int(secPhase * perSec)):
            if mode == "back":
                left_motor.spin(FORWARD)
                right_motor.spin(FORWARD)
            elif mode == "turn":
                left_motor.spin(FORWARD)
                right_motor.spin(REVERSE)
            wait(half_period_ms)

            # Switch directions
            if mode == "back":
                left_motor.spin(REVERSE)
                right_motor.spin(REVERSE)
            elif mode == "turn":
                left_motor.spin(REVERSE)
                right_motor.spin(FORWARD)
            wait(half_period_ms)

    for n in range(times):
        if n % 2 == 0:
            print("TurnShake:")
            shake("turn")
        else:
            print("BackAndForth:")
            shake("back")
    
    stopMotors()

def followLine(until):
    '''
    Follows line until some condition
    @params : until - function that returns whether to stop
    '''
    direction = 0

    brain.screen.clear_screen()

    while True:
        error = math.atan(left_line_tracker.reflectivity()) - math.atan(right_line_tracker.reflectivity())

        # break if hit perpendicular line
        if(until()):
            print("break")
            break
        
        direction = error * LINE_K_P
        
        drive(LINE_FOLLOW_SPEED, direction)

#REVIEW
def turn(target_angle: int, direction: TurnType.TurnType):
    '''
    @params: 
        target_angle - angle in degrees to turn
        direction - LEFT || RIGHT
    '''

    # Set direction value
    direct = 1
    if direction == LEFT:
        direct = -1
    
    # Start turning
    left_motor.set_velocity(TURN_SPEED * direct, RPM)
    right_motor.set_velocity(TURN_SPEED * direct, RPM)
    left_motor.spin(FORWARD)
    right_motor.spin(REVERSE)
    withinMargin = False
    
    # Keep turning until we reach the target angle
    while not withinMargin:  # 5 degrees accounts for recurring overshoot
        if abs(inertial_sensor.heading() - target_angle) < TURN_MARGIN:
            withinMargin = True

        if abs(inertial_sensor.heading() - (target_angle + 360)) < TURN_MARGIN:
            withinMargin = True

        if abs(inertial_sensor.heading() - (target_angle - 360)) < TURN_MARGIN:
            withinMargin = True
        
        brain.screen.print_at("Current Angle: ", inertial_sensor.heading(),x=40, y=40)

        print("Current Angle" + str(inertial_sensor.heading()))
    
    # Stop the motors
    left_motor.stop()
    right_motor.stop()

# ================= Detection ================= #

def seesTag():
    # returns whether the camera sees an april tag
    objs = camera.take_snapshot(Tagdesc(0xFFFF))
    print(camera.largest_object())
    return False

#TODO:
def findFruit(color):
    '''
    @params: color (String) - "yellow", "orange", "green"
    '''
    # Rotate till fruit on ground* & in view
    pass


# ================= Routine Movement Sets ================= #

def goUpRamp():
    # define stop condition for line follow
    def until():
        return left_line_tracker.reflectivity() < ON_LINE_VAL and left_line_tracker.reflectivity() < ON_LINE_VAL

    # follow line
    followLine(until)

#TODO: REVIEW:
def approachAprilTag(id, dist):
    '''
    @params: 
        - id (int): apr tag id
        - dist (int): width in pixels april tag should reach on screen
    '''
    pass

# ================= Task Completion ================= #

#TODO:
def dropFruit():
    pass

#TODO:
def pickUpThreeFruit(color):
    '''
    @params : color (String) - "yellow", "green", "orange"
    '''
    findFruit(color)

    #TODO:
    def centerClosestFruit():
        # Rotate till biggest fruit on the ground* in center view
        pass

    #TODO:
    def pickUpSingleFruit():
        # Roll over fruit to pick it up
        pass

    pass

#TODO:
def returnFromFruitPicking(color):
    '''
    @params: color (String) : "yellow", "orange", "green"
    '''
    def returnFromGreen():
        pass
    def returnFromYellow():
        pass
    def returnFromOrange():
        pass
    pass

#TODO:
def shakeTree(id):
    '''
    Finds, shakes and then moves away from tree
    '''
    # Rotate till tree in view
    # Centers tree
    # Approaches
    # shake()
    # Retreats
    pass

# ================= Main ================= #

#TODO:
def main():
    def acquireFruit(color, tree_id):
        shakeTree(tree_id)
        pickUpThreeFruit(color)
        returnFromFruitPicking(color)

    inertial_sensor.set_heading(270)

    goUpRamp()

    # ---------- YELLOW ---------- #
    turn(45, LEFT) #DEFINE: angle
    acquireFruit("yellow", 1)
    approachAprilTag(21, 999) #DEFINE: width in pixels april tag should reach
    dropFruit()

    # ---------- ORANGE ---------- #
    approachAprilTag(21, 999) #DEFINE: width in pixels april tag should reach
    turn(45, RIGHT)
    acquireFruit("orange", 2)
    approachAprilTag(31, 999) #DEFINE: width in pixels april tag should reach
    dropFruit()

    # ---------- GREEN ---------- #
    approachAprilTag(31, 999) #DEFINE: width in pixels april tag should reach
    turn(90, RIGHT)
    approachAprilTag(8, 999) #DEFINE: width in pixels april tag should reach
    acquireFruit("green", 3)
    approachAprilTag(8, 999) #DEFINE: width in pixels april tag should reach
    dropFruit()

    # ?! SUCCESS ?! #


main()