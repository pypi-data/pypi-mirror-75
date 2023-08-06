from whisper_evaluate import Statistics
import numpy as np
import pandas as pd
from whisper_evaluate.config import en_zh


class WhisperStatistics(Statistics):

    def __init__(self, standard_file: str, result_file: str):
        self.df, self.df_no_trie, self.df_trie = None, None, None
        self.parse_standard_and_result(standard_file, result_file)
        self.indicator = {
            "no_trie": {
                "accuracy": tuple(),
                "recall": {},
                "precision": {},
                "f1": {},
            },
            "trie": {
                "accuracy": tuple(),
                "recall": {},
                "precision": {},
                "f1": {},
            }
        }

    def count_accuracy(self):
        self.indicator["no_trie"]["accuracy"] = self.accuracy(self.df_no_trie, "label", "predict_label")
        self.indicator["trie"]["accuracy"] = self.accuracy(self.df_trie, "label", "predict_label")

    def count_recall(self, mode: str = "整体"):
        if mode == "整体":
            self.indicator["no_trie"]["recall"]["整体"] = self.recall(self.df_no_trie)
            self.indicator["trie"]["recall"]["整体"] = self.recall(self.df_trie)
        else:
            self.indicator["no_trie"]["recall"][mode] = self.recall(self.df_no_trie, "type", "predict_type", mode)
            self.indicator["trie"]["recall"][mode] = self.recall(self.df_trie, "type", "predict_type", mode)

    def count_precision(self, mode: str = "整体"):
        if mode == "整体":
            self.indicator["no_trie"]["precision"]["整体"] = self.precision(self.df_no_trie, "label", "predict_label")
            self.indicator["trie"]["precision"]["整体"] = self.precision(self.df_trie, "label", "predict_label")
        else:
            self.indicator["no_trie"]["precision"][mode] = self.precision(self.df_no_trie, "type", "predict_type",
                                                                          mode)
            self.indicator["trie"]["precision"][mode] = self.precision(self.df_trie, "type", "predict_type", mode)

    def parse_standard_and_result(self, standard_file: str, result_file: str):
        standard_df = pd.read_csv(standard_file)
        standard_df.columns = ["example", "label", "type"]
        result = []
        with open(result_file, 'r', encoding='utf-8') as f:
            for line in f:
                a = eval(line)
                results = a['results'][0]
                _match_words = results['matched_words']
                _new_words = results['new_words']
                _review_words = results['review_words']
                predict_type = self._get_result_type(_match_words + _new_words)
                predict_label = "Pass" if predict_type == "其他" else "Reject"
                predict_type_trie = "政治" if self._get_result_type(_review_words) == "政治" else predict_type
                predict_label_trie = "Pass" if predict_type_trie == "其他" else "Reject"
                result.append([predict_label, predict_type, predict_label_trie, predict_type_trie,
                               " ".join([x["word"] for x in _match_words]), " ".join([x["word"] for x in _new_words]),
                               " ".join([x["word"] for x in _review_words])])
        result = np.array(result)
        standard_df["predict_label"] = pd.Series(result[:, 0])
        standard_df["predict_type"] = pd.Series(result[:, 1])
        standard_df["predict_label_trie"] = pd.Series(result[:, 2])
        standard_df["predict_type_trie"] = pd.Series(result[:, 3])
        standard_df["match_words"] = pd.Series(result[:, 4])
        standard_df["new_words"] = pd.Series(result[:, 5])
        standard_df["review_words"] = pd.Series(result[:, 6])
        self.df = standard_df
        self.df_no_trie = standard_df[["example", "label", "type", "predict_label", "predict_type"]]
        self.df_trie = standard_df[["example", "label", "type", "predict_label_trie", "predict_type_trie"]]
        self.df_trie.columns = ["example", "label", "type", "predict_label", "predict_type"]

    def __count_f1(self):
        for category in self.indicator["no_trie"]["precision"]:
            self.indicator["no_trie"]["f1"][category] = self.f1(self.indicator["no_trie"]["precision"][category][0],
                                                                self.indicator["no_trie"]["recall"][category][0])
            self.indicator["trie"]["f1"][category] = self.f1(self.indicator["trie"]["precision"][category][0],
                                                             self.indicator["trie"]["recall"][category][0])

    def count_all(self, other_type: list = []):
        self.count_accuracy()
        for _type in ["整体", "政治"] + other_type:
            self.count_recall(_type)
            self.count_precision(_type)
        self.__count_f1()

    def _get_result_type(self, words: list):
        tag_set = set()
        if not words:
            return "其他"
        for element in words:
            tag_set.add(element["type"])
        if "Politics" in tag_set:
            return en_zh["Politics"]
        if "Heresy" in tag_set:
            return en_zh["Heresy"]
        if "Terrorism" in tag_set:
            return en_zh["Terrorism"]
        if "Crime" in tag_set:
            return en_zh["Crime"]
        if "Porn" in tag_set:
            return en_zh["Porn"]
        if "Gamble" in tag_set:
            return en_zh["Gamble"]
        if "Contraband" in tag_set:
            return en_zh["Contraband"]
        if "SensitiveEvent" in tag_set:
            return en_zh["SensitiveEvent"]
        if "Abuse" in tag_set:
            return en_zh["Abuse"]
        if "IllegalWebsite" in tag_set:
            return en_zh["IllegalWebsite"]
        if "Adv" in tag_set:
            return en_zh["Adv"]
        return en_zh["Normal"]
