import time
import logging
import multiprocessing
from pathlib import Path
from memorization.gpt_api import sentence_generator
from django.core.management.base import BaseCommand
from memorization.utils import standardize_text
from word.models import Terms, Word
from logging.handlers import RotatingFileHandler
from tinydb import TinyDB, Query
from BetterJSONStorage import BetterJSONStorage
from django import db as django_db


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_file = 'logs.log'
max_bytes = 2097152  # 2 MB
backup_count = 1  # número de arquivos de backup
file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


path = Path('sentences_examples_chatgpt.json')
db = TinyDB(
    path,
    access_mode="r+",
    storage=BetterJSONStorage
)


COLORS = {
        'noun': '#2980b9',
        'verb': '#27ae60',
        'adjective': '#e74c3c'
    }
GRAMMATICAL_CLASSES = ('adjective','noun', 'verb')


def main(sentence_obj):    
    SETENCES = {}
    _identify_part_of_speech(sentence_obj)
    
    objects_available_for_update = db.search(Query().obj_id == str(sentence_obj.get('id')))
    SETENCES[str(sentence_obj.get('id'))] = standardize_text(sentence_obj.get('text'))
        
    _setup(objects_available_for_update, SETENCES)
    _to_save(SETENCES)


def _identify_part_of_speech(sentence_obj):
    sentence = standardize_text(sentence_obj.get('text'))
    sentence_obj_id = str(sentence_obj.get('id'))

    _dictionary_parts_of_speech = _separating_text_by_grammatical_class(sentence, sentence_obj_id)
    for item in _dictionary_parts_of_speech:
        parts_of_speech = list(item.keys())[0]
        word = list(item.values())[0]
        _definition = ''

        if Word.objects.filter(name=word).exists():
            token = Word.objects.filter(name=word).last()
            _definition = token.definition
            logger.info(f'_sentence_generator_already_registered_database: {token.id}')
        
        _sentence_generator(parts_of_speech, word, _definition, sentence_obj_id)


def _separating_text_by_grammatical_class(sentence, sentence_obj_id):
    try:
        container = []
        request = f"""
            Act as an English grammar teacher and separate the text based on its parts of speech "{sentence}" return the response in csv format no header, return only the following structure:
            word, part of speech written in full
            ...
            ...
        """
        result = sentence_generator(request)
        logger.info(f'_separating_text_by_grammatical_class: {sentence_obj_id} => {result}')
        if not result:
            return container

        for elem in str(result).splitlines():
            if ',' in elem and len(elem) < 30:
                data = elem.lower().split(',')
                container.append({data[1].strip(): data[0].strip()})
        
        return container
    except Exception as exp:
        logger.warning(f'_separating_text_by_grammatical_class__error: {sentence_obj_id} => {exp}')
        return container


def _sentence_generator(parts_of_speech, word, _definition, sentence_obj_id):
    try:
        if parts_of_speech in GRAMMATICAL_CLASSES and _definition == '':
            request = f'Atue como um dicionário e responda qual a definição em português brasil da palavra {word} Seja sucinto e retorne apenas o foi solicitado.'
            _definition = sentence_generator(request)
            if not _definition:
                return
            logger.info(f'_sentence_generator_gpt: {sentence_obj_id} => {_definition}')

        data = {
            'obj_id': sentence_obj_id, 
            'text': word, 
            'class': parts_of_speech, 
            'color': COLORS.get(parts_of_speech), 
            'definition': str(_definition),
            'updated_in_the_database': False
        }
        db.insert(data)    
    except Exception as exp:
        logger.warning(f'_sentence_generator__exp: {sentence_obj_id} => {exp}')


def _setup(objects_available_for_update, SETENCES):
    _payload = {}

    for elem in objects_available_for_update:

        try:
            word = elem.get('text')
            _id = elem.get('obj_id')
            if not _id in _payload:
                _payload[_id] = {}

            _payload[_id].update({f'{word}':f'{word}'})

            if elem.get('class') in GRAMMATICAL_CLASSES:
                obj = Word.objects.filter(name=elem.get('text')).last()
                if obj == None:
                    try:
                        obj = Word.objects.create(
                            **{'name': str(elem.get('text')), 
                            'definition': elem.get('definition'), 
                            'part_of_speech': elem.get('class')}
                        )
                    except Exception as exp:
                        obj = Word.objects.filter(name=elem.get('text')).last()

                color = elem.get('color')
                url = f"http://localhost:8000/admin/word/word/{obj.id}/change/"
                html = f"<a href='{url}' target='_blank'><span style='color:{color}'>{word}</span></a>"
                _payload[_id].update({f'{word}':f'{html}'})
            
        except Exception as exp:
            logger.error(f'setup__error: {elem.get("obj_id")} -> {exp} -> {objects_available_for_update}')
            break
        
    for setence in SETENCES:
        try:
            _transformed_sentences = []
            for word in SETENCES[setence].split():        
                _transformed_sentences.append(_payload[setence][word]) if word in _payload.get(setence) else _transformed_sentences.append(word)

            _result = ' '.join(_transformed_sentences)
            SETENCES[setence] = _result
        except Exception as exp:
            logger.error(f'setup__error_2: {setence} -> {exp}')
            break


def _to_save(SETENCES):
    for item in SETENCES:
        try:
            instance = Terms.objects.get(id=item)
            instance.text = SETENCES[item]
            instance.save()
            db.update({'updated_in_the_database': True}, Query().obj_id == item)
            logger.info(f'to_save: {instance.id}')
        except Exception as exp:
            logger.warning(f'to_save__error: {item} -> {exp}')


class Command(BaseCommand):
    help = "OK"
    
    def add_arguments(self, parser):
        parser.add_argument('--qtd', default=0, type=int)

    def handle(self, *args, **options): 
        start_time = time.time()

        amount = options.get('qtd')        
        sentences_already_processed = list(set(elem.get('obj_id') for elem in db.search(Query().updated_in_the_database == True)))

        queryset = Terms.objects.all().exclude(id__in=sentences_already_processed).order_by('-created_at').values('id', 'text')[0:amount]
        _queryset_handled = list(queryset)
        
        # print(multiprocessing.cpu_count())
        django_db.connections.close_all()

        with multiprocessing.Pool(processes=2) as pool:
            pool.map(main, _queryset_handled)

        logger.info(f'Time taken: {time.time() - start_time} seconds')