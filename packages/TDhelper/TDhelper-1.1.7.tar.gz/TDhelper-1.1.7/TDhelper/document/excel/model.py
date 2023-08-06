from TDhelper.document.excel.meta.modelMeta import modelMeta
class model(metaclass=modelMeta):
    __excelHandle__= None
    __sheetHandle__= None
    def __init__(self,filePath=''):
        self.Meta.file= filePath
        self.__initExcelHandle__()

    def __initExcelHandle__(self):
        return None

    def __enter__(self):
        return self

    def readLine(self, lineOffset=1):
        return True

    def close(self):
        return None
    
    class Meta:
        file= ''
        sheet= 'sheet1'