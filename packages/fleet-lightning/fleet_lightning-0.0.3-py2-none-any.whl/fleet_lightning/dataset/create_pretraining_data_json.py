# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Create masked LM/next sentence masked_lm TF examples for BERT."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import collections
import random
import sys
sys.path.append("..")
import tokenization
import tensorflow as tf

flags = tf.flags

FLAGS = flags.FLAGS

flags.DEFINE_string("hdfs_input", None,
                        "hdfs input path of current generation")

flags.DEFINE_string("hdfs_output_path", None,
                    "hdfs output path of current generation")

flags.DEFINE_string("vocab_file", None,
                    "The vocabulary file that the BERT model was trained on.")

flags.DEFINE_bool(
    "do_lower_case", True,
    "Whether to lower case the input text. Should be True for uncased "
    "models and False for cased models.")

flags.DEFINE_integer("max_seq_length", 128, "Maximum sequence length.")

flags.DEFINE_integer("max_predictions_per_seq", 20,
                     "Maximum number of masked LM predictions per sequence.")

flags.DEFINE_integer("random_seed", 12345, "Random seed for data generation.")

flags.DEFINE_integer(
    "dupe_factor", 10,
    "Number of times to duplicate the input data (with different masks).")

flags.DEFINE_float("masked_lm_prob", 0.15, "Masked LM probability.")

flags.DEFINE_float(
    "short_seq_prob", 0.1,
    "Probability of creating sequences which are shorter than the "
    "maximum length.")


class TrainingInstance(object):
    """A single training instance (sentence pair)."""

    def __init__(self, tokens, segment_ids, masked_lm_positions,
                 masked_lm_labels, is_random_next):
        self.tokens = tokens
        self.segment_ids = segment_ids
        self.is_random_next = is_random_next
        self.masked_lm_positions = masked_lm_positions
        self.masked_lm_labels = masked_lm_labels

    def __str__(self):
        s = ""
        s += "tokens: %s\n" % (" ".join(
            [tokenization.printable_text(x) for x in self.tokens]))
        s += "segment_ids: %s\n" % (" ".join(
            [str(x) for x in self.segment_ids]))
        s += "is_random_next: %s\n" % self.is_random_next
        s += "masked_lm_positions: %s\n" % (" ".join(
            [str(x) for x in self.masked_lm_positions]))
        s += "masked_lm_labels: %s\n" % (" ".join(
            [tokenization.printable_text(x) for x in self.masked_lm_labels]))
        s += "\n"
        return s

    def __repr__(self):
        return self.__str__()

def get_values_str(name, features):
    feature = features[name]
    values = []
    if feature.int64_list.value:
        values = feature.int64_list.value
    elif feature.float_list.value:
        values = feature.float_list.value
    value_str = " ".join([str(x) for x in values])
    value_str = tokenization.printable_text(value_str)
    return value_str

