import re
from collections import Counter
import nltk
from unidecode import unidecode

stopwords = set(nltk.corpus.stopwords.words("portuguese"))
stemmer = nltk.stem.RSLPStemmer()

class BaseTransformerText:
    def transform(self, text):
        pass

    def __call__(self, text=""):
        if isinstance(text, list):
            outputs = []

            for t in text:
                if not isinstance(t, str):
                    raise Exception(
                        f"{self.__class__.__name__}:Todos os elementos da lista devem ser do tipo string. Recebido: {type(t)}"
                    )
                outputs.append(self.transform(t))

            return outputs
        raise Exception(
            f"{self.__class__.__name__}:Como entrada, deve ser fornecida uma lista com os textos a serem transformados"
        )


class BaseTransformerList:
    def transform(self, tokens):
        pass

    def __call__(self, text):
        if isinstance(text, list):
            outputs = []

            for t in text:
                if not isinstance(t, list):
                    raise Exception(
                        f"{self.__class__.__name__}:Cada texto deve ser informado como uma lista de tokens para essa transformação."
                    )
                for token in t:
                    if not isinstance(token, str):
                        raise Exception(
                            f"{self.__class__.__name__}:Todo token deve ser uma string. Recebido: type(token)"
                        )

                outputs.append(self.transform(list(t)))

            return outputs

        raise Exception(
            "Como entrada, deve ser fornecida uma lista com os tokens a serem transformados"
        )


class BaseReplacerText:
    def replace(self, text, replaces):
        pass

    def __call__(self, text, replaces=None):
        print(replaces)
        if not isinstance(replaces, dict):
            raise Exception(
                f"{self.__class__.__name__}: Como entrada, deve ser fornecido um dicionário das substituições. Recebido: {type(replaces)}"
            )

        if isinstance(text, list):
            outputs = []

            for t in text:
                if not isinstance(t, str):
                    raise Exception(
                        f"{self.__class__.__name__}: Todos os elementos da listniza devem ser do tipo string. Recebido: {type(t)}"
                    )

                outputs.append(self.replace(t, replaces))

            return outputs
        raise Exception(
            f"{self.__class__.__name__}:Como entrada, deve ser fornecida uma lista com os textos a serem transformados"
        )


class RemoveAccent(BaseTransformerText):
    def transform(self, text):
        return unidecode(text)


class Lower(BaseTransformerText):
    def transform(self, text):
        return text.lower()


class Upper(BaseTransformerText):
    def transform(self, text):
        return text.upper()


class Capitalize(BaseTransformerText):
    def transform(self, text):
        return text.title()


class RemoveNumber(BaseTransformerText):
    def transform(self, text):
        return re.sub(r"[\d]+[\d\,\.\-\(\) \/:ºª\%]*", " __NUM__ ", text)


class RemoveURL(BaseTransformerText):
    def transform(self, text):
        return re.sub(
            r"(https?:\/\/(?:www\d?\.|(?!www\d?))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\d?\."
            r"[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\d?\.|(?!www\d?))[a-zA-Z0-9]"
            r"+\.[^\s]{2,}|www\d?\.[a-zA-Z0-9]+\.[^\s]{2,})",
            " __URL__ ",
            text,
        )


class RemoveEmail(BaseTransformerText):
    def transform(self, text):
        return re.sub(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", " __EMAIL__ ", text
        )


class JustWords(BaseTransformerText):
    def transform(self, text):
        text = re.sub(r"[\W\n]", " ", text)
        return re.sub(r"[ ]{2,}", " ", text).strip()


class Tokenize(BaseTransformerText):
    def transform(self, text):
        return nltk.word_tokenize(text)


class LeiReplace(BaseTransformerText):
    def transform(self, text):
        text = re.sub(
            r"leis(\s+\d{1,10}\W?\d{1,10}?\/\d{1,4}[,](\s+\d{1,10}\W?\d{1,10}?\/\d{1,4})*)|lei(\s+\d{1,10}\W?\d{1,10}?\/\d{1,4}[,](\s+\d{1,10}\W?\d{1,10}?\/\d{1,4})*)",  # NOQA pylint: disable=C0301
            repl_art_lei_aninhado,
            text,
        )
        return re.sub(r"lei\s+\d{1,10}\W?\d{1,10}?\/\d{1,4}", repl_art_lei, text)


