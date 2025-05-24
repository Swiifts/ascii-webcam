import PIL

from PIL import Image, ImageDraw, ImageFont
from typing import List


class Converter: 
    # TODO: Move to config file
    ASCII_CHARACTERS = "$@B%8&WM*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. " # Character set used to generate ASCII image    
    font_size = 12 # Size of the font on output image
    
    #TODO: Find better font 
    font = ImageFont.load_default()

    def __init__(self, new_image_width = 100):
        self.new_image_width = new_image_width

    # Resize image 
    def resize_image(self, image: Image) -> Image:
        width, height = image.size
        ratio = height / width
        new_height = int(self.new_image_width * ratio)
        resized_image = image.resize((self.new_image_width, new_height))
        return resized_image

    # Convert image to grayscale
    def image_to_grayscale(self, image: Image) -> Image: 
        return image.conver("L")
        
    # Convert grayscale to ASCII
    def grayscale_to_ascii(self, image: Image) -> List[List[str]]:
        pixels = image.getdata()
        characters_line = "".join([self.ASCII_CHARACTERS[pixel//(256/len(self.ASCII_CHARACTERS))] for pixel in pixels]) # Convert pixels to characters based on brightness
        
        # Convert 1D string list to 2D 
        characters = [characters_line[i:i+self.new_image_width] for i in range(0, len(characters_line), self.new_image_width)]
            
        return characters

    # Convert 2D list tp image
    def ascii_to_Image(self, image: List[List[str]]) -> Image:         
        width = len(image[0])
        height = len(image)
        
        # Output image dimentions 
        char_width, char_height = self.font.getsize("A")  # approximate size of one character
        img_width = width * char_width
        img_height = height * char_height

        # Create base layer
        new_image = Image.new("L", (img_width, img_height), color=0)
        draw = ImageDraw.Draw(new_image)
        
        # Draw Characters
        for y in range(height):
            for x in range(width):
               draw.text((x*char_width, y * char_height), image[y][x], fill=255, font=self.font) 

        return new_image
    
    # Image to Image Pipeline
    def image_to_ascii_image(self, path: str) -> Image:
        image = Image.open(path)
        image = self.resize_image(image)
        grayscale = self.image_to_grayscale(image)
        ascii_matrix = self.grayscale_to_ascii(grayscale)
        ascii_image = self.ascii_to_Image(ascii_matrix)
        return ascii_image
