
class driveOBJ():
    def __init__(self,car,fTime=0.1,lrTime=0.05,fSpeed=15,lrSpeed=35):
        self.car=car        
        self.F_Time=fTime
        self.LR_Time=lrTime
        self.F_Speed=fSpeed
        self.LR_Speed=lrSpeed
        
    def move(self,degree,speeds,colors):
        # Initialize a variable for the maximum speed value
        max=0
        speedClass=0
        colorClass=0
        # Loop through the list of speeds
        for i in range(len(speeds)):
            if speeds[i][1]>max:
                max=speeds[i]
                speedClass=speeds[i][0]


        max=0        
        for i in range(len(colors)):
            if colors[i][1]>max:
                max=colors[i]
                colorClass=colors[i][0]
        
        if colorClass=="red":
            car.stop()
        else:       
            # Check the speed class and set the car speed accordingly
            if speedClass=="s30":
                self.car.speed(20)
            elif speedClass=="s60":
                self.car.speed(40)
     
            if degree<0.2 and degree>-0.2:
                self.car.speed(self.F_Speed)
                self.car.forward(self.F_Time)
                print(f"speed:{self.F_Speed} time:{self.F_Time} deg:{degree} forward ")
                
            elif degree<=0.2: 
                self.car.speed(self.LR_Speed)
                self.car.left(self.LR_Time)
                print(f"speed:{self.LR_Speed} time:{self.LR_Time} deg:{degree} left    " )
                
            elif degree>=-0.2: 
                self.car.speed(self.LR_Speed)
                self.car.right(self.LR_Time)
                print(f"speed:{self.LR_Speed} time:{self.LR_Time} deg:{degree} right   ")
                
        