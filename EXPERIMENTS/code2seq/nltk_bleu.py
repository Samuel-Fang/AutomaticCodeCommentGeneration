from nltk.translate.bleu_score import corpus_bleu

def nltk_bleu(ref_file, hyp_file):
    rf = open(ref_file, 'r')
    hf = open(hyp_file, 'r')

    refs = []
    hyps = []

    for ref, hyp in zip(rf.readlines(), hf.readlines()):
        refs.append([ref])
        hyps.append(hyp)

    return corpus_bleu(refs, hyps)*100