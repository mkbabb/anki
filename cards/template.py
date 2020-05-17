import re
import textwrap
from typing import Any, Callable, Dict, List, Tuple, Union, Optional

astre = re.compile(r"\* (.*?)\*")
tabre = re.compile(r"\n")

NEW_LINE = "\n"
TAB = "\t"


def parse_class(tag):
    t_list = tag.split(".")
    t = t_list.pop(0)
    return f'''{str(t).strip().lower()}''' +\
        f'''class="{" ".join(map(lambda x: str(x).strip().lower(), t_list))}"'''


def tag_elm(tags: List[str], content: Optional[str] = None):
    if(content is None):
        new_line = ""
        content = ""
    else:
        new_line = NEW_LINE

    content = content\
        if content.find("\n") == -1\
        else re.sub(tabre, "\n" + "\t" * len(tags), content)
    content = TAB * len(tags) + content

    start = "".join(f'''{TAB*n}<{i[0]} {i[1]}>{new_line}'''
                    for n, i in enumerate(tags))\
        if not isinstance(tags[0][1], list)\
        else "".join(f'''{TAB*n}<{i[0]} {" ".join(i[1])}>{new_line}'''
                     for n, i in enumerate(tags))
    return start + content +\
        "".join(
            f'''{new_line}{TAB*(len(tags) - (n + 1))}</{i[0]}>'''
            for n, i in enumerate(tags[::-1]))


def replace_map(s: str,
                regex: Any,
                func: Callable[[str], str]) -> str:
    t = [s]

    def wrapper(match):
        for i in range(1, regex.groups + 1):
            t[0] = t[0].replace(match.group(0), func(match.group(i)))
        return t[0]
    u = list(map(lambda x: wrapper(x), re.finditer(regex, s)))
    return s if not len(u) else u[-1]


def erm(match):
    return tag_elm([["em", ""]], match)


def create_def_template(def_object: dict) -> List[str]:
    words: List[str] = []

    for word, definition in def_object.items():
        defs: List[str] = [tag_elm([["div", 'class="def-block"'],
                                    ["h2", 'class="def-title"']],
                                   f"{word.strip().lower()}"),
                           tag_elm([["div", 'class="line-top"']])]
        n = 0
        for i, j in definition.items():
            block = ""
            k = 0
            while (k < len(j) - 1):
                d = replace_map("<br>".join(textwrap.wrap(j[k]))
                                .strip()
                                .lower(),
                                astre, erm)\
                    .replace(word, f"<b>{word}</b>")
                e = replace_map("<br>".join(textwrap.wrap(j[k + 1]))
                                .strip()
                                .lower(),
                                astre, erm)\
                    .replace(word, f"<b>{word}</b>")

                if(i != "examples" and i != "synoyms"):
                    t1 = "div"
                    t2 = 'class="def-ex"'
                else:
                    t1 = "li"
                    t2 = 'class="def-descrip"'

                block += tag_elm([["li", "class='def-descrip'"]], f"{d}") + \
                    "\n" + \
                    tag_elm([[t1, t2]], f"{e}")

                k += 1
            block = tag_elm([["h2", 'class="def-kind"']],
                            f"–{i.strip().lower()}, {n}") +\
                "\n" +\
                tag_elm([["ol", ""]], block)
            defs.append(tag_elm([["div", 'class="def-block"']], block))
            n += 1
        words.append("\n".join(defs))
    return words


word = {"hitherto":
        {"adverb": [
            "up until *this* point, time, etc; until now; heretofore",
            "A force so tremendous it is hitherto unseen by the world at large; its portent wholly evil and tenebrous.",
        ],
            "examples": [
            "He was, hitherto, grate (cheese); howbeit he was bad thereafter playing the flute (string cheese).",
            "The fish were hitherto taken care of, notwithstanding the tempest of late."
        ],
            "synonyms":
            ["heretofore",
             "hithertofore"
             ]
        }
        }

# word = {"herein":
#         {"adverb":
#          ["in or into *this* document, time, object.",
#           "Herein they lay, for withal they shall stay"],
#          "examples":
#          ["Herein sleeps the giant of might",
#           "Herein they lay, for withal they shall stay"]
#          }
#         }


f = open("t.html", "w")

t = create_def_template(word)
for i in t:
    f.write(tag_elm([["div", 'class="back-card"']], i))
    print(i)
f.close()
