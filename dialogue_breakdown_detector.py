from transformers import BertForSequenceClassification
from transformers import BertTokenizer
import torch
import torch.nn.functional as F


class DialogueBreakdownDetector:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased", do_lower_case=False)
        # num_labelsを1に設定
        self.model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=1)
        # 対話破綻検出のファインチューニング後のモデルを読み込み
        self.model.load_state_dict(torch.load("dbdc_bert.bin", map_location='cpu'))

    def __convert_sequences_to_features(self, user_input, candidate):
        user_candidate_tokens = []
        user_candidate_input_type_ids = []

        user_candidate_tokens.append("[CLS]")
        user_candidate_input_type_ids.append(0)

        tokens_a = self.tokenizer.tokenize(user_input)
        for token in tokens_a:
            user_candidate_tokens.append(token)
            user_candidate_input_type_ids.append(0)
        user_candidate_tokens.append("[SEP]")
        user_candidate_input_type_ids.append(0)

        tokens_b = self.tokenizer.tokenize(candidate)
        for token in tokens_b:
            user_candidate_tokens.append(token)
            user_candidate_input_type_ids.append(1)
        user_candidate_tokens.append("[SEP]")
        user_candidate_input_type_ids.append(1)

        input_ids = self.tokenizer.convert_tokens_to_ids(user_candidate_tokens)

        return [input_ids], [user_candidate_input_type_ids]

    def evaluate(self, user_input, candidate):
        with torch.no_grad():
            ids_list, type_ids_list = self.__convert_sequences_to_features(user_input, candidate)
            result = self.model.forward(torch.tensor(ids_list).to("cpu"),
                                        token_type_ids=torch.tensor(type_ids_list).to("cpu"))
            # 値をそのまま出力
            return result[0][0][0].numpy()
