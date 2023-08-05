# Indo OCR Army

This is a package for OCR Identity card in Indonesia. This packages build on top of detectron2 so you should install detectron2 first and some requirements need to install separately before you run this packages, for quick tutorial run this:

```
conda install 
```

for comprehensive use, you can do this:
```
import os
import cv2
import matplotlib.pyplot as plt

from IndoOCRArmy.modelOCR import defaultConfig, DrawOCR, numericalDetectron2, boundingBoxesDetectron2, alphabeticalDetectron2, easypredict

# load classes
cfg = defaultConfig()

for key in cfg.keys():
    if 'list_cuda' in cfg[key]:
        cfg[key]['list_cuda'] = [0]
        
drawer_ocr = DrawOCR(cfg['drawOCR'])
bBoxDet = boundingBoxesDetectron2(cfg['boundingBoxesDetectron2'])
numDet = numericalDetectron2(cfg['numericalDetectron2'])
alphaDet = alphabeticalDetectron2(cfg['alphabeticalDetectron2'])

# load image
image_ktp = cv2.imread("assets/ktp_example.jpg")
image_sim = cv2.imread("assets/sim_example.jpg")

# detect boundingboxes
crops, boxes, labels = bBoxDet.predict(image_ktp, input_type='ktp')

# detect number and alphabet
dict_ID = numDet.predict_ensemble(crops[0])
dict_Name = alphaDet.predict_ensemble(crops[1])

# choose `weighted_hardvote_word` for the best result according to our benchmark
ID =  dict_ID.get("weighted_hardvote_word")
Name =  dict_Name.get("weighted_hardvote_word")

# parse NIK to get information about : location, gender, and birthdate
parse_NIK = numDet.parse_nik(ID)

# create listdata and listlabel for visualization later
listdata = [ID, Name]
listlabel = [x for x in list(labels.values()) if x is not None]
for label, data in parse_NIK.items():
    listdata.append(data)
    listlabel.append(label)
    
print(ID)
print(Name)

drawer_ocr.show_list_images(list_img=crops.values())
```

For visuzlize comprehensive result, use this:

```
drawer_ocr.show_desc(image_ktp, boxes, labels, listdata, listlabel)
```

For quick result, use this:
```
image_ktp = cv2.imread("assets/ktp_example.jpg")
easypredict(image_ktp, bBoxDet, numDet, alphaDet, input_type='ktp')
```