def write_instance_to_plain_text(instances, tokenizer, max_seq_length,
                                 max_predictions_per_seq, output_path,
                                 rank):
    upload_files = []

    filename_prefix = output_path + "/part-" + str(rank)

    file_index = 0

    pair_per_file = 51200

    total_written = 0

    cur_fout = None

    for (inst_index, instance) in enumerate(instances):
        input_ids = tokenizer.convert_tokens_to_ids(instance.tokens)
        input_mask = [1] * len(input_ids)
        segment_ids = list(instance.segment_ids)
        assert len(input_ids) <= max_seq_length
        
        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length

        masked_lm_positions = list(instance.masked_lm_positions)
        masked_lm_ids = tokenizer.convert_tokens_to_ids(
            instance.masked_lm_labels)
        masked_lm_weights = [1.0] * len(masked_lm_ids)

        while len(masked_lm_positions) < max_predictions_per_seq:
            masked_lm_positions.append(0)
            masked_lm_ids.append(0)
            masked_lm_weights.append(0.0)

        next_sentence_label = 1 if instance.is_random_next else 0

        features = collections.OrderedDict()
        features["input_ids"] = create_int_feature(input_ids)
        features["input_mask"] = create_int_feature(input_mask)
        features["segment_ids"] = create_int_feature(segment_ids)
        features["masked_lm_positions"] = create_int_feature(
            masked_lm_positions)
        features["masked_lm_ids"] = create_int_feature(masked_lm_ids)
        features["masked_lm_weights"] = create_float_feature(masked_lm_weights)
        features["next_sentence_labels"] = create_int_feature(
            [next_sentence_label])

        tf_example = tf.train.Example(features=tf.train.Features(
            feature=features))

        total_written += 1

        tokens = [tokenization.printable_text(x) for x in instance.tokens]
        token_str = " ".join(tokens)
        input_ids_str = get_values_str("input_ids", features)
        input_mask_str = get_values_str("input_mask", features)
        segment_ids_str = get_values_str("segment_ids", features)
        masked_lm_positions_str = get_values_str("masked_lm_positions", features)
        masked_lm_ids_str = get_values_str("masked_lm_ids", features)
        masked_lm_weights_str = get_values_str("masked_lm_weights", features)
        next_sentence_labels_str = get_values_str("next_sentence_labels", features)

        #all_str = [token_str, input_ids_str, input_mask_str, segment_ids_str,
        #masked_lm_positions_str, masked_lm_ids_str, masked_lm_weights_str,
        #next_sentence_labels_str]
        all_str = [input_ids_str, input_mask_str, segment_ids_str,
                   masked_lm_positions_str, masked_lm_ids_str, masked_lm_weights_str,
                   next_sentence_labels_str]
        
        if inst_index % pair_per_file == 0:
            if cur_fout != None:
                cur_fout.close()
                file_index += 1
            tf.logging.info("*** rank " + str(rank) + " save file " + filename_prefix + "-" + str(file_index) + ".txt")
            cur_fout = open(filename_prefix + "-" + str(file_index) + ".txt", "w")
            upload_files.append(filename_prefix + "-" + str(file_index) + ".txt")
            
        cur_fout.write(";".join(all_str) + "\n")
    return upload_files


def create_int_feature(values):
    feature = tf.train.Feature(int64_list=tf.train.Int64List(
        value=list(values)))
    return feature


def create_float_feature(values):
    feature = tf.train.Feature(float_list=tf.train.FloatList(
        value=list(values)))
    return feature


def create_training_instances(input_files, tokenizer, max_seq_length,
                              dupe_factor, short_seq_prob, masked_lm_prob,
                              max_predictions_per_seq, rng):
    """Create `TrainingInstance`s from raw text."""
    all_documents = [[]]

    # Input file format:
    # (1) One sentence per line. These should ideally be actual sentences, not
    # entire paragraphs or arbitrary spans of text. (Because we use the
    # sentence boundaries for the "next sentence prediction" task).
    # (2) Blank lines between documents. Document boundaries are needed so
    # that the "next sentence prediction" task doesn't span between documents.
    def parse_json(reader):
        while True:
            doc = reader.readline()
            if not doc:
                break
            doc = unicode(doc, errors='ignore')
            doc = json.loads(doc, encoding='utf-8')
            lines = doc['text'].split('\n\n')
            for line in lines:
                line += '\n'
                yield line


    for input_file in input_files:
        with tf.gfile.GFile(input_file, "r") as reader:
            for line in parse_json(reader):
                line = tokenization.convert_to_unicode(line)
                if not line:
                    break
                line = line.strip()

                # Empty lines are used as document delimiters
                if not line:
                    all_documents.append([])
                tokens = tokenizer.tokenize(line)
                if tokens:
                    all_documents[-1].append(tokens)

    # Remove empty documents
    all_documents = [x for x in all_documents if x]
    rng.shuffle(all_documents)

    vocab_words = list(tokenizer.vocab.keys())
    instances = []
    for _ in range(dupe_factor):
        for document_index in range(len(all_documents)):
            instances.extend(
                create_instances_from_document(
                    all_documents, document_index, max_seq_length,
                    short_seq_prob, masked_lm_prob, max_predictions_per_seq,
                    vocab_words, rng))
    rng.shuffle(instances)
    return instances


