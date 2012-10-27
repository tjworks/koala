import re

def parsePhone(txt):
    """
    Parse out phone number that may be in word format
    """
    txt = txt.replace('-', '').lower().replace('.', '')
    reps = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, "zero":0}
    for key,num in reps.iteritems():
        txt=txt.replace(key, "%s" %num)
    txt = txt.replace(' ', '')
    #pat = re.compile(r"(\s*one\s*|\s*two\s*|\s*three\s*|\s*four\s*|\s*five\s*|\s*six\s*|\s*seven\s*|\s*eight\s*|\s*nine\s*|\s*zero\s*|\s*[0-9]\s*){10}", re.IGNORECASE)
    pat = re.compile("[2-9][0-9]{9}")
    matcher = pat.search(txt)
    print("matcher %s --> %s" %(matcher, txt) )
    if(matcher): return matcher.group(0)
    return None