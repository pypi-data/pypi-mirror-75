from kolibri.config import ModelConfig
from kolibri.data.cleaners.audio import AudioPreprocessor
from kolibri.dnn.tasks.audio import *
from kolibri.dnn.tasks.text import *
from kolibri.features import *
from kolibri.kolibri_component import Component
from kolibri.meta.ecoc_estimator import EcocEstimator
from kolibri.meta.ensemble_samplers import *
from kolibri.model_loader import ModelLoader
from kolibri.model_trainer import ModelTrainer
from kolibri.nlp.bigram_analyzer import BigramAnalyzer
from kolibri.tasks.classification import *
from kolibri.tokenizer import *
from kolibri.version import __version__

name = 'kolibri'

#p=Popen(["analyze", "-f /Users/mohamedmentis/Documents/Mentis/Development/Python/Deep_kolibri/kolibri/tools/freeling/config/fr_mwe.cfg","--output", "conll", "--server", "--port", "50101 &"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#time.sleep(10)
#for line in iter(p.stdout.readline,""):
#    print(line)


#"analyze -f /Users/mohamedmentis/Documents/Mentis/Development/Python/Deep_kolibri/kolibri/tools/freeling/config/en_mwe.cfg --output conll --server --port 50101 &"