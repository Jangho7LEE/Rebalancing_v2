from MyQuant.lib.DataManager import DataManager

class Quant(DataManager):
    def __init__(self, base_path = "./data") -> None:
        super().__init__(base_path)

    from MyQuant.lib.DartXML import corp_code_to_stock