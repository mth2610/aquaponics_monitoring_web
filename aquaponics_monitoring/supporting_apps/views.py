from django.shortcuts import render
from django.core.files.base import ContentFile
from django.template import loader
from django.http import HttpResponse
import base64
# Create your views here.

def count_circles(request):
    import cv2
    import numpy as np
    from PIL import Image


    min_radius = int(request.POST['minRadius'])
    max_radius = int(request.POST['maxRadius'])
    user_image = request.FILES['userImage']
    template = loader.get_template('supporting_apps/count_circles.html')
    user_image = Image.open(user_image)
    print len(np.array(user_image))
    # Store image in a string buffer
    # buffer = StringIO.StringIO()
    # canvas = pylab.get_current_fig_manager().canvas
    # canvas.draw()
    # pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    # pilImage.save(buffer, "PNG")
    # pylab.close()
    # img = str((buffer.getvalue()).encode('Base64'))
    context = {}

    #img = cv2.imread(np.array(user_image) ,0)
    img = cv2.cvtColor(np.array(user_image), cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    print cimg
    circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,minDist=min_radius,
                                param1=50,param2=30,minRadius=min_radius,maxRadius=max_radius)
    circles = np.uint16(np.around(circles))
    number_of_pipes = len(circles[0])
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    # cv2.imwrite("output.png", cimg)
    #cv2.imshow('detected circles',cimg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cimg = cv2.imencode(".jpg", cimg)[1]
    context = {"image": base64.encodestring(cimg)}
    context.update({"number_of_pipes":number_of_pipes})
    return HttpResponse(template.render(context, request))