def create_instances_from_document(
        all_documents, document_index, max_seq_length, short_seq_prob,
        masked_lm_prob, max_predictions_per_seq, vocab_words, rng):
    """Creates `TrainingInstance`s for a single document."""
    document = all_documents[document_index]

    # Account for [CLS], [SEP], [SEP]
    max_num_tokens = max_seq_length - 3

    # We *usually* want to fill up the entire sequence since we are padding
    # to `max_seq_length` anyways, so short sequences are generally wasted
    # computation. However, we *sometimes*
    # (i.e., short_seq_prob == 0.1 == 10% of the time) want to use shorter
    # sequences to minimize the mismatch between pre-training and fine-tuning.
    # The `target_seq_length` is just a rough target however, whereas
    # `max_seq_length` is a hard limit.
    target_seq_length = max_num_tokens
    if rng.random() < short_seq_prob:
        target_seq_length = rng.randint(2, max_num_tokens)

    # We DON'T just concatenate all of the tokens from a document into a long
    # sequence and choose an arbitrary split point because this would make the
    # next sentence prediction task too easy. Instead, we split the input into
    # segments "A" and "B" based on the actual "sentences" provided by the user
    # input.
    instances = []
    current_chunk = []
    current_length = 0
    i = 0
    while i < len(document):
        segment = document[i]
        current_chunk.append(segment)
        current_length += len(segment)
        if i == len(document) - 1 or current_length >= target_seq_length:
            if current_chunk:
                # `a_end` is how many segments from `current_chunk` go into the `A`
                # (first) sentence.
                a_end = 1
                if len(current_chunk) >= 2:
                    a_end = rng.randint(1, len(current_chunk) - 1)

                tokens_a = []
                for j in range(a_end):
                    tokens_a.extend(current_chunk[j])

                tokens_b = []
                # Random next
                is_random_next = False
                if len(current_chunk) == 1 or rng.random() < 0.5:
                    is_random_next = True
                    target_b_length = target_seq_length - len(tokens_a)

                    # This should rarely go for more than one iteration for large
                    # corpora. However, just to be careful, we try to make sure that
                    # the random document is not the same as the document
                    # we're processing.
                    for _ in range(10):
                        random_document_index = rng.randint(
                            0, len(all_documents) - 1)
                        if random_document_index != document_index:
                            break

                    random_document = all_documents[random_document_index]
                    random_start = rng.randint(0, len(random_document) - 1)
                    for j in range(random_start, len(random_document)):
                        tokens_b.extend(random_document[j])
                        if len(tokens_b) >= target_b_length:
                            break
                    # We didn't actually use these segments so we "put them back" so
                    # they don't go to waste.
                    num_unused_segments = len(current_chunk) - a_end
                    i -= num_unused_segments
                # Actual next
                else:
                    is_random_next = False
                    for j in range(a_end, len(current_chunk)):
                        tokens_b.extend(current_chunk[j])
                truncate_seq_pair(tokens_a, tokens_b, max_num_tokens, rng)

                assert len(tokens_a) >= 1
                assert len(tokens_b) >= 1

                tokens = []
                segment_ids = []
                tokens.append("[CLS]")
                segment_ids.append(0)
                for token in tokens_a:
                    tokens.append(token)
                    segment_ids.append(0)

                tokens.append("[SEP]")
                segment_ids.append(0)

                for token in tokens_b:
                    tokens.append(token)
                    segment_ids.append(1)
                tokens.append("[SEP]")
                segment_ids.append(1)

                (tokens, masked_lm_positions,
                 masked_lm_labels) = create_masked_lm_predictions(
                     tokens, masked_lm_prob, max_predictions_per_seq,
                     vocab_words, rng)
                instance = TrainingInstance(
                    tokens=tokens,
                    segment_ids=segment_ids,
                    is_random_next=is_random_next,
                    masked_lm_positions=masked_lm_positions,
                    masked_lm_labels=masked_lm_labels)
                instances.append(instance)
            current_chunk = []
            current_length = 0
        i += 1

    return instances


MaskedLmInstance = collections.namedtuple("MaskedLmInstance",
                                          ["index", "label"])


