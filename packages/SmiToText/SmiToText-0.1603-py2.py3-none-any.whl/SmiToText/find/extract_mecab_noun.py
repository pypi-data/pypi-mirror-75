import argparse

import os
from datetime import date

from SmiToText.tokenizer.nltk import nltkSentTokenizer
from SmiToText.util.util import Util

util = Util()


def expect_noun_text(text):
    word_list = []
    check_word_end = ['.', ':', ';', '!', '?', '\"', '\'', '”']

    exclude_char_list = ['[', ']', '\'', '\"', ')', '(', '「', '」', '-', '」', '「', '’', ':', '/', '”', '“', '?', '!',
                         '~', '-', ',', 'ㆍ', '◇', '△', '〃', '〈', '〉', '·', '+', '▲', '○', '【', '…',
                         ]
    # end_char_exclude_list = [
    #     '잡는', '잡은', '라는', '하는', '르는', '가는', '기는', '에는', '에서는', '보는', '다는', '되는', '또는', '어지', '이냐',
    #     '함', '들어지', '어지는', '함을', '때로는', '이제는', '느끼는', '느껴지는', '위해서', '였음', '있', '봤', '있는', '있고', '있다', '있을',
    #     '만큼', '리려', '이', '가', '했', '들', '쉬움', '와는', '연결만', '정확히', '연결만으로', '연결만큼은', '알려주는', '위해서는', '정확히는', '정확히',
    #     '본격적', '빼돌리려는', '재미있는', '재미있다', '달려있는지는', '달려있는지를', '받는', '받고', '받음', '받다', '받어', '받기', '받은', '받을',
    #     '했음', '했음을', '했을', '했다', '했음으로', '했기에', '늘어나고', '늘어나는', '비싸지는', '비싸지다', '떨어트리고', '떨어트리는', '떨어트리다', '떨어트리러',
    #     '시키는', '시키다', '시키러', '시키고', '두드러지는', '두드러지다', '두드러지고', '두드러진다', '두드러지는데', '이루어지고', '이루어지고는', '이루어지는', '이루어지는데',
    #     '이루어진다',
    #     '이뤄지고', '이뤄지는', '이뤄지고는', '이뤄지는데', '대해서는', '대해서를', '어울리는', '어울리고', '어울리는데', '어울리다', '달래주는', '달래주고', '달래주는데',
    #     '달래주다',
    #     '달래주기', '몰아주기는', '몰아주기로', '몰아주기를', '더하려는', '더하려고', '더하려고는', '뛰어넘는', '뛰어넘다', '뛰어넘기', '뛰어넘을', '보여주기', '보여주는',
    #     '보여주다',
    #     '대여해주는', '대여해주기', '대여해주다',
    #     '높여지는', '높여지고', '높여지다', '높아지는', '높아지고', '높아지다',
    #     '꾀하려는', '꾀하려고', '꾀하려고는', '제공함을', '제공함이', '제공함과',
    #     '움과', '움이', '움을', '내는', '내고는', '내기', '흔드는', '랬냐는', '랬냐고', '하는지는', '하는지를', '오르내리는', '오르내리다', '오르내리기',
    #     '보이는', '보이기', '보이다', '까지는', '까지를', '까지와', '감싸주는', '감싸주기', '감싸주고', '감싸주다', '관련해서는', '관련해서와', '말까',
    #     '돌아오는', '돌아오다', '돌아오기', '뛰어드는', '뛰어드', '자리잡았는', '자리잡았기', '자리잡았고', '자리잡았다', '자리잡았을',
    #     '찾아오는', '찾아오다', '찾아오기', '찾아오는데', '찾아오기를', '찾아오기만', '만이', '만을', '만은', '만으로는', '만으로', '어지간해서는', '어지간해서',
    #     '흔들리는', '흔들리고', '흔들리다', '흔들리며', '쏟아지는','쏟아지기', '쏟아지고','몰아치고', '몰아치는', '몰아치다', '판매되었', '판매되었기', '판매되었다', '판매되었을',
    #     '흘러나오는', '흘러나오기', '흘러나오다', '흘러나오기에', '흘러나오',
    #     '하려는', '하려고',
    # ]
    end_char_exclude_list = ['가', '가는', '기는', '그리고서', '그랬을까',
                             '까지는', '까지를', '까지와',
                             '그리고서',
                             '나오는', '나오다', '내고는', '내기', '내는', '넘기', '넘는',
                             '넘다', '넘을',
                             '되는', '되었', '되었기', '되었다', '되었을', '드는', '들', '들리고', '들리는', '들리다에', '들어지',
                             '때로는', '또는', '뛰어드',
                             '뛰어드는', '라는', '랬냐고', '랬냐는', '려고', '려는', '르는', '리고', '리는', '리는데',
                             '리다', '리려', '리려는', '만은', '만을',
                             '만이', '만큼', '말까',
                             '받고', '보이기', '보이는', '보이다', '본격적', '봤',
                             '보거말고',
                             '쉬움', '시키고', '시키는', '시키다', '시키러',
                             '아치고', '아치는', '아치다', '어지', '어지는', '에는', '에도', '에와', '에서는', '에서를', '에서도',
                             '오기', '오기만',
                             '오는', '오는', '오는데', '오다', '오다', '으로', '으로', '으로는', '이', '이냐', '이제는', '있', '있고', '있는',
                             '있다',
                             '있을', '잡았', '잡았고', '잡았기', '잡았는', '잡았다', '주고', '주기', '주기는', '주기로', '주기를', '주는',
                             '주는', '주다', '지고',
                             '지고', '지고', '지고', '지고', '지고', '지고는', '지고는', '지기', '지는', '지는', '지는',
                             '지는', '지는', '지는', '지는', '지는',
                             '지는', '지는데', '지는데', '지는데', '지다', '지다', '지다', '지다', '지를',
                             '진다', '진다', '트리고', '트리는', '트리러', '하는',
                             '하려고', '하려고', '하려고는', '하려고는', '하려는', '하려는',
                             '함', '함을', '해서', '해서', '해서는', '해서는', '해서는', '해서는',
                             '해서를', '해서와', '해주기', '해주는', '해주다',
                             '했', '했기에', '했다', '했을', '했음', '했음을',
                             '다는', '다를', '다와', '다고',
                             '였음', '였음을', '였음과',
                             '했느냐는', '했느가는', '했는냐는', '했는가는', '했는가를',
                             '잡았을', '잡았기', '잡았고', '잡았다',
                             '겠냐는', '겠다는', '부터는', '부터', '하자는', '하는', '걱정을', '맞추는', '들이는', '들이다', '들이기', '들이고',
                             '았다', '았던', '음을', '되기를', '되기는', '다고는', '다고', '았을', '았기', '으로서', '으로서는', '었고', '었다', '었는데',
                             '해보는', '해보기', '해보기를', '해보기는', '로는', '와는', '지기는', '지기를', '지기도',
                             '하느냐는', '하느냐', '하기를', '하기는', '들이는', '들이기', '들이다', '한가를', '한가는',
                             '시키기를', '라고는', '라고', '와는', '제외하고는', '할까는',
                             '시키자는', '시키자를', '되기를', '되기는', ]

    end_char_include_list = ['에게는',
                             '했',
                             '만큼은', '들을', '들은', '들과', '들이', '과는', '으로', '으로는', '을', '를', '은',
                             '는', '과', '와', '로']

    end_char_replace_list = [ '는것',
                              '에서', '이냐', '이상',
                              '하기', '할때', '하시', '해놓',  ]
    for word in text.split():

        if word.endswith(tuple(check_word_end)):
            word = word[:len(word) - 1]

        if not any([char for char in exclude_char_list if char in word]):
            if not word.endswith(tuple(end_char_exclude_list)) and word.endswith(tuple(end_char_include_list)):

                for item in end_char_include_list:
                    if word.endswith(item):
                        word = word.replace(item, '')
                        if len(word) > 3 and len(word) < 15 and not util.is_int(word) and not util.is_alpha(word):
                            for remove_item in end_char_replace_list:
                                if word.endswith(remove_item) :
                                    word = util.rreplace(word, remove_item, '', 1)

                            word_list.append(word)
                            break;

    return word_list


