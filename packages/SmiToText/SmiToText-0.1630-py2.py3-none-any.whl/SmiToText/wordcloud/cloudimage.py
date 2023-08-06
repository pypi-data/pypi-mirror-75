import argparse
import json
import os
from collections import Counter

import matplotlib as mpl

mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from wordcloud import WordCloud

from SmiToText.frequency.word import word_tags
from SmiToText import __ROOT_DIR__


def wordcloud_gen(keywords, save_path, width=1000, height=1000, font_path='', image=''):
    if image != '':
        mask = np.array(Image.open(image))
        wordcloud = WordCloud(
            margin=1,
            font_path=font_path,
            width=width,
            height=height,
            background_color="white",
            # prefer_horizontal=0.9999,  # horizontal preference
            # min_font_size=5,  # min font size
            # max_font_size=40,
            mask=mask
        )
    else:
        wordcloud = WordCloud(
            margin=2,
            font_path=font_path,
            width=width,
            height=height,
            background_color="white",
            # prefer_horizontal=0.9999,  # horizontal preference
            # min_font_size=5,  # min font size
            # max_font_size=40,
            # mask=mask
        )
    wordcloud = wordcloud.generate_from_frequencies(keywords)
    fig = plt.figure(figsize=(8, 8), dpi=300)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()

    # plt.show()
    fig.savefig(save_path)


if __name__ == '__main__':
    texts = '이것 은 예문 입니다. 여러분 의 문장을 넣 으세요'
    # keywords = {'이것': 5, '예문': 3, '단어': 5, '빈도수': 3}
    default_font_path = __ROOT_DIR__ + os.sep + 'SmiToText' + os.sep + 'font' + os.sep + 'Goyang.ttf'

    # print(default_font_path)
    parser = argparse.ArgumentParser(description="Word Cloud Generator")
    parser.add_argument('--input', type=str, required=True, default='', help='Input File')
    parser.add_argument('--output', type=str, required=True, default='', help='Word Cloud Image File')
    parser.add_argument('--font', type=str, required=False, default='', help='Word Cloud Font File')
    parser.add_argument('--lang', type=str, required=False, default='en', help='Lang Check( en, ko ), defalut en')
    parser.add_argument('--type', type=str, required=False, default='text', help='Select Counter or Text')
    parser.add_argument('--image', type=str, required=False, default='', help='Shape Image File')
    parser.add_argument('--exclude', type=str, required=False, default='', help='Word Cloud Exclude File')

    args = parser.parse_args()
    if not args.input:
        print("Input File is invalid!")
        exit(1)

    if not args.output:
        print("Word Cloud Image File!")
        exit(1)

    input = str(args.input)
    output = str(args.output)
    font = str(args.font)
    lang = str(args.lang)
    image = str(args.image)
    type = str(args.type)
    exclude = str(args.exclude)

    exclude_word = []

    if not font:
        font = default_font_path

    if exclude:
        with open(exclude, encoding='utf-8', mode='r') as exclude_file:
            lines = exclude_file.readlines()
            for line in lines:
                if len(line.strip()) > 0:
                    exclude_word.append(line.strip())

    print(font)
    countText = Counter()
    if type.lower() == 'text':
        with open(input, encoding='utf-8', mode='r') as input_file:
            lines = input_file.readlines()
            tempCountText = Counter()
            for line in lines:
                line = line.strip()
                if line not in exclude_word:
                    tempCountText = word_tags(line)
                    countText = countText + tempCountText
                # else:
                #     print(line)
    else:
        with open(input, encoding='utf-8', mode='r') as json_file:
            countText = json.load(json_file)

            if len(countText) > 0:
                for word in list(countText.keys()):
                    word = word.strip()
                    if len(exclude_word) > 0:
                        for exclude_word_item in exclude_word:
                            exclude_word_item = exclude_word_item.strip()
                            if word.find(exclude_word_item) >= 0:
                                del countText[word]
                                # print(exclude_word_item, word)
                                break

    wordcloud_gen(countText, output, font_path=font, image=image)
