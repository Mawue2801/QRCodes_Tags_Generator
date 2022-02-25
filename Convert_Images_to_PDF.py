from PIL import Image
imageList = []
for i in range(1,2):
    objectname = f'img{i}'
    objectname = Image.open(f'Batch_{i}.jpg')
    objectname = objectname.convert('RGB')
    imageList.append(objectname)

imageList.pop(0)

objectname.save('NewPDF.pdf',save_all=True, append_images=imageList)

# im1 = Image.open('Front.jpg')
# im1 = im1.convert('RGB')

# im1.save('Front.pdf')