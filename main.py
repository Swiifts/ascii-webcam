from converter import Converter 

def main():
    converter = Converter(1000, 20, 10) 
    ascii_image = converter.image_to_ascii_image("test.jpg")
    ascii_image.show()
    ascii_image.save("ascii_output.png")

if __name__ == "__main__":
    main()
