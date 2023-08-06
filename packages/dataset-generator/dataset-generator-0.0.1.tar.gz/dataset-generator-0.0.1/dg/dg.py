#!/usr/bin/env python3

"""dg - Dataset Generator"""

import os
import cv2
import json
import time
import shutil
import glob
import random
import numpy as np


class DataSetGenerator:
    """
	this is the main class from which many
	subclasses are derived .
	"""

    def __init__(self, name, save_path="", bg_colour=None, prints=False):
        """
		basic attributes and functions that
		has to initialized for every dataset
		class .
		"""
        self.name = name
        if not save_path.endswith("/") and save_path != "":
            save_path = save_path + "/"
        self.save_path = save_path
        self.print = prints
        self.ids = []
        self.img_paths = []
        self.bgs = []

    def generate(self, size, count, channels=3):
        """call general functions for data generation"""
        self.size = size
        self.h, self.w = size
        self.count = count
        self.channels = channels
        self.make_path()
        self.create_list()
        self.create_json()
        t = time.time()
        for i, (path, img, mask) in enumerate(self.gen()):
            cv2.imwrite(path, img)
            if mask:
                *p, id_ = path.split("/")
                cv2.imwrite(f"{self.save_path}{self.name}/masks/{id_}", mask)
            if self.print:
                print("[Done {:6d}]   [Time:   {:.2f} s]".format(i, time.time() - t))
                t = time.time()

    def make_path(self):
        """
		create default directories for storing the
		dataset csv file and the images .
		"""
        folders = [
            f"{self.save_path}{self.name}/json/",
            f"{self.save_path}{self.name}/images/",
        ]
        if hasattr(self, "masks"):
            folders.append(f"{self.save_path}{self.name}/masks/")
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def create_list(self):
        """create image ids and paths ."""
        for _ in range(self.count):
            id_ = random.randint(10000, 99999)
            self.ids.append(id_)
            self.img_paths.append(f"{self.save_path}{self.name}/images/{id_}.png")
            if hasattr(self, "masks"):
                self.masks.append(f"{self.save_path}{self.name}/masks/{id_}.png")

    def create_json(self):
        """create json file to store ids,paths and bgs"""
        data = {"image_id": self.ids, "img_path": self.img_paths, "bg": self.bgs}
        if hasattr(self, "bbox"):
            data["bbox"] = self.bbox
        if hasattr(self, "masks"):
            data["masks"] = self.masks
        with open(f"{self.save_path}{self.name}/json/images_info.json", "w") as f:
            json.dump(data, f)

    def cleanup(self):
        """delete already existing dataset"""
        if os.path.exists(f"{self.save_path}{self.name}"):
            shutil.rmtree(f"{self.save_path}{self.name}")


class PlainSet(DataSetGenerator):
    """a plain images dataset generator"""

    def __init__(self, name, bg_colour=None, save_path="", prints=False):
        super().__init__(name, save_path=save_path, prints=prints)
        self.bg = bg_colour

    def gen(self):
        """generate images and return path ,img"""
        c = self.channels
        for path, bg in zip(self.img_paths, self.bgs):
            plain = np.ones((self.h, self.w, c), dtype=np.uint8)
            yield path, (plain * bg).astype(np.uint8), None

    def create_list(self):
        """
		handle the backgrounds specific for 
		PlainSet .
		"""
        super().create_list()
        for i in range(self.count):
            if not self.bg:
                bg = [random.randint(0, 255) for _ in range(self.channels)]
            elif len(self.bg) != 1:
                bg = self.bg[i % len(self.bg)]
            else:
                bg = self.bg
            self.bgs.append(bg)


class ObjectSet(DataSetGenerator):
    """
	common class for both object over plainset 
	and object over some backgrounds
	"""

    def __init__(
        self,
        name,
        obj,
        resize=None,
        bg_colour=None,
        mask_required=False,
        save_path="",
        prints=False,
    ):
        """get the object image"""
        # add bg to the arguement bcoz of mro
        super().__init__(name, bg_colour=bg_colour, save_path=save_path, prints=prints)

        if isinstance(obj, str):
            self.objects = [cv2.imread(obj, -1)]
        else:
            self.objects = [cv2.imread(ob, -1) for ob in obj]
        self.alphas = []
        for i in range(len(self.objects)):
            if resize:
                self.objects[i] = cv2.resize(self.objects[i], resize)
            ob = self.objects[i]
            if ob.shape[2] == 4:
                alpha = ob[:, :, 3]
            else:
                alpha = np.ones(ob.shape[:2], dtype=np.uint8) * 255
            self.alphas.append(alpha)
        self.bbox = []
        if mask_required:
            self.masks = []

    def create_list(self):
        """create bbox list"""
        super().create_list()
        for i in range(self.count):
            box = []
            for ob in self.objects:
                h, w, c = ob.shape
                x = random.randrange(0, self.w - w)
                y = random.randrange(0, self.h - h)
                box.append([x, y, w, h])
            self.bbox.append(box)

    def alpha_blend(self, img, obj, bbox, alpha):
        """do alpha blending"""
        x, y, w, h = bbox
        img = cv2.resize(img, self.size)
        for i in range(0, 3):
            img[y : y + h, x : x + w, i] = img[y : y + h, x : x + w, i] * (
                1 - alpha / 255.0
            ) + obj[:, :, i] * (alpha / 255.0)
        if hasattr(self, "masks"):
            mask = np.zeros((3, self.h, self.w), dtype=np.uint8)
            mask[1, y : y + h, x : x + w] = alpha / 255
            mask[0] = cv2.bitwise_not(mask[1]) / 255
            mask = mask.transpose((1, 2, 0))
        else:
            mask = False
        return img, mask


class ObjectOverPlainSet(ObjectSet, PlainSet):
    """object over plain images  ."""

    # so inherited both objectset and plainset

    def gen(self):
        """
		call plainimage generator and return 
		the alpha blended image
		"""
        for bbox, (path, plain, _) in zip(self.bbox, super().gen()):
            for alpha, obj, box in zip(self.alphas, self.objects, bbox):
                plain, mask = self.alpha_blend(plain, obj, box, alpha)
            yield path, plain, mask


class ObjectOverBackgroundSet(ObjectSet):
    def __init__(
        self,
        name,
        obj,
        bg,
        mask_required=False,
        resize=None,
        save_path="",
        prints=False,
    ):
        """get the background """
        super().__init__(
            name,
            obj,
            resize=resize,
            mask_required=mask_required,
            save_path=save_path,
            prints=prints,
        )
        self.bg = bg
        if isinstance(bg, str):
            self.background = [bg]
        else:
            self.background = []
            for img in bg:
                self.background.append(img)

    def create_list(self):
        """create a background list"""
        super().create_list()
        for i in range(self.count):
            self.bgs.append(i % len(self.background))

    def gen(self):
        """
		return alpha blended image for every 
		background image.
		"""
        for path, bg_idx, bbox in zip(self.img_paths, self.bgs, self.bbox):
            img = cv2.imread(self.background[bg_idx])
            for alpha, obj, box in zip(self.alphas, self.objects, bbox):
                img, mask = self.alpha_blend(img, obj, box, alpha)
            yield path, img, mask


if __name__ == "__main__":

    object_paths = ['../samples/object1.png', '../samples/object2.png']
    background_path = '../samples/background.jpg'
    ob = ObjectOverBackgroundSet(
        name="dataset",
        obj=object_paths,
        bg=background_path,
        resize=(20, 20),
        prints=True,
    )
    ob.cleanup()
    ob.generate(size=(500, 500), count=10)
