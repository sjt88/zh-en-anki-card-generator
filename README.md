## Chinese <-> English Anki Card Generator

Automate Google translation & generation of Chinese/English Anki cards from a directory of mp3 files.

[logo]: example.png "Example Card"

## Motivations

Creating Anki cards is not very fun.

## Usage

1. Fill a directory with mp3 files of chinese sentences/phrases/words.
2. Make sure each file is named as per the speech:

```
files/
  你好.mp3
  我在学中文.mp3
```

3. Create a service account in the Gcloud console with read access to the translate API.
4. `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json`
5. `pipenv install`
6. `pipenv python generate_from_mp3.py path/to/files`

An anki package `output.apkg` will be created in the current directory.

5. Import the `apkg` file into Anki

Card css forked from u/TrainOfPotatoes post [here](https://www.reddit.com/r/Anki/comments/3mfmb4/consistent_replay_button_on_desktop_and_android/)
