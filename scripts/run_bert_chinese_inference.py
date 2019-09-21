import torch
from pytorch_transformers import (WEIGHTS_NAME, BertConfig,
                                  BertForSequenceClassification, BertTokenizer,
                                  RobertaConfig,
                                  RobertaForSequenceClassification,
                                  RobertaTokenizer,
                                  XLMConfig, XLMForSequenceClassification,
                                  XLMTokenizer, XLNetConfig,
                                  XLNetForSequenceClassification,
                                  XLNetTokenizer)
from torch.utils.data import (DataLoader, RandomSampler, SequentialSampler,
                              TensorDataset)
import logging
logger = logging.getLogger(__name__)      
logger.setLevel(logging.INFO)   
MODEL_CLASSES = {
    'bert': (BertConfig, BertForSequenceClassification, BertTokenizer),
    'xlnet': (XLNetConfig, XLNetForSequenceClassification, XLNetTokenizer),
    'xlm': (XLMConfig, XLMForSequenceClassification, XLMTokenizer),
    'roberta': (RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer),
}


def inference_batch(dataset,batch_size=64, model=model, device=device):
    dataloader = DataLoader(dataset, batch_size=batch_size)
    model.eval()
    res = []
    for batch in dataloader:        
        batch = tuple(t.to(device) for t in batch)
        with torch.no_grad():
            inputs = {'input_ids':      batch[0],
                      'attention_mask': batch[1],
                      'token_type_ids': batch[2]}
            outputs = model.bert(**inputs)
            seq_encoding = outputs[0]
            res.append(seq_encoding)
    return res

def read_sents(file_path):
    sents = []
    with open(file_path, encoding="utf-8") as fin:
        fin.readline()
        for line in fin:
            gs = line.strip().split(',')
            sents.append(gs[0])
    return sents

def convert_features_dataset(features):
    # Convert to Tensors and build dataset
    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
    dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
    return dataset

class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids, input_mask, segment_ids):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        
def convert_sents_to_features(examples, max_seq_length,
                                 tokenizer=tokenizer,
                                 cls_token_at_end=False,
                                 cls_token='[CLS]',
                                 cls_token_segment_id=1,
                                 sep_token='[SEP]',
                                 sep_token_extra=False,
                                 pad_on_left=False,
                                 pad_token=0,
                                 pad_token_segment_id=0,
                                 sequence_a_segment_id=0, 
                                 sequence_b_segment_id=1,
                                 mask_padding_with_zero=True):
    """ Loads a data file into a list of `InputBatch`s
        `cls_token_at_end` define the location of the CLS token:
            - False (Default, BERT/XLM pattern): [CLS] + A + [SEP] + B + [SEP]
            - True (XLNet/GPT pattern): A + [SEP] + B + [SEP] + [CLS]
        `cls_token_segment_id` define the segment id associated to the CLS token (0 for BERT, 2 for XLNet)
    """

    features = []
    for (ex_index, example) in enumerate(examples):
        if ex_index % 500 == 0:
            logger.info("Writing example %d of %d" % (ex_index, len(examples)))

        tokens_a = tokenizer.tokenize(example)

        special_tokens_count = 3 if sep_token_extra else 2
        if len(example) > max_seq_length - special_tokens_count:
            tokens_a = tokens_a[:(max_seq_length - special_tokens_count)]

        tokens = tokens_a + [sep_token]
        if sep_token_extra:
            # roberta uses an extra separator b/w pairs of sentences
            tokens += [sep_token]
        segment_ids = [sequence_a_segment_id] * len(tokens)

        if cls_token_at_end:
            tokens = tokens + [cls_token]
            segment_ids = segment_ids + [cls_token_segment_id]
        else:
            tokens = [cls_token] + tokens
            segment_ids = [cls_token_segment_id] + segment_ids

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real
        # tokens are attended to.
        input_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        # Zero-pad up to the sequence length.
        padding_length = max_seq_length - len(input_ids)
        if pad_on_left:
            input_ids = ([pad_token] * padding_length) + input_ids
            input_mask = ([0 if mask_padding_with_zero else 1] * padding_length) + input_mask
            segment_ids = ([pad_token_segment_id] * padding_length) + segment_ids
        else:
            input_ids = input_ids + ([pad_token] * padding_length)
            input_mask = input_mask + ([0 if mask_padding_with_zero else 1] * padding_length)
            segment_ids = segment_ids + ([pad_token_segment_id] * padding_length)

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length

        if ex_index < 5:
            print("*** Example ***")
            print("guid: %s" % (ex_index))
            #print("tokens: %s" % " ".join(
            #        [str(x) for x in tokens]))
            print("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            print("input_mask: %s" % " ".join([str(x) for x in input_mask]))
            print("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))

        features.append(
                InputFeatures(input_ids=input_ids,
                              input_mask=input_mask,
                              segment_ids=segment_ids))
    return features

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
n_gpu = torch.cuda.device_count()
config_class, model_class, tokenizer_class = MODEL_CLASSES['bert']
model_name = "bert-base-chinese"
config = config_class.from_pretrained(model_name)
tokenizer = tokenizer_class.from_pretrained(model_name)
model = model_class.from_pretrained(model_name)
model.to(device)# setup devices

if __name__ == "__main__":


    sents = read_sents("./mingju.csv")
    print("reading sents with number: {}".format(len(sents)))
    #logger.info()
    features = convert_sents_to_features(sents, 64, tokenizer)
    """
    dataset = convert_features_dataset(features)
    res = inference_batch(model, dataset, 64, device)
    
    print(res)
    """
