from ..fr.tokenizer import FrMemorizingTokenizer
from pie_extended.pipeline.iterators.proto import DataIterator
from pie_extended.pipeline.postprocessor.proto import ProcessorPrototype
from pie_extended.pipeline.postprocessor.memory import MemoryzingProcessor


def get_iterator_and_processor():
    tokenizer = FrMemorizingTokenizer()
    processor = MemoryzingProcessor(
        tokenizer_memory=tokenizer,
        head_processor=ProcessorPrototype()
    )

    iterator = DataIterator(
        tokenizer=tokenizer
    )
    return iterator, processor

