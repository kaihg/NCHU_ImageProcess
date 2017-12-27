
# coding: utf-8

# In[37]:


from PIL import Image, ImageFilter,ImageDraw
import math
import numpy


# In[27]:


source = Image.open("source.jpg")


# In[28]:


edgeImage = source.filter(ImageFilter.FIND_EDGES)
edgeImage.save('edgeImg.jpg') 


# In[31]:


def createPointImg(img,threshold=128,fileName="binaryImg.jpg"):
    # 來源圖片是用預設方法取得的線，在圖片邊緣也會產生線，不希望如此所以特別減少 1 + 1 px
    output = Image.new("L",(img.width-2,img.height-2))
    outputPixels = output.load()
    pixels = img.load()
    
    for j in range(img.height-2):
        for i in range(img.width-2):
            if pixels[i+1,j+1] < threshold:
                outputPixels[i,j] = 0
            else :
                outputPixels[i,j] = 255
    output.save(fileName)
    return output


# In[32]:


binaryImg = createPointImg(edgeImage)


# In[6]:


def houghTransform(x,y,angle):
    return x*math.cos(angle) + y*math.sin(angle)


# In[7]:


def computerImageHough(img):
    sliceNum = 1000
    #output = Image.new("L",(img.width,img.height))
    #outputPixels = output.load()
    pixels = img.load()
    outputPixels = []
    
    minP = 0
    maxP = 0
    
    for j in range(img.height):
        outputPixels.append([])
        for i in range(img.width):
            if pixels[i,j] != 0:
                lineP = []
                # 算 (i,j) pixel 在所有 angle 上的 p，並記錄下來
                for angleCount in range(sliceNum):
                    angle = (2 * angleCount / sliceNum - 1) * math.pi 
                    p = houghTransform(i,j,angle)
                    #print(p)
                    lineP.append(p)
                    # 記錄上下限，以便後面產生圖片
                    if p < minP:
                        minP = p
                    if p > maxP:
                        maxP = p
                outputPixels[j].append(lineP)
            else :
                outputPixels[j].append([])
    
    
    return (outputPixels,minP,maxP)


# In[33]:


result = computerImageHough(binaryImg)


# In[9]:


print(result[1],result[2])


# In[10]:


def createHoughImg(data,minP,maxP,sliceNum = 1000):
    height = round(maxP - minP)
    
    transData = numpy.zeros(shape=(height,sliceNum))
    maxCount = 0 
    maxPosition = None
    #print(transData[0][0])
    
    # find 最多交點數量
    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            line = row[j]
            for k in range(len(line)):
                p = int(line[k] - minP)
                #print(p,k)
                #print(transData[p][k])
                transData[p][k] += 1
                if (transData[p][k] > maxCount):
                    maxCount = transData[p][k]
                    maxPosition = (p,k)
    #print(maxCount,maxPosition)
    
    output = Image.new("L",(height,sliceNum))
    outputPixels = output.load()
    
    for p in range(height):
        for s in range(sliceNum):
            outputPixels[p,s] = int(transData[p][s] * 255 / maxCount)
    
    output.save("Hough.jpg")
    return maxPosition,maxCount


# In[34]:


result2 = createHoughImg(result[0],result[1],result[2])


# In[12]:


print(result2)


# In[46]:


def findAllLine(data, passPoint, minP):
    angle = passPoint[1]
    p = passPoint[0]
    
    points = []
    
    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            line = row[j]
            if (len(line) > angle) and int(line[angle] - minP) == p:
                points.append((j,i))
    return points


# In[47]:


#print(len(result),len(result[0]),len(result[0][0]),len(result[0][0][0]))
points = findAllLine(result[0],result2[0],result[1])


# In[48]:


def drawLine(img, points):
    img2 = img.crop((0,0,img.width,img.height))
    #img2 = Image.new("L",(img.width,img.height))
    draw = ImageDraw.Draw(img2)
    
    draw.line(points,fill = 255,width = 3)
    img2.save("result.jpg")


# In[50]:


drawLine(edgeImage,points)

