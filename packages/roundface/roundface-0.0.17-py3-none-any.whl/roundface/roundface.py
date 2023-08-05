import os
import cv2
import numpy as np
import argparse
import glob


class RoundFace:
    def __init__(self, source, output_size, is_greyed, radius=1.0):
        base_dir = os.path.dirname(__file__)
        prototxt = os.path.join(base_dir , 'model','deploy.prototxt')
        caffemodel = os.path.join(base_dir , 'model','weights.caffemodel')

        self.base_dir = base_dir
        self.output_size = output_size
        self.is_greyed = bool(is_greyed)
        self.allowed_extensions = ('.jpg', '.jpeg', '.png')
        self.image_source = self.validate_image_source(source)
        self.source_is_file = os.path.isfile(self.image_source)
        self.dest_dir = self.create_dest_dir()
        self.radius = radius

        self.model = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
        self.face_count = 0

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        if value < 0.5:
            self.__radius = 0.5
        else:
            self.__radius = value

    def process(self):
        if self.source_is_file:
            self.process_image(self.image_source)
        else:
            self.process_folder()

    def process_folder(self):
        old_working_dir = os.getcwd()
        os.chdir(self.image_source)
        for ext in self.allowed_extensions:
            images = glob.glob(f'*{ext}')
            for img in images:
                self.process_image(img)

        os.chdir(old_working_dir)

    def process_image(self, filepath):
        _, name = os.path.split(filepath)
        extension = name[name.index('.', -5):].lower()

        if not extension in self.allowed_extensions:
            raise Exception("Invalid Image File")

        image = cv2.imread(filepath)
        height, width = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0))

        self.model.setInput(blob)
        detections = self.model.forward()

        for i in range(0, detections.shape[2]):
            face_box = detections[0, 0, i, 3:7] * np.array(
                [width, height, width, height])
            start_x, start_y, end_x, end_y = face_box.astype(np.int)

            confidence = detections[0, 0, i, 2]

            if (confidence > 0.5):
                center = ((start_x + end_x) // 2, (start_y + end_y) // 2)
                radius = int((end_y - start_y) * self.radius)

                new_start_x, new_end_x, new_start_y, new_end_y = (
                    center[0] - radius, center[0] + radius, center[1] - radius,
                    center[1] + radius)

                profile_image = image[new_start_y:new_end_y, new_start_x:
                                      new_end_x]
                self.save_image(profile_image, i, name)
                self.face_count += 1

    def save_image(self, profile_image, face_index, name):
        if profile_image.size == 0:
            return

        grey_photo = cv2.cvtColor(profile_image, cv2.COLOR_BGR2GRAY)

        if self.output_size:
            size = self.output_size
            profile_image = cv2.resize(profile_image, (size, size))
            grey_photo = cv2.resize(grey_photo, (size, size))

        if self.is_greyed:
            cv2.imwrite(f'{self.dest_dir}/{face_index}-{name}', grey_photo)
        else:
            cv2.imwrite(f'{self.dest_dir}/{face_index}-{name}', profile_image)

    def validate_image_source(self, image_path):
        validated_path = image_path
        working_dir = os.getcwd()
        relative_path = os.path.join(working_dir, image_path)

        if os.path.exists(relative_path):
            validated_path = relative_path

        else:
            if not os.path.exists(image_path):
                raise Exception("Invalid Image Source")

        return validated_path

    def create_dest_dir(self):
        source_parent = os.path.dirname(self.image_source)
        dest_dir = os.path.join(source_parent, "roundface")

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        return dest_dir

def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--source', required=True,
                        help="Image Source. It can be a file or folder")

    parser.add_argument('-g', '--grey', type=int, default=0,
        help="Whether resulting photos should be greyed out. 0 for False, 1 for True.")

    parser.add_argument('-sz', '--size', type=int,
                        help="Number. Output size in pixels.")

    parser.add_argument('-r','--radius', type=float, default=1.0,
                        help="Float. Adjust photo radius to a given ratio")
    args = parser.parse_args()

    rf = RoundFace(args.source, args.size, args.grey, args.radius)
    rf.process()

if __name__ == "__main__":
    execute()
