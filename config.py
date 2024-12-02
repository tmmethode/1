# from googletrans import Translator  # type: ignore
import pandas as pd  # type: ignore
import data

CONFIG = {
    # 'scrollZoom': False,
    # 'editable': False,
    # 'showLink': False,
    'displaylogo': False,
}

# Languages dataset
LANG = pd.read_csv("lang/en_fr_rw .csv")

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-top": "0",
    "margin-right": "1rem",
    "padding": "0",
    "background-color": "#DCDCDC",
    "padding-top": "0.5rem",
}


def translate(text: str, to: str = "en") -> str:
    if to == data.CURRENT_LANG or text not in LANG[data.CURRENT_LANG].values:
        return text

    translated_text = LANG[LANG[data.CURRENT_LANG] == text][to].values[0]  # type: ignore # noqa  
    return translated_text

# def translate_text(text_to_translate: str) -> str:
#     try:
#         if text_to_translate and LANG != "rw":
#             translator = Translator()
#             translated = translator.translate(text_to_translate, dest=LANG)
#             return translated.text
#         return text_to_translate
#     except KeyError:
#         return text_to_translate
