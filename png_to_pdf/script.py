from PIL import Image

image_1 = Image.open('C:\\Users\\kumar\\Pictures\\passports\\Ravi_pp_1.jpg')
image_2 = Image.open('C:\\Users\\kumar\\Pictures\\passports\\Ravi_pp_2.jpg')

im_1 = image_1.convert('RGB')
im_2 = image_2.convert('RGB')

image_list = [im_2]

im_1.save(r'C:\\Users\\kumar\\Pictures\\passports\\Ravi_pp.pdf', save_all=True, append_images=image_list)
