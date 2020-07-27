word2vec.md

# Introduction au word embedding avec word2vec






```
from gensim.models.word2vec import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from tqdm import tqdm # vaut le coup de creuser
import pandas as pd
import string

tqdm.pandas()

df_wiki = pd.read_csv("en_wiki_SMALL.txt", header=None, sep="noWayYouFindThisSentence268346315618", engine="python")

def clean(text):
    return text.split()


def clean2(text):
    return text.lower().split()

def remove_punctuation(text, punctuation=string.punctuation):
    """
    From string.punctuation, each character is replaced by None (the character is removed)
    """
    text = text.translate(str.maketrans('', '', punctuation))
    return text

def clean3(text):
    return remove_punctuation(text).split()



# Stopwords data
stopwords_en = {"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out",
                "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such",
                "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him",
                "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don",
                "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while",
                "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them",
                "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because",
                "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just",
                "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if",
                "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than"}


def remove_stopwords(text, stopwords):
    """
    Remove every occurrence of the given stopwords set
    """
    text = " ".join([w for w in text.split() if w not in stopwords])
    return text

def clean4(text):
    return remove_stopwords(text)


# df_wiki['clean'] = df_wiki[0].progress_apply(lambda r: clean(r))
# df_wiki['clean2'] = df_wiki[0].progress_apply(lambda r: clean2(r))
df_wiki['clean'] = df_wiki[0].progress_apply(lambda r: clean3(r))
print(df_wiki.head())

w2v = Word2Vec(df_wiki.clean,
               min_count=13, # si le mot est présent moins de ce nombre de fois, le mot n'est pas inclus dans le modèle
               window=2, # le nombre de mots autour desquels on va regarder pour chercher du contexte
               size=67, # la taille de la matrice. petite: peu d'informations circulent. grande: bcp d'infos, mais info qui peut s'éparpiller. on est pas mal vers 300. À 2000, on se rend compte qu'on a pas des meilleurs résultats
               sg=False, # skiggram
               )

#on passe de plusieurs millions (6090307) de mots à 34533
# print(len(w2v.wv.vocab))
# print(sum([w2v.wv.vocab[w].count for w in w2v.wv.vocab]))


def evaluate_model(w2v, evaluation_path_file="questions-words.txt"):
    """
    Given a w2v, print scores for analogies evaluation.
    """
    score, source = w2v.wv.evaluate_word_analogies(evaluation_path_file, dummy4unknown=False)
    print("Within model vocab :", score)
    score, source = w2v.wv.evaluate_word_analogies(evaluation_path_file, dummy4unknown=True)
    print("Whole eval dataset :", score)


# evaluate_model(w2v.wv) # avec le premier clean
# Within model vocab : 0.09091888398147151
# Whole eval dataset : 0.04318460908718788

evaluate_model(w2v.wv) # avec clean3

# on peut
print(w2v.wv.most_similar("however"))
# it
# It (meilleurs résultats: It est en début de phrase)
# mountain
# Mountain

# interessant de régarder le score du plus haut (le mieux compris), et le range entre le premier et le dernir
# score normalisé (pour une certaine norme), entre 0 et 1
# si pas de normalisation, rien n'est comparable: 
```


365Talents
Clément Viricel
Tanguy Moreau
(prenom.nom@365Talents.com)

