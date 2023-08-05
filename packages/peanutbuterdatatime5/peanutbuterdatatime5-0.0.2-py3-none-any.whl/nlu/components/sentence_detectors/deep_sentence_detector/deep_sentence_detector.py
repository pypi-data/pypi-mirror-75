import nlu.pipe_components
import sparknlp
from sparknlp.base import *
from sparknlp.annotator import *

class DeepSentenceDetector:
    @staticmethod
    def get_default_model():
        return DeepSentenceDetector() \
            .setInputCols(["document"]) \
            .setOutputCol("sentence")



