import PIL
import csv
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)

def coords( x, y, image ):
    return [0.01 * x * image.size[0],0.01 * y * image.size[1]]

def add_banner(local_rawimg_path, local_modimg_path, timestamp, gps_coords, lux, pressure, temperature, salinity, picture_name):
    image_source = Image.open(local_rawimg_path + picture_name)
    banner_height=400
    banner = Image.new("RGBA", (image_source.size[0],banner_height), (0,0,0))
    draw = ImageDraw.Draw(banner)
    
    #LEFT SIDE
    #Date
    draw.text(coords(10,10,banner), "Timestamp:", (255,255,255), font=font)
    draw.text(coords(20,10,banner), timestamp, (255,255,255), font=font)
    #Location
    draw.text(coords(10,30,banner), "Location:", (255,255,255), font=font)
    draw.text(coords(20,30,banner), gps_coords, (255,255,255), font=font)
    
    #RIGHT SIDE
    #Pressure
    draw.text(coords(70,10,banner), "Pressure:", (255,255,255), font=font)
    draw.text(coords(80,10,banner), pressure + " mbar", (255,255,255), font=font)
    #Temperature
    draw.text(coords(70,30,banner), "Temperature:", (255,255,255), font=font)
    draw.text(coords(80,30,banner), temperature + " " + chr(176) + "C", (255,255,255), font=font)
    #Luminosity
    draw.text(coords(70,50,banner), "Luminosity:", (255,255,255), font=font)
    draw.text(coords(80,50,banner), lux, (255,255,255), font=font)
    #Salinity
    draw.text(coords(70,70,banner), "Salinity:", (255,255,255), font=font)
    draw.text(coords(80,70,banner), salinity, (255,255,255), font=font)

    draw = ImageDraw.Draw(banner)
    
    newImage = Image.new('RGB',(image_source.size[0],image_source.size[1]+banner_height))
    newImage.paste(image_source,(0,0))
    newImage.paste(banner,(0,image_source.size[1]))
    
    
    newImage.save(local_modimg_path+picture_name)
    return

#add_banner("timestamp", "lux", "pressure", "temperature", "salinity", "raw_picture.jpeg")