TAL: Traitement automatique du langage (NLP)

 - traduction automatique (google trad)
 - analyse de sentiment (prédiction d'élections)
 - génération de texte (chatbots)

-> découverte des wordembedding à travers le modèle word2vec, en implémentant nos word2vec

Techno : gensim

## Word2vec

data science:
on sait ce qu'on a comme données d'entrées
on sait ce qu'on veut.
…Il reste à trouver les algos pour faire le lien

-> intuition linguistique: très difficile, c'est un vrai boulot

Comment mesurer la ressemblance entre des mots?
"on reconnait un mot à ce qui l'accompagne", 1957
word embedding space: on transforme un mot en vecteur das l'espacet
-> 2 mots qui se ressemblent ont un angle petit: cos(a, b) proche de 1

Comment faire pour que les vecteurs et les nombres correspondent?

-> impossible à la main (on peut avoir 300 dimensions, et certains dictionnaires ont 200000 mots)
-> IA, modèle word2vec:

CBOW: continuous bag of words
Skipgram
 -> l'un trouve le mot manquant dans une phrase à trou, l'autre fait l'inverse et permet d'avoir le contexte dans lequel on trouve 

skipgram: marche moins bien sur les mots peu fréquents (peu de données)


C'est un réseau de neurones
entrainement du réseau:
mon ____ ronronne quand je le caresse (données sous forme de liste)

 -> modèlisation sous forme de réseau de neurones
 -> interprétation (cheval?)
 -> erreur
 -> optimisation du réseau par rétropropagation

Au début, les mots semblent (sont?) placés aléatoirement, après que l'algo ait tourné il

colan.github understanding LSTMs
(génération de texte)
towarddatascience -> understanding encoder decoder sequence to sequence

ELMo & BERT: les deux derniers algos sortis, les papiers valent le coupw
jalammar.github.io -> bert

# process:

import
tqdm
évaluer


notre dataset: dump de pages wikipedia en texte brut
nettoyage du dataset: ça peut être long: bien réfléchir à l'avance


en passant to en lowercase, on perd de l'information: il n'est plus possible de différencier it (le pronom) et IT (le domaine de l'informatique)


enlever les accent, c'est compliqué: on va rapprocher des mots (les gens oublient souvent les accents), mais d'autres vont se ressembler dans le modèle (jeune et jeûne)

dans notre modèle, on a souvent II à proximité d'élizabeth. C'est une question de choix d'hyperparamètres.

stopwords: il y a très peu de mots (1%) qui représente 99% des mots qu'on trouve dans un texte. Ce sont les mots qu'on veut virer de notre dataset car ils ne sont pas porteur de sens.
Attention: on va perdre de la précision car on va perdre du contexte, hors w2v marche exclusivement avec le contexte

Avantage de word2vec: le modèle s'entraine assez vite


L'ordre des opérations de nettoyage importe. 

 lowercase puis enlever les stopwords != enlever les stopwords puis lowercase.
 (dans un des cas, on va conserver IT, mais en lowercase)

Après clean4, à quoi ressemble notre modèle? il est toujours très basique



## ngrams & min_count

on va regrouper les mots par groupes de longueur N.
ex: notre dame, on peut considérer que c'est un seul mot
hugo, c'est un mot,
victor, c'est pareil, mais victor hugo, si on utilise des 2-grams, c'est un mot qui a du sens.

On peut aussi forcer nos ngram

quand on introduit les ngrams, on a tendance à augmenter notre vocabulaire: on aura toujours "notre" et "dame" dans certains contextes, mais dans certains autres on aura "notre dame"

Dans notre cas, comme on a très peu de données, les ngrams ne marche pas bien: l'évaluation du modèle est de seulement 2%. si on prend min_count = 42 au lieu de 13, on monte à 5%

## POS-tagging

capacité à mettre un tag automatique sur une phrase (nom, pronom, verb, adjectif, adverbe, conjonction, preposition, article, interjection…)

ce sont des modèles qui deviennente

On peut également réduir un mot à sa racine (verbe conjugué -> racine ou infinitif, mots masculins/féminins…). Cela s'appelle la lemmatisation.


Des embedding aboutis existent déja, et on peut les télécharger (rarement en français: la plupart en anglais). En général, c'est trop générique: en fonction de la tâche demandée, il vaut mieux faire son propre embedding


# modèle final:

    #avant: on fait passer les ngrams
    w2v_ngrams = Word2Vec(df_wiki.clean,
               min_count=(2), # 
               window=10, # le nombre de mots autour desquels on va regarder pour chercher du contexte
               size=300, # la taille de la matrice. petite: peu d'informations circulent. grande: bcp d'infos, mais info qui peut s'éparpiller. on est pas mal vers 300. À 2000, on se rend compte qu'on a pas des meilleurs résultats
               sg=True, # skiggram
               )

34% de score au sein du dataset,
10% sur le dataset global

quasiment 50% vient de skipgram
puis la taille 300
ensuite 

C'est assez long


attention à l'overfitting (lire le papier sur word2vec)

# influence du dataset

majeure!

Embeddings sur plein de dataset reddit:

 - the donald
 - conspiracy
 - politics

-> les résultats dépendent énormément des biais que l'on peut trouver dans les datasets

Le choix de dataset est clé