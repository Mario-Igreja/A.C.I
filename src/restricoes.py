# restricoes.py
def experiencia_restricao(assignment):
    experiencia_necessaria = assignment.get('experiencia_vaga', 0)
    experiencia_curriculo = assignment.get('experiencia_curriculo', 0)
    return experiencia_curriculo >= experiencia_necessaria

def habilidades_restricao(assignment):
    habilidades_necessarias = assignment.get('habilidades_vaga', [])
    habilidades_curriculo = assignment.get('habilidades_curriculo', [])
    return all(habilidade in habilidades_curriculo for habilidade in habilidades_necessarias)

def educacao_restricao(assignment):
    grau_minimo = assignment.get('educacao_vaga', '')
    educacao_curriculo = assignment.get('educacao_curriculo', '')
    return educacao_curriculo == grau_minimo
