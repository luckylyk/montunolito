

def pattern_to_json(pattern):
    json_pattern = {}
    json_pattern['figures'] = pattern['figures'][:]
    json_pattern['behaviors'] = {
        str(k): v for k, v in pattern['behaviors'].items()}
    json_pattern['relationships'] = {
        str(k): {str(l): w for l, w in v.items()}
        for k, v in pattern['relationships'].items()}
    return json_pattern


def json_to_pattern(jsondict):
    pattern = {}
    pattern['figures'] = jsondict['figures'][:]
    pattern['behaviors'] = {
        tuple([int(n) for n in k.strip('()').split(', ')]):
        v for k, v in jsondict['behaviors'].items()}
    pattern['relationships'] = {
        tuple([int(n) for n in k.strip('()').split(', ')]):
        {tuple([int(n) for n in l.strip('()').split(', ')]): w
         for l, w in v.items()}
        for k, v in jsondict['relationships'].items()}
    return pattern