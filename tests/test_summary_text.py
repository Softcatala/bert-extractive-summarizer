import pytest
from summarizer import Summarizer


@pytest.fixture()
def summarizer():
    return Summarizer('distilbert-base-uncased')


@pytest.fixture()
def passage():
    return '''
—Els indults són bons per als presos i fatals per al moviment. En el sentit del reconeixement internacional, de l’excitació internacional, de l’abús de l’estat, de tapar els tres mil represaliats i continuar tranquil·lament. Ells saben que el perill és al carrer. Amb els indults posen en llibertat els possibles negociadors, res més que això. Ara, que fotin el camp de la presó, que siguin lliures, que respirin, que vegin la família… I que es mirin el país una altra vegada des del carrer i no des de darrere dels barrots.

—Potser sí. És que és una situació personal i familiar dificilíssima. Encara que un vulgui ser absolutament coherent, els condicionants són tals que la prudència seria dir “feu”, i desaparèixer. Ara de moment és el contrari. Però si em demaneu si Oriol Junqueras té dret de fer política, i tant que en té! Mentre el seu partit li ho demani. Jordi Sànchez hi té dret? Tot el del món! Ara, això és bo per al país? Per mi, la política s’ha de fer amb molt contacte amb la societat, no de la gent que et ve a visitar sinó de la que et trobes al carrer. Els partits són unes bombolles cada dia més impermeables. Doncs dins de la presó, encara molt més. Jo crec que no és bo. I per una altra cosa: els partits tenen unes dinàmiques interiors, de funcionament, de lideratge, que s’acaben fent taps. Involuntàriament, eh? Però se’n fan.
    '''

def test_do_not_use_first(summarizer, passage):
    res = summarizer(passage, num_sentences=3)
    
    expected_summary = '—Els indults són bons per als presos i fatals per al moviment. Encara que un vulgui ser absolutament coherent, els condicionants són tals que la prudència seria dir “feu”, i desaparèixer. Els partits són unes bombolles cada dia més impermeables. I per una altra cosa: els partits tenen unes dinàmiques interiors, de funcionament, de lideratge, que s’acaben fent taps.'

    assert res == expected_summary