class ArtReplace(BaseTransformerText):
    def transform(self, text):
        text = re.sub(
            r"artigo(\s+\d{1,10}[,](\s+\d{1,10}[,])*)|artigos(\s+\d{1,10}[,](\s+\d{1,10}[,])*)|art.(\s+\d{1,10}\[,](\s+\d{1,10}\S+)*)",
            repl_art_lei_aninhado,
            text,
        )
        return re.sub(
            r"art\W+?\s+\d{1,10}|art\s+\d{1,10}|artigo\s+\d{1,10}", repl_art_lei, text,
        )


class IncisoReplace(BaseTransformerText):
    def transform(self, text):
        return re.sub(r"inciso\s+\w+", repl_inciso, text)


class ParagrafoReplace(BaseTransformerText):
    def transform(self, text):
        text = re.sub(r"º", "", text)
        return re.sub(r"§\s+\d+", repl_paragrafo, text)


class Replace(BaseReplacerText):
    def replace(self, text, replaces):
        for pattern in replaces:
            repl = replaces[pattern]
            text = re.sub(pattern, repl, text)
        return text


class RemoveStopwords(BaseTransformerList):
    def transform(self, tokens):
        return [t for t in tokens if t.lower() not in stopwords]


class JoinTokens(BaseTransformerList):
    def transform(self, tokens):
        return " ".join(tokens)


class Stemming(BaseTransformerList):
    def transform(self, tokens):
        return [stemmer.stem(token) for token in tokens]


class Bigram(BaseTransformerList):
    def transform(self, tokens):
        return list(nltk.ngrams(tokens, 2))


class Trigram(BaseTransformerList):
    def transform(self, tokens):
        return list(nltk.ngrams(tokens, 3))


class TokenCounter(BaseTransformerList):
    def transform(self, tokens):
        counter = Counter(tokens)
        data = list(counter.most_common())
        return data


class Pipeline:
    def __call__(self, text=None, transforms=None, replaces=None):
        outputs = list(text)

        for t in transforms:
            transformer = TRANSFORMS[t]

            results = []
            for out in outputs:
                if t == "replace":
                    results += transformer([out], replaces)
                else:
                    results += transformer([out])

            outputs = results

        return outputs


def repl_inciso(match):
    str1 = match.group(0).strip()
    str_f = re.sub(r" ", "_", str1)
    return f" {str_f} "


def repl_paragrafo(match):
    str1 = match.group(0).strip()
    lst_str = str1.split()
    str2 = None
    try:
        str2 = num_to_letters(lst_str[1])
    except BaseException:
        pass
    str_f = str2 if str2 else lst_str[1]
    str_f = r" {}_{} ".format("paragrafo", str_f)
    return str_f


def repl_art_lei(match):
    s = match.group(0).strip()
    s = re.sub(r"[.|:|;]", "", s)
    s = re.sub(r"\s", "_", s)
    s = re.sub(r"\/", "", s)
    str1 = re.findall(r"\D+", s)[0]
    str2 = num_to_letters(re.findall(r"\d+", s)[0])

    return r" {}{} ".format(str1, str2)


def repl_art_lei_aninhado(match):
    s = match.group(0).strip()
    s = re.sub(r"[.,:]", "", s)
    s = re.sub(r"s", "", s)
    s = s.split()
    s = " ".join(list(map(lambda x: r"{} {}".format(s[0], x), s[1:])))
    return s


def num_to_letters(word):
    mapping = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h",
        8: "i",
        9: "j",
    }
    return "".join(list(map(lambda x: mapping.get(int(x), x), list(word))))


TRANSFORMS = {
    "capitalize": Capitalize(),
    "bi-gram": Bigram(),
    "tri-gram": Trigram(),
    "join-tokens": JoinTokens(),
    "just-words": JustWords(),
    "lower": Lower(),
    "remove-accents": RemoveAccent(),
    "remove-emails": RemoveEmail(),
    "remove-numbers": RemoveNumber(),
    "remove-stopwords": RemoveStopwords(),
    "remove-urls": RemoveURL(),
    "steamming": Stemming(),
    "tokenize": Tokenize(),
    "token-counter": TokenCounter(),
    "upper": Upper(),
    "replace-lei": LeiReplace(),
    "replace-art": ArtReplace(),
    "replace-inciso": IncisoReplace(),
    "replace-paragrafo": ParagrafoReplace(),
    "replace": Replace(),
}
