import requests
import json
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches


with open("KeyAPI.json", 'r') as file:
    cleAPI = json.load(file)['key']

with open("personne_id_in_group.json", "r") as file:
    group_data = json.load(file)['data']
print(group_data)


def face_detect(url_image, key):
    face_api_url = 'https://francecentral.api.cognitive.microsoft.com/face/v1.0/detect'
    params = {'returnFaceId': 'true',
              'returnFaceLandmarks': 'false',
              'returnFaceAttributes': 'emotion',
              'recognitionModel': 'recognition_02'}
    headers = {'Ocp-Apim-Subscription-Key': key,
               'Content-type': 'application/octet-stream'}
    with open(url_image, "rb") as file:
        image_data = file.read()
    with requests.post(face_api_url, params=params, headers=headers, data=image_data) as requete:
        faces = requete.json()
    return faces


def face_identify(id_group, id_personnes, key):  # id_personnes est une list
    url = 'https://francecentral.api.cognitive.microsoft.com/face/v1.0/identify'
    headers = {'Ocp-Apim-Subscription-Key': key,
               'Content-type': 'application/json'}
    data = {"PersonGroupId": id_group,
            "faceIds": id_personnes,
            "maxNumOfCandidatesReturned": 1,
            "confidenceThreshold": 0.5}
    with requests.post(url, headers=headers, data=str(data)) as requete:
        reponse = requete.json()
    return reponse


def ajouter_personne_dans_groupe(id_group, nom_personne, key):
    url = 'https://francecentral.api.cognitive.microsoft.com/face/v1.0/persongroups/' + id_group + '/persons'
    headers = {'Ocp-Apim-Subscription-Key': key,
               'Content-type': 'application/json'}
    data = {"name": nom_personne}
    with requests.post(url, headers=headers, data=str(data)) as requete:
        reponse = requete.json()
    return reponse  # personId


def ajouter_image_personne_groupe(id_group, id_personne, key, url_image):
    url = 'https://francecentral.api.cognitive.microsoft.com/face/v1.0/persongroups/' + id_group +'/persons/' + id_personne +'/persistedFaces'
    headers = {'Ocp-Apim-Subscription-Key': key,
               'Content-type': 'application/octet-stream'}
    with open(url_image, 'rb') as file:
        image_data = file.read()
    with requests.post(url, headers=headers, data=image_data) as requete:
        pass


def find_name(id_personne, data_group):
    for personne in data_group:
        if personne['personId'] == id_personne:
            return personne['name']


def found_emotion(face):
    list_key = list(face['faceAttributes']['emotion'].keys())
    list_value = list(face['faceAttributes']['emotion'].values())
    return [list_key[list_value.index(max(list_value))], round(max(list_value), 2)]


def grab_frame(capture):
    ret, frame = capture.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def draw_rectangles(axe, faces_list, identity_list, data_group):
    for face in faces_list:
        em = found_emotion(face)
        emotion = em[0]
        valeur_emotion = em[1]
        x = face['faceRectangle']['left']
        y = face['faceRectangle']['top']
        width = face['faceRectangle']['width']
        height = face['faceRectangle']['height']
        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
        axe.add_patch(rect)

        for identity in identity_list:
            if face['faceId'] == identity['faceId'] and identity['candidates'] != []:
                confidence = round(identity['candidates'][0]['confidence'], 2)
                name = find_name(identity['candidates'][0]['personId'], data_group)

                plt.text(x + width, y + 20, name, fontsize=16)
                plt.text(x + width, y + 40, "confidence: " + str(confidence), fontsize=16)
                plt.text(x + width, y + 60, emotion + " :" + str(valeur_emotion), fontsize=16)


# Initiate the camera
cap = cv2.VideoCapture(0)

# create subplot
# ax = plt.subplot()

# create image plot
# im = ax.imshow(grab_frame(cap))

plt.ion()
loop = True
while loop:
    # im.set_data(grab_frame(cap))
    plt.clf()
    ret, frame = cap.read()
    cv2.imwrite("frame.png", frame)

    faces = face_detect("frame.png", cleAPI)  # requete API 1
    print(faces)
    facesId = []
    for face in faces:
        facesId.append(face['faceId'])

    ids_identity = face_identify("id69000", facesId, cleAPI)  # requete API 2
    print(ids_identity)


    ax = plt.gca()
    draw_rectangles(ax, faces, ids_identity, group_data)

    img = mpimg.imread('frame.png')
    imgplot = plt.imshow(img)
    plt.pause(0.1)

plt.ioff()  # due to infinite loop, this gets never called.
plt.show()





