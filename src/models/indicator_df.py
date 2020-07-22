from src.models.df_model import DfModel


class IndicatorDf(DfModel):
    def __init__(self, name):
        DfModel.__init__(self, name)

    def predict(self):
        pass
