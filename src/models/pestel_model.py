from src.controller.pestel_controller import get_indicators, table_to_google


class Pestel_category_model:
    def __init__(self, name):
        self.name: str = name

    def get_indicators(self):
        return get_indicators(self.name)

    def construct_google_data(self):
        return table_to_google(self.name)

