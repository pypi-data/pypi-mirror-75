import pandas as pd


class Statistics(object):
    """Evaluation model indicators
    Accuracy/Precision/Recall/F1/PrecisionPolitics/RecallPolitics
    ...
    """

    def accuracy(self, df: pd.DataFrame, label_name: str = "label", predict_name: str = "predict_label") -> (
            float, str):
        """Count the accuracy of the df.
        (tp + tn) / (tp + fp + tn + fn)
        """
        a = df[df[label_name] == df[predict_name]].shape[0]
        b = df.shape[0]
        if b == 0: return (1, "缺少该类数据")
        return a / b, f"{a}/{b}"

    def precision(self, df: pd.DataFrame, label_name: str = "label", predict_name: str = "predict_label",
                  value: str = "Reject") -> (float, str):
        """Count the precision of the df.
        tp / (tp + fp)
        """
        a = df[(df[label_name] == value) & (df[predict_name] == value)].shape[0]
        b = df[df[predict_name] == value].shape[0]
        if b == 0: return (1, "缺少该类数据")
        return a / b, f"{a}/{b}"

    def recall(self, df: pd.DataFrame, label_name: str = "label", predict_name: str = "predict_label",
               value: str = "Reject") -> (float, str):
        """Count the precision of the df.
        tp / (tp + fn)
        """
        a = df[(df[label_name] == value) & (df[predict_name] == value)].shape[0]
        b = df[df[label_name] == value].shape[0]
        if b == 0: return (1, "缺少该类数据")
        return a / b, f"{a}/{b}"

    def f1(self, precision: float, recall: float) -> float:
        assert precision + recall > 0
        return 2 * precision * recall / (precision + recall)

#
# if __name__ == '__main__':
#
#
#     import pprint
#
#     we = WhisperStatistics("/home/geb/PycharmProjects/model-evaluation/test-data-standard-latest.csv",
#            "/home/geb/PycharmProjects/model-evaluation/results/yuxin/test-data-standard-latest-whisper1.1-res.txt")
#
#     # we.count_accuracy()
#     # we.count_precision()
#     # we.count_recall()
#     # we.count_precision("政治")
#     # we.count_recall("政治")
#     we.count_all()
#     pprint.pprint(we._indicator)
#
#     # df = pd.read_csv("/home/geb/PycharmProjects/model-evaluation/reports/whisper1.1.7.res-1595827993/data-for-check.csv")
#     # df["yuxin_predict"] = df["yuxin_predict"].apply(lambda x: f(x))
#
#     # print(df.head())
#     # print(ss.accuracy(df, "type", "yuxin_type", "政治"))
#     # print(ss.precision(df, "label", "yuxin_predict"))
#     # print(ss.recall(df, "label", "yuxin_predict"))
