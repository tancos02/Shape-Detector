from Tkinter import *
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import cv2
import numpy as np

def rules1(lineCount,facts,rules) :
    result = False
    if(lineCount == 3) :
        result = True
        facts.append('segitiga')
        rules.append('rules1')
    return result

def rules2(lineCount,facts,rules) :
    result = False
    if(lineCount == 4) :
        result = True
        facts.append('segiempat')
        rules.append('rules2')
    return result

def rules3(lineCount,facts,rules) :
    result = False
    if(lineCount == 5) :
        result = True
        facts.append('segilima')
        rules.append('rules3')
    return result

def rules4(lineCount,facts,rules) :
    result = False
    if(lineCount == 6) :
        result = True
        facts.append('segienam')
        rules.append('rules4')
    return result

def filter(lines) :
    arr_point = []
    for line in lines[0] :
        x1, y1, x2, y2 = line
        if(len(arr_point) > 0) :
            for filtered_line in arr_point :
                is_line = True
                x3, y3, x4, y4 = filtered_line
                if((x1 < x3+21) and (x1 > x3-21)) and ((y1 < y3+21) and (y1 > y3-21)) :
                    if((x2 < x4+21) and (x2 > x4-21)) and ((y2 < y4+21) and (y2 > y4-21)) :
                        is_line = False
                        break
            if(is_line) :
                arr_point.append([x1, y1, x2, y2])
        else :
            arr_point.append([x1, y1, x2, y2])
    for i in range (0,len(arr_point)-1) :
        for j in range(i,len(arr_point)) :
            if((arr_point[i][0] < arr_point[j][2]+21) and (arr_point[i][0] > arr_point[j][2]-21)) :
                arr_point[j][2] = arr_point[i][0]
            if((arr_point[i][0] < arr_point[j][0]+21) and (arr_point[i][0] > arr_point[j][0]-21)) :
                arr_point[j][0] = arr_point[i][0]
            if((arr_point[i][2] < arr_point[j][2]+21) and (arr_point[i][2] > arr_point[j][2]-21)) :
                arr_point[j][2] = arr_point[i][2]
            if((arr_point[i][2] < arr_point[j][0]+21) and (arr_point[i][2] > arr_point[j][0]-21)) :
                arr_point[j][0] = arr_point[i][2]
            if((arr_point[i][1] < arr_point[j][3]+21) and (arr_point[i][1] > arr_point[j][3]-21)) :
                arr_point[j][3] = arr_point[i][1]
            if((arr_point[i][1] < arr_point[j][1]+21) and (arr_point[i][1] > arr_point[j][1]-21)) :
                arr_point[j][1] = arr_point[i][1]
            if((arr_point[i][3] < arr_point[j][3]+21) and (arr_point[i][3] > arr_point[j][3]-21)) :
                arr_point[j][3] = arr_point[i][3]
            if((arr_point[i][3] < arr_point[j][1]+21) and (arr_point[i][3] > arr_point[j][1]-21)) :
                arr_point[j][1] = arr_point[i][3]
    return(arr_point)
 
def select_image():
    global panelA, panelB, panelC

    path = tkFileDialog.askopenfilename()

    if len(path) > 0:
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 75, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250)
        
        image1 = Image.fromarray(image)
		
        for line in filter(lines):
            x1, y1, x2, y2 = line
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        image2 = Image.fromarray(image)

        image1 = ImageTk.PhotoImage(image1)
        image2 = ImageTk.PhotoImage(image2)

        if panelA is None or panelB is None:
            panelA = Label(image=image1)
            panelA.image = image1
            panelA.pack(side="left", padx=10, pady=10)

            panelB = Label(image=image2)
            panelB.image = image2
            panelB.pack(side="right", padx=10, pady=10)

            lines = filter(lines)
            lineCount = len(lines)
            facts = []
            rules = []
            facts.append(str(lineCount))
            print(lineCount)
            isSegitiga = rules1(lineCount,facts,rules)
            isSegiEmpat = rules2(lineCount,facts,rules)
            isSegiLima = rules3(lineCount,facts,rules)
            isSegiEnam = rules4(lineCount,facts,rules)
            panelC = Text(root)
            panelC.insert(INSERT, 'facts :')
            panelC.insert(INSERT, facts)
            panelC.insert(INSERT, '\n')
            panelC.insert(INSERT, 'rules :')
            panelC.insert(INSERT, rules)
            panelC.insert(INSERT, '\n')
            panelC.insert(INSERT, 'conclusion :')
            panelC.insert(INSERT, facts[-1] + '\n')
            panelC.pack(side="right", padx=10, pady=10)
 
        else:
            panelA.configure(image=image1)
            panelB.configure(image=image2)
            panelA.image = image1
            panelB.image = image2


root = Tk()
panelA = None
panelB = None
panelC = None

btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
 
root.mainloop()