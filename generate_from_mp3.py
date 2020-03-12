from google.cloud import translate_v2 as translate
from genanki import Deck, Model, Note, Package
from os import listdir
from os.path import join, splitext
from argparse import ArgumentParser
from pypinyin import pinyin

translate_client = translate.Client()


def hanzi_english_model(deck_name):
    zh_front = open('assets/zh_front.html', 'r').read()
    zh_back = open('assets/zh_back.html', 'r').read()
    en_front = open('assets/en_front.html', 'r').read()
    en_back = open('assets/en_back.html', 'r').read()
    css = open('assets/styles.css', 'r').read()

    return Model(
        1607392319,
        'Hanzi <-> English',
        fields=[
            {'name': 'Hanzi'},
            {'name': 'Pinyin'},
            {'name': 'English'},
            {'name': 'Audio'},
        ],
        css=css,
        templates=[
            {
                'name': 'Hanzi -> English',
                'qfmt': zh_front,
                'afmt': zh_back,
            },
            {
                'name': 'English -> Hanzi',
                'qfmt': en_front,
                'afmt': en_back,
            },
        ])


def create_note(filename, model):
    hanzi = splitext(filename)[0]
    translation_result = translate_client.translate(
        hanzi, target_language='en')
    english_text = translation_result['translatedText']
    audio_text = '[sound:' + hanzi + '.mp3]'
    pinyin_text = ' '.join([' '.join(phrase) for phrase in pinyin(hanzi)])
    return Note(
        model=model,
        fields=[hanzi, pinyin_text, english_text, audio_text])


def add_notes(audio_files, model, deck):
    for filename in audio_files:
        note = create_note(filename=filename, model=model)
        deck.add_note(note)
    return deck


def generate(deck_name, audio_dir):
    audio_files = listdir(audio_dir)
    model = hanzi_english_model(deck_name)
    deck = Deck(
        2059400110,
        'Chinese Deck')
    deck = add_notes(audio_files=audio_files, model=model, deck=deck)
    package = Package(deck)
    full_paths = [join(audio_dir, filename)
                  for filename in audio_files]
    write_package(package=package, audio_files=full_paths)


def write_package(package, audio_files):
    package.media_files = audio_files
    package.write_to_file('output.apkg')


def parse_arguments():
    parser = ArgumentParser(
        description='Generate Anki deck from audio files')
    parser.add_argument('audio_dir')
    parser.add_argument('--deck_name')
    args = parser.parse_args()

    return args


def run():
    args = parse_arguments()
    deck_name = args.deck_name if args.deck_name else 'Chinese Dictionary'
    generate(deck_name=deck_name,
             audio_dir=args.audio_dir)


run()
