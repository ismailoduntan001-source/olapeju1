"""
Make Olapeju's Yoruba voice files.

Reads every word, sentence and phrase from www/index.html, asks Google
Text-to-Speech for a Yoruba recording of each one, and saves them in
www/audio/ together with a manifest.json the app uses to find them.
"""

import hashlib
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "www" / "index.html"
OUT = ROOT / "www" / "audio"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def load_data():
    html = HTML.read_text(encoding="utf-8")
    m = re.search(r'<script type="application/json" id="lessons">(.*?)</script>',
                  html, re.S)
    if not m:
        sys.exit("Could not find the lessons block in www/index.html")
    return json.loads(m.group(1))


def all_texts(data):
    ph = data["phrases"]
    texts = [ph["greeting"], ph["hello"], ph["tryAgain"]] + list(ph["praise"])
    for words, _english in data["lessons"]:
        texts += list(words)
        texts.append(" ".join(words))
    seen, out = set(), []
    for t in texts:
        t = nfc(t)
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def file_name(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12] + ".mp3"


def main():
    strict = "--strict" in sys.argv
    try:
        from gtts import gTTS
    except ImportError:
        sys.exit("Install the voice library first:  pip install gTTS")

    OUT.mkdir(parents=True, exist_ok=True)
    texts = all_texts(load_data())
    manifest, failed = {}, []

    for i, text in enumerate(texts, 1):
        name = file_name(text)
        path = OUT / name
        if not path.exists() or path.stat().st_size == 0:
            for attempt in range(1, 4):
                try:
                    gTTS(text=text, lang="yo").save(str(path))
                    break
                except Exception as e:
                    if path.exists():
                        path.unlink()
                    if attempt == 3:
                        failed.append((text, str(e)))
                    else:
                        time.sleep(2 * attempt)
            time.sleep(0.4)
        if path.exists() and path.stat().st_size > 0:
            manifest[text] = name
        print("[%d/%d] %s %s" % (i, len(texts), "ok " if text in manifest else "FAIL", text))

    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nSaved %d of %d voice files in %s" % (len(manifest), len(texts), OUT))
    if failed:
        print("Missing %d (the app will use the phone's own voice for these):" % len(failed))
        for t, e in failed:
            print("  - %s  (%s)" % (t, e))
        if strict:
            sys.exit(1)


if __name__ == "__main__":
    main()
