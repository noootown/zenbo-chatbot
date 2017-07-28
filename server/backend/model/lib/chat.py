import os
import sys

import tensorflow as tf

from . import data_utils
from .seq2seq_model_utils import create_model, get_predicted_sentence

import jieba


def chat(args):
    with tf.Session() as sess:
        # Create model and load parameters.
        args.batch_size = 1  # We decode one sentence at a time.
        model = create_model(sess, args)

        # Load vocabularies.
        vocab_path = os.path.join(args.data_dir, "vocab%d.in" % args.vocab_size)
        vocab, rev_vocab = data_utils.initialize_vocabulary(vocab_path)

        # Decode from standard input.
        sys.stdout.write("> ")
        sys.stdout.flush()
        sentence = sys.stdin.readline()

        if len(sentence.split(' ')) < 2: 
            sentence = sentence_split(sentence)

        while sentence:
            predicted_sentence = get_predicted_sentence(args, sentence, vocab, rev_vocab, model, sess)
            # print(predicted_sentence)
            if isinstance(predicted_sentence, list):
                for sent in predicted_sentence:
                    print("%s: %s" % ('chatbot', sentence_combine(sent['dec_inp'])))
                # for sent in predicted_sentence:
                #         print("  (%s) -> %s" % (sent['prob'], sent['dec_inp']))
            else:
                print(sentence, ' -> ', predicted_sentence)
                    
            sys.stdout.write("> ")
            sys.stdout.flush()
            sentence = sys.stdin.readline()
            
            if len(sentence.split(' ')) < 2: 
                sentence = sentence_split(sentence)

                
## jieba split input sentence
def sentence_split(sentence):
    seg_list = jieba.cut(sentence, cut_all=False)
    sentence = ' '.join((' '.join(seg_list)).split())
    return sentence

def sentence_combine(sentence):
    seg_list = jieba.cut(sentence, cut_all=False)
    sentence = ''.join((' '.join(seg_list)).split())
    return sentence
