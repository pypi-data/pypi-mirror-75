from itertools import groupby


def split_form_table(cldf_wordlist):
    """
    Create a list of list of ordered dictionaries, grouped by Language_ID, where each CLDF
    row is mapped to an individual entry.

    Example:  OrderedDict([('ID', 'amar1273-1-1'), ('Parameter_ID', '1'), ...])
    """
    return [
        list(f2)
        for f1, f2 in groupby(
            sorted(cldf_wordlist["FormTable"], key=lambda f1: (f1["Language_ID"])),
            lambda f1: (f1["Language_ID"]),
        )
    ]


def make_index_link(s):
    stripped = s.split("raw/")[-1]
    stripped_link = s.split("raw/")[-1].replace(" ", "%20")
    return "* [{0}]({1})".format(stripped, stripped_link)


def make_chan_link(s, url):
    s = s.replace(" ", "%20")
    url = url + s
    return " ([Source]({0}))".format(url)


def check_for_problems(entry):
    for row in entry:
        if row["Problematic"] is True:
            return " **(Problems)**"

    return ""


def make_language_name(language_name=""):
    if language_name:
        return " ({0})".format(language_name)
    else:
        return ""


def int_to_en(num):
    """
    This is taken from https://stackoverflow.com/a/32640407 and slightly modified.
    :param num: int32 integer.
    :return: English version of num.
    """
    int_to_english = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
        16: "sixteen",
        17: "seventeen",
        18: "eighteen",
        19: "nineteen",
        20: "twenty",
        30: "thirty",
        40: "forty",
        50: "fifty",
        60: "sixty",
        70: "seventy",
        80: "eighty",
        90: "ninety",
    }

    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert 0 <= num

    if int(num) != num:
        return 'problem'  # pragma: no cover

    if num < 20:
        return int_to_english[num]

    if num < 100:
        if num % 10 == 0:
            return int_to_english[num]
        else:
            return int_to_english[num // 10 * 10] + " " + int_to_english[num % 10]

    if num < k:
        if num % 100 == 0:
            if num // 100 == 1:
                return "hundred"
            return int_to_english[num // 100] + " hundred"
        else:
            return int_to_english[num // 100] + " hundred and " + int_to_en(num % 100)

    if num < m:
        if num % k == 0:
            if num // k == 1:
                return "thousand"
            return int_to_en(num // k) + " thousand"
        else:
            return int_to_en(num // k) + " thousand, " + int_to_en(num % k)

    if num < b:
        if (num % m) == 0:
            if num // m == 1:
                return "million"
            return int_to_en(num // m) + " million"
        else:
            return int_to_en(num // m) + " million, " + int_to_en(num % m)

    if num < t:
        if (num % b) == 0:
            return int_to_en(num // b) + " billion"
        else:
            return int_to_en(num // b) + " billion, " + int_to_en(num % b)

    if num % t == 0:
        return int_to_en(num // t) + " trillion"
    else:
        return int_to_en(num // t) + " trillion, " + int_to_en(num % t)


# Largest Glottolog families for sorting:
FAMILIES = [
    "Austronesian",
    "Atlantic-Congo",
    "Sino-Tibetan",
    "Indo-European",
    "Afro-Asiatic",
    "Nuclear Trans New Guinea",
    "Austroasiatic",
    "Tupian",
    "Tai-Kadai",
    "Mande",
    "Pama-Nyungan",
    "Dravidian",
    "Otomanguean",
    "Nilotic",
    "Turkic",
    "Uralic",
    "Central Sudanic",
    "Arawakan",
    "Nakh-Daghestanian",
    "Pano-Tacanan",
    "Uto-Aztecan",
    "Salishan",
    "Algic",
    "Cariban",
]
