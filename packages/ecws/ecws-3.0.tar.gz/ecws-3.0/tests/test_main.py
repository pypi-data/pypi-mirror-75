from ecws.main import Segmenter

# def test_main_function():
path = '/Users/abel/Desktop/work/sg-cws/NLP-ECWS-R3.0/result.bert/model.tar.gz'
vocab_path = "/Users/abel/Desktop/work/sg-cws/NLP-ECWS-R3.0/bert-model/transformers-BertForPreTraining"
segmenter = Segmenter(path, vocab_path)
sent = '我爱北京天安门'
output = segmenter.seg(sent)
