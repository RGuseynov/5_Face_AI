import requests
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches


subscription_key = '69defd2acc3f444cbd7c79a019a983bc'
assert subscription_key

face_api_url = 'https://francecentral.api.cognitive.microsoft.com/face/v1.0/detect'

params = {'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,smile,emotion'}

headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-type': 'application/octet-stream'}

with open('photos promo/Emanuel.png', "rb") as file:
    image_data = file.read()

with requests.post(face_api_url, params=params, headers=headers, data=image_data) as requete:
    faces = requete.json()

print(faces)

x = faces[0]['faceRectangle']['left']
y = faces[0]['faceRectangle']['top']
width = faces[0]['faceRectangle']['width']
height = faces[0]['faceRectangle']['height']

ax = plt.gca()
rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

img=mpimg.imread('photos promo/Emanuel.png')
imgplot = plt.imshow(img)
plt.show()