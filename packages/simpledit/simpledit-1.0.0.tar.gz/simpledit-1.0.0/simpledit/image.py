class ImageObject(object):
    def __init__(self, img, file_name, save_status):
        self.images = [img]
        self.file_name = file_name
        self.save_state = save_status
        self.index = 0

    def add_image(self, index, img):
        self.images = self.images[0:self.index]
        self.images.insert(index, img)
    
    def get_current_image(self):
        return self.images[self.index]
    
    def get_index(self):
        return self.index

    def increment_index(self):
        self.index +=1
    
    def decrement_index(self):
        self.index -=1

    def num_images(self):
        return len(self.images)

    def get_original_image(self):
        return self.images[0]
