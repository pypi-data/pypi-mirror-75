import sparknlp

class RegexMatcher:
    @staticmethod
    def get_default_model():
        return   sparknlp.annotator.TextMatcherModel.pretrained() \
            .setInputCols("document") \
            .setOutputCol("entity") \


    @staticmethod
    def get_pretrained_model(name, language):
        return   sparknlp.annotator.TextMatcherModel.pretrained(name,language) \
            .setInputCols("document") \
            .setOutputCol("entity") \


