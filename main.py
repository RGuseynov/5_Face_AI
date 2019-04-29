import cognitive_face as CF
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

KEY = '69defd2acc3f444cbd7c79a019a983bc'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = 'https://francecentral.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
img_url = 'Screenshot from 2019-04-29 14-46-40.png'
faces = CF.face.detect(img_url)
print(faces)

x = faces[0]['faceRectangle']['left']
y = faces[0]['faceRectangle']['top']
width = faces[0]['faceRectangle']['width']
height = faces[0]['faceRectangle']['height']

ax = plt.gca()
rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

img=mpimg.imread('Screenshot from 2019-04-29 14-46-40.png')
imgplot = plt.imshow(img)
plt.show()