def create_masked_lm_predictions(tokens, masked_lm_prob,
                                 max_predictions_per_seq, vocab_words, rng):
    """Creates the predictions for the masked LM objective."""

    cand_indexes = []
    for (i, token) in enumerate(tokens):
        if token == "[CLS]" or token == "[SEP]":
            continue
        cand_indexes.append(i)

    rng.shuffle(cand_indexes)

    output_tokens = list(tokens)

    num_to_predict = min(max_predictions_per_seq,
                         max(1, int(round(len(tokens) * masked_lm_prob))))

    masked_lms = []
    covered_indexes = set()
    for index in cand_indexes:
        if len(masked_lms) >= num_to_predict:
            break
        if index in covered_indexes:
            continue
        covered_indexes.add(index)

        masked_token = None
        # 80% of the time, replace with [MASK]
        if rng.random() < 0.8:
            masked_token = "[MASK]"
        else:
            # 10% of the time, keep original
            if rng.random() < 0.5:
                masked_token = tokens[index]
            # 10% of the time, replace with random word
            else:
                masked_token = vocab_words[rng.randint(0, len(vocab_words) - 1)]

        output_tokens[index] = masked_token

        masked_lms.append(MaskedLmInstance(index=index, label=tokens[index]))

    masked_lms = sorted(masked_lms, key=lambda x: x.index)

    masked_lm_positions = []
    masked_lm_labels = []
    for p in masked_lms:
        masked_lm_positions.append(p.index)
        masked_lm_labels.append(p.label)

    return (output_tokens, masked_lm_positions, masked_lm_labels)


def truncate_seq_pair(tokens_a, tokens_b, max_num_tokens, rng):
    """Truncates a pair of sequences to a maximum sequence length."""
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_num_tokens:
            break

        trunc_tokens = tokens_a if len(tokens_a) > len(tokens_b) else tokens_b
        assert len(trunc_tokens) >= 1

        # We want to sometimes truncate from the front and sometimes from the
        # back to add more randomness and avoid biases.
        if rng.random() < 0.5:
            del trunc_tokens[0]
        else:
            trunc_tokens.pop()


def main(_):

    import sys
    import os
    import paddle.fluid as fluid
    from paddle.fluid.contrib.utils import HDFSClient, multi_download, multi_upload
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    world_size = comm.Get_size()
    rank = comm.Get_rank()
    hadoop_home = os.environ["HADOOP_HOME"]
    hdfs_input = FLAGS.hdfs_input
    hdfs_output_path = FLAGS.hdfs_output_path
    configs = {
        "fs.default.name": "afs://xingtian.afs.baidu.com:9902",
        "hadoop.job.ugi": "mlarch,Fv1M87"
    }

    client = HDFSClient(hadoop_home, configs)
    files = client.lsr(hdfs_input)
    os.system("rm -rf input_data")
    os.system("rm -rf output_data")
    os.system("mkdir -p input_data")
    multi_download(client, hdfs_input, "./input_data", rank, world_size, 5)
    #input_files = ["./input_data/%s" % x for x in os.listdir("input_data")]
    #file_pernode = int(len(input_files) / world_size)
    #input_files = input_files[int(rank) * file_pernode:int(rank + 1) * file_pernode]
    input_files = ["./input_data/%s" % x for x in os.listdir("input_data")]

    tf.logging.set_verbosity(tf.logging.INFO)

    tokenizer = tokenization.FullTokenizer(
        vocab_file=FLAGS.vocab_file, do_lower_case=FLAGS.do_lower_case)

    tf.logging.info("*** current rank is " + str(rank) + " ***")
    tf.logging.info("*** Reading from input files ***")

    rng = random.Random(FLAGS.random_seed)
    instances = create_training_instances(
        input_files, tokenizer, FLAGS.max_seq_length, FLAGS.dupe_factor,
        FLAGS.short_seq_prob, FLAGS.masked_lm_prob,
        FLAGS.max_predictions_per_seq, rng)

    tf.logging.info("*** Writing to output files ***")
    os.system("mkdir -p output_data")
    local_path = "input_data"

    output_path = "output_data"

    write_instance_to_plain_text(instances, tokenizer, FLAGS.max_seq_length,
                                 FLAGS.max_predictions_per_seq, output_path,
                                 rank)
    multi_upload(client, hdfs_output_path, output_path)


if __name__ == "__main__":
    flags.mark_flag_as_required("vocab_file")
    tf.app.run()
