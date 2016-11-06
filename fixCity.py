# Has too many similar lines so it would be better to separate it
def fixCityName(c):
    if "prish" in c.lower():
        return "Prishtinë"
    elif "gjila" in c.lower():
        return "Gjilan"
    elif "priz" in c.lower():
        return "Prizren"
    elif "gjako" in c.lower():
        return "Gjakovë"
    elif "pej" in c.lower():
        return "Pejë"
    elif "viti" in c.lower():
        return "Viti"
    elif "poduje" in c.lower():
        return "Podujevë"
    elif "besia" in c.lower():
        return "Podujevë"
    elif "istog" in c.lower():
        return "Istog"
    elif "klin" in c.lower():
        return "Klinë"
    elif "suharek" in c.lower():
        return "Suharekë"
    elif "shtime" in c.lower():
        return "Shtime"
    elif "feriz" in c.lower():
        return "Ferizaj"
    elif "obiliq" in c.lower():
        return "Obiliq"
    elif "f.kosov" in c.lower():
        return "Fushë Kosovë"
    elif "fushe kosov" in c.lower():
        return "Fushë Kosovë"
    elif "lipja" in c.lower():
        return "Lipjan"
    elif "kamenic" in c.lower():
        return "Kamenicë"
    elif "mitrov" in c.lower():
        return "Mitrovicë"
    elif "malishe" in c.lower():
        return "Malishevë"
    elif "drenas" in c.lower():
        return "Drenas"
    elif "prsih" in c.lower():
        return "Prishtinë"
    elif "syhar" in c.lower():
        return "Suharekë"
    elif "rahove" in c.lower():
        return "Rahovec"
    elif "deqan" in c.lower():
        return "Deçan"
    elif "deçan" in c.lower():
        return "Deçan"
    elif "junik" in c.lower():
        return "Junik"
    elif "kosov" in c.lower():
        return "Fushë Kosovë"
    elif "kaçani" in c.lower():
        return "Kaçanik"
    elif "tiran" in c.lower():
        return "Tiranë"
    elif "vushtrr" in c.lower():
        return "Vushtrri"
    elif "zagreb" in c.lower():
        return "Zagreb"
    elif "gjhilan" in c.lower():
        return "Gjilan"
    elif "artan" in c.lower():
        return "Artanë"
    elif "dragas" in c.lower():
        return "Dragash"
    elif "leposav" in c.lower():
        return "Leposaviq"
    elif "graçani" in c.lower():
        return "Graçanicë"
    elif "zveçan" in c.lower():
        return "Zveçan"
    elif "graqani" in c.lower():
        return "Graçanicë"
    elif "shterpc" in c.lower():
        return "Shtërpcë"
    elif "shtërpc" in c.lower():
        return "Shtërpcë"
    elif "zubin" in c.lower():
        return "Zubin Potok"
    elif "ranillu" in c.lower():
        return "Ranillug"
    elif "novob" in c.lower():
        return "Novobërdë"
    elif "klin" in c.lower():
        return "Klinë"
    elif "" in c:
        return "I pacaktuar"
    else:
        return c
