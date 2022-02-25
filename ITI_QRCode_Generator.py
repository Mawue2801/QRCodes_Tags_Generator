import qrcode
import pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

df = pd.read_excel('Participants.xlsx')

tagNumberFont = ImageFont.truetype('Anton-Regular.ttf', 80)
image_x = [390,1513,390,1513]
image_y = [560,560,2165,2165]
text_x = [900,2022,900,2022]
text_y = [760,760,2365,2365]
tag_center_x = [679, 1801, 679, 1801]
name_y = [1105, 1105, 2705, 2705]
institution_y = [1210, 1210, 2810, 2810]
name_max_width = 750
institution_max_width = 645

num = 1
tag_num = 12
for i in range(tag_num//4):
    # template = Image.open("new1.jpg")
    template = Image.open("Blank.jpg")
    nameText = ImageDraw.Draw(template)
    institutionText = ImageDraw.Draw(template)
    for j in range(4):
        if len(str(num)) == 1:
            formatted_num = f'000{num}'
        elif len(str(num)) == 2:
            formatted_num = f'00{num}'
        elif len(str(num)) == 3:
            formatted_num = f'0{num}'
        else:
            formatted_num = str(num) 

        code = f'ITI-{formatted_num}'
        namefontsize = 80
        institutionfontsize = 60

        qr_code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=18)
        qr_code.add_data(code)
        qr_code.make()
        img_qr_code = qr_code.make_image(fill_color="#1A1364",back_color="white").convert("RGB")
        pos = (image_x[j],image_y[j])
        template.paste(img_qr_code, pos)
        mark_width, mark_height = tagNumberFont.getsize(code)
        name = str(df['NAMES'][num-1]).upper()
        institution = str(df['INSTITUTIONS'][num-1]).upper()
        nameFont = ImageFont.truetype('Oswald-Regular.ttf', namefontsize)
        institutionFont = ImageFont.truetype('Oswald-Regular.ttf', institutionfontsize)
        name_width, _ = nameFont.getsize(name)
        while name_width > name_max_width:
            namefontsize = namefontsize - 2
            nameFont = ImageFont.truetype('Oswald-Regular.ttf', namefontsize)
            name_width, _ = nameFont.getsize(name)
        institution_width, _ = institutionFont.getsize(institution)
        while institution_width > institution_max_width:
            institutionfontsize = institutionfontsize - 2
            institutionFont = ImageFont.truetype('Oswald-Regular.ttf', institutionfontsize)
            institution_width, _ = institutionFont.getsize(institution)    
        nameText.text((tag_center_x[j] - name_width/2, name_y[j]), name, font=nameFont ,fill=(26, 19, 100))
        institutionText.text((tag_center_x[j] - institution_width/2, institution_y[j]), institution, font=institutionFont ,fill=(209, 2, 8))
        textImage = Image.new('RGBA', (mark_width, mark_height), (255, 255, 255, 1))
        draw = ImageDraw.Draw(textImage)
        draw.text((0, 0), code, font=tagNumberFont ,fill=(209, 2, 8))
        textImage = textImage.rotate(90,expand=1)
        pos2 = (text_x[j], text_y[j])
        template.paste(textImage, pos2)
        df.at[num-1,'CODES'] = code
        num += 1
    filename = f'Batch_{i+1}.jpg'
    template.save(filename)
df.to_excel('Participants.xlsx',index=False)
