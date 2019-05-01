# création groupe de personnes
person_group_url = 'https://francecentral.api.cognitive.microsoft.com/face/v1.0/persongroups/id69000'
headers2 = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-type': 'application/json'}
data2 = {
    "name": "PROMO_AI",
    "userData": "16 SimplonAI Students",
    "recognitionModel": "recognition_02"}
with requests.put(person_group_url, headers=headers2, data=str(data2)) as requete2:
    pass


# ajout de tout le monde dans le groupe
for file in os.listdir('photos promo'):
    reponse = ajouter_personne_dans_groupe("id69000", file[:-4], cleAPI)
    idPersonne = reponse['personId']
    print(idPersonne)
    url_photo = "photos promo/" + file
    ajouter_image_personne_groupe("id69000", idPersonne, cleAPI, url_photo)
    time.sleep(10)


# affichage matplotlib
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