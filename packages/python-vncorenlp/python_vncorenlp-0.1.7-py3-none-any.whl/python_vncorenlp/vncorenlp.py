import os
import sys
from argparse import Namespace
from functools import lru_cache
from typing import *

from . import protocols

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
CLASS_PATH = os.path.join(DATA_DIR, 'vncorenlp.jar')
MODEL_DIR = os.path.join(DATA_DIR, 'models')

VOCAB = 'vocab'
SEGMENTER = 'wordsegmenter.rdr'
TAGGER = 'postagger'
CLUSTER = 'clusters.xz'
EMBEDDING = 'embeddings.xz'
NER = 'ner.xz'
DEP = 'dep.xz'


class Token(NamedTuple):
    text:str
    pos:Optional[str]
    ner:Optional[str]
    dep:Optional[str]


Sentence = List[Token]
Doc = List[Sentence]


def install(*options, jar_path:str=CLASS_PATH):
    if not os.path.exists(MODEL_DIR):
        import urllib.request
        from io import BytesIO
        from zipfile import ZipFile

        url = 'https://github.com/NgHoangDat/python_vncorenlp/raw/master/python_vncorenlp/data/models.zip'
        response = urllib.request.urlopen(url)
        data = BytesIO(response.read())
        with ZipFile(data) as f:
            f.extractall(DATA_DIR)
        
    import jnius_config

    for option in options:
        jnius_config.add_options(option)

    jnius_config.set_classpath(jar_path)


@lru_cache(maxsize=1)
def load_class() -> Namespace:
    from jnius import autoclass

    return Namespace(
        ArrayList=autoclass('java.util.ArrayList'),
        Vocabulary=autoclass('vn.corenlp.wordsegmenter.Vocabulary'),
        LexicalInitializer=autoclass('vn.pipeline.LexicalInitializer'),
        WordSegmenter=autoclass('vn.corenlp.wordsegmenter.WordSegmenter'),
        PosTagger=autoclass('vn.corenlp.postagger.PosTagger'),
        NerRecognizer=autoclass('vn.corenlp.ner.NerRecognizer'),
        DependencyParser=autoclass('vn.corenlp.parser.DependencyParser'),
        VnCoreNLP=autoclass('vn.pipeline.VnCoreNLP')
    )


class Pipeline:

    def __init__(self):
        self.instance:Optional[protocols.VnCoreNLP] = None

    def load_model(self, model_dir:str=MODEL_DIR, use_segmenter:bool=True, use_postagger:bool=False, use_ner:bool=False, use_dep:bool=False):
        vocab = None
        segmenter = None
        tagger = None
        cluster = None
        embedding = None
        ner = None
        dep = None

        if use_segmenter:
            vocab = VOCAB
            segmenter = SEGMENTER

        if use_postagger:
            tagger = TAGGER
        
        if use_ner or use_dep:
            cluster = CLUSTER
            embedding = EMBEDDING

        if use_ner:
            ner = NER

        if use_dep:
            dep = DEP

        self.load_custom(model_dir, vocab, segmenter, tagger, cluster, embedding, ner, dep)


    def load_custom(self, model_dir:str, 
            vocab:Optional[str]=None, segmenter:Optional[str]=None, 
            tagger:Optional[str]=None, 
            cluster:Optional[str]=None, embedding:Optional[str]=None, 
            ner:Optional[str]=None, dep:Optional[str]=None
        ):

        package = load_class()
        self.instance = package.VnCoreNLP()

        if segmenter:
            assert vocab, 'Segmenter need vocab to work'
            vocabulary = package.Vocabulary(os.path.join(model_dir, vocab))
            segmenter = package.WordSegmenter(os.path.join(model_dir, segmenter), vocabulary)
            self.instance.setWordSegmenter(segmenter)

        if tagger:
            pos_tagger = package.PosTagger(os.path.join(model_dir, tagger))
            self.instance.setPosTagger(pos_tagger)

        lexica = None
        if cluster and embedding:
            lexica = package.LexicalInitializer(
                os.path.join(model_dir, cluster),
                os.path.join(model_dir, embedding)
            ).initializeLexica()

        if ner:
            assert lexica, 'Ner need cluster and embedding to work'
            ner_recognizer = package.NerRecognizer(os.path.join(model_dir, ner), lexica)
            self.instance.setNerRecognizer(ner_recognizer)

        if dep:
            assert lexica, 'Ner need cluster and embedding to work'
            dep_parser = package.DependencyParser(os.path.join(model_dir, dep), lexica)
            self.instance.setDependencyParser(dep_parser)

    @lru_cache(maxsize=256)
    def annotate_doc(self, doc:str) -> Doc:
        doc = self.instance.annotateDoc(doc)
        return [
            [
                Token(word.getForm(), word.getPosTag(), word.getNerLabel(), word.getDepLabel())
                for word in sentence
            ] for sentence in doc
        ]

    @lru_cache(maxsize=256)
    def __annotate_docs(self, docs:Tuple[str, ...]) -> List[Doc]:
        package = load_class()
        docs_array = package.ArrayList()
        for doc in docs:
            docs_array.add(doc)

        docs = self.instance.annotateDocs(docs_array)
        return [
            [
                [
                    Token(word.getForm(), word.getPosTag(), word.getNerLabel(), word.getDepLabel())
                    for word in sentence
                ] for sentence in doc
            ] for doc in docs
        ]

    def annotate_docs(self, docs:Sequence[str]) -> List[Doc]:
        return self.__annotate_docs(tuple(docs))
