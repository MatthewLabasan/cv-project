import easyocr
import PIL

reader = easyocr.Reader(['en'])

bound = reader.readtext("test_images/GUIcircles.png")
for tup in bound:
    print(tup[1])


bound = reader.readtext("test_images/GUI.png")
for tup in bound:
    print(tup[1])

