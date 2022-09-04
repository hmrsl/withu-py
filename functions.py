import os
import pathlib

import cv2

# from deepface import DeepFace
# from pkg.Face_Recognition import face_recognize
# from pkg.Badword import badword


def count_faces(root, post=17):
    path = os.path.join(root, "post", f"{post}.png")
    face_cascade = cv2.CascadeClassifier(os.path.join(root, 'cv', 'haarcascade_frontalface_alt.xml'))

    image = cv2.imread(path)
    im = cv2.imread(path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    face_index = 1

    path = os.path.join(root, "post", "face", f"{post}")
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    for (x, y, w, h) in faces:
        img_path = os.path.join(path, f"{face_index}.png")

        cv2.rectangle(image, (x, y), (x + w, y + h),
                      (0, 0, 255), 2)

        face = im[y:y + h, x:x + w]
        cv2.imwrite(img_path, face)
        face_index += 1

    path = f"{path}\\{0}.png"
    cv2.imwrite(path, image)

    return len(faces)


def gen_icons(path, result):
    p = path

    # read the image
    originalmage = cv2.imread(p)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    # print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        return

    ReSized1 = cv2.resize(originalmage, (960, 540))

    # converting an image to grayscale
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    # plt.imshow(ReSized2, cmap='gray')

    # applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    # plt.imshow(ReSized3, cmap='gray')

    # retrieving the edges for cartoon effect
    # by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))
    # plt.imshow(ReSized4, cmap='gray')

    # applying bilateral filter to remove noise
    # and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    # plt.imshow(ReSized5, cmap='gray')

    # masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    cv2.imwrite(os.path.join(result, "1.png"), cv2.cvtColor(cartoonImage, cv2.COLOR_RGB2BGR))
    cv2.imwrite(os.path.join(result, "2.png"), cv2.cvtColor(grayScaleImage, cv2.COLOR_RGB2BGR))
    cv2.imwrite(os.path.join(result, "3.png"), cv2.cvtColor(smoothGrayScale, cv2.COLOR_RGB2BGR))
    cv2.imwrite(os.path.join(result, "4.png"), cv2.cvtColor(colorImage, cv2.COLOR_RGB2BGR))


def has_bad_words(text, path):
    # return percentage of bad words || 0 for no bad words
    # TODO Uncomment
    # return badword.main(text, path)
    return 0


def is_admin(user_id, img_path):
    print(img_path)
    # face detected -> true
    # TODO Uncomment
    # return face_recognize.face_recognize(img_path, user_id)
    return True


def train_admin(img_path):
    #     Train ML using image path
    p = img_path
    imagename = img_path.split('\\')[-1]
    print(imagename)
    imagepath = "E:\\Programming\\VPS\\08 Annonymus chat\\Python\\WithU\shan\\Face_Recognition\\Face_Images\\"

    # read the image
    originalmage = cv2.imread(p)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

    # print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        return

    cv2.imwrite(imagepath + imagename, originalmage)

    pass


def detect_emotion(path):

    # TODO UnComment
    return "Sad"
    # try:
    #     analyze = DeepFace.analyze(img_path=path,
    #                                actions=('emotion',), prog_bar=False,
    #                                detector_backend='opencv', enforce_detection=False)
    #     return analyze['dominant_emotion']
    # except:
    #     return "ERROR"

