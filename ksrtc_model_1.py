# -*- coding: utf-8 -*-
"""KSRTC Model 1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XAjmwmuRcCHISvemBjhlwCxW0Eo4dy7Y
"""

!pip install -Uqq fastai 'duckduckgo_search>=6.2'

from duckduckgo_search import DDGS #DuckDuckGo has changed the api so we need to update
from fastcore.all import *

def search_images(keywords, max_images=200): return L(DDGS().images(keywords, max_results=max_images)).itemgot('image')
import time, json

urls = search_images("Venad KSRTC", max_images=1)

from fastdownload import download_url

download_url(urls[0], "cover.jpg")

from fastai.vision.all import *
im = Image.open("cover.jpg")
im.to_thumb(255, 255)

download_url(search_images("City Circular KSRTC", max_images=2)[1], "man.jpg")

im = Image.open("man.jpg")
im.to_thumb(256, 256)

from google.colab import drive
drive.mount('/content/drive')

!ls drive/MyDrive/bus-type

path = Path("drive/MyDrive/bus-type")

failed = verify_images(get_image_files(path))
failed.map(Path.unlink)
len(failed)

dls = DataBlock(blocks=(ImageBlock, CategoryBlock),
               get_items=get_image_files,
               splitter= RandomSplitter(valid_pct=0.2, seed=42),
                get_y = parent_label,
                item_tfms=[Resize(192, ResizeMethod.Squish)]
               ).dataloaders(path, bs=3)

dls.show_batch(max_n=30)

learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(5)

download_url(search_images("Red KSRTC", max_images=2)[1], "man.jpg")
im = Image.open("man.jpg")
im.to_thumb(255, 255)

is_circular, _, probs = learn.predict(PILImage.create(im))

higher = max(probs[0], probs[1])
print(f"This is a: {is_circular}.")
print(f"Probability it's a {is_circular}: {higher:.4f}")
im = Image.open("man.jpg")
im.to_thumb(256, 256)

print(probs)

is_circular, _, probs = learn.predict(PILImage.create(im))