def extract_file_noun(input, output):
    input_file = open(input, mode='r', encoding='utf-8')
    open(output, mode='w', encoding='utf-8')
    output_file = open(output, mode='a', encoding='utf-8')
    line_number = 1
    while (True):
        line = input_file.readline()
        if not line:
            break;

        line = line.strip()

        for line_array in line.split("\n"):
            sentences = nltkSentTokenizer(line_array)

            sentence_words = []
            for sent in sentences:

                word_list = expect_noun_text(sent)

                if len(word_list):
                    for word in word_list:
                        if util.check_email(word) :
                            continue
                        else:
                            add_flag = True
                            for char in word:
                                if char in ["‘", "`", ",", "'", "\"", "|", "!", "@", "#", "$", "%", "^", "&", "*", "(",
                                            ")",
                                            "-", "_", "=", "+", "<", ">", ".", ";", ":",
                                            "ㄱ", "ㄴ", "ㄲ", "ㅂ", "ㅃ", "ㅈ", "ㅉ", "ㄷ", "ㄸ", "ㄱ", "ㅁ", "ㅇ", "ㄹ", "ㅎ", "ㅅ", "ㅆ",
                                            "ㅍ", "ㅊ", "ㅌ", "ㅋ", "ㅛ", "ㅕ", "ㅑ", "ㅐ", "ㅔ", "ㅗ", "ㅓ", "ㅏ", "ㅣ", "ㅠ", "ㅜ",
                                            "ㅡ"]:
                                    add_flag = False

                            if word == '기자' or word == str(date.today().day) + '일':
                                add_flag = False

                            if add_flag:
                                output_file.write(word + os.linesep)
                                sentence_words.append(word)
                            # print(line_number, word)
        print(line_number, sentence_words)
        line_number += 1


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Extract File Noun word")
    parser.add_argument('--input', type=str, required=True, default='', help='Input File')
    parser.add_argument('--output', type=str, required=True, default='', help='Output File')
    args = parser.parse_args()

    if not args.input:
        print("input file is invalid!")
        exit(1)

    if not args.output:
        print("output file is invalid!")
        exit(1)

    input = str(args.input)
    output = str(args.output)

    extract_file_noun(input, output)

