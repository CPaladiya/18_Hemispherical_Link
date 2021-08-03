import cv2
def GetLiveCenter(BinaryImage):
    ''' Takes in BinaryImage of the feed, Finds contours within binary image, then finds biggest one of them all.
        That contour is most probably a green ball. Then we find live center of the green ball and return it.
    '''
    #getting the contours out of the binary image
    contours, hierarchy = cv2.findContours(BinaryImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours)!=0:
        #finding the biggest contours of all available
        max_contour = max(contours,key = cv2.contourArea)
        #if balle is too near of too far, we dont want to do anything so we have set min and max area allowed for biggest contour
        if(cv2.contourArea(max_contour)>= 5000 and cv2.contourArea(max_contour)<= 77000):
            #here we are getting very start (top left) points of contour and contour's width and height
            TLx,TLy,wContour,hContour = cv2.boundingRect(max_contour)
            ball_X = int(TLx+wContour/2)
            ball_Y = int(TLy+hContour/2)
            return ball_X,ball_Y
    return 0,0

def DrawAxis(Image):
    '''Takes in live masked image from a feed, and finds it center. Then it draws the center and axis of the image with respect of center of the image
    '''
    #drawing the center of the image
    w = Image.shape[1] # width of the image
    h = Image.shape[0]  #height of the image
    X = int(w/2) #using width to get x center
    Y = int(h/2) #using height to get y center
    cv2.circle(Image, (X,Y), 10, (0,0,255),-1)
    #Drawing X-axis within the image
    cv2.line(Image, (0,Y),(w,Y), (0,0,255),1)
    #Drawing Y-axis within the image
    cv2.line(Image, (X,0),(X,h), (0,0,255),1)
    
def PrintCentersOnImage(Image,ball_X,ball_Y):
    '''Takes in live image from the feed, mostly a masked image, live location of ball. It draws, center of ball, the offset lines from axis and prints
       numbers on screen for offset and live location of the ball
    '''
    if(ball_X!=0 and ball_X!=0):
        #creating the string to be shown on the screen
        wImage = Image.shape[1] #width of the image
        hImage = Image.shape[0] #height of the image
        X_offset = ball_X - int(wImage/2)
        Y_offset = ball_Y - int(hImage/2)
        OffsetLocation = "Offset X: "+str(X_offset)+ " Offset Y: "+ str(Y_offset) #offset from the center of the screen
        LiveLocation = "Live X: "+str(ball_X)+ " Live Y: "+ str(ball_Y) #live location of ball
    
        cv2.circle(Image, (ball_X,ball_Y), 10, (0,255,255),-1) #Drawing live center of the ball
        #adding the string to live feed masked image
        #image, string, leftBottom point of string,font type, font scale, color, thickness of line, line type
        cv2.putText(Image,LiveLocation, (10,hImage-10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (244,242,115), 2, cv2.LINE_AA)
        #printing the offset value, on how much are we offset from the desired image center
        cv2.putText(Image,OffsetLocation, (10,hImage-45), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (247,243,129), 2, cv2.LINE_AA)
    
        #drawing offset line from center of the ball to the relevant axis
        cv2.line(Image, (ball_X,ball_Y),(ball_X,int(hImage/2)), (0,255,255),1)
        cv2.line(Image, (ball_X,ball_Y),(int(wImage/2),ball_Y), (0,255,255),1)
            
