---
id: 844
title: 'Tester (correctement !) la présence d&rsquo;une clé dans un tableau en PHP'
date: 2016-12-13T08:21:18+00:00
author: Keirua
layout: post
guid: http://blog.keiruaprod.fr/?p=844
permalink: /2016/12/13/tester-correctement-la-presence-dune-cle-dans-un-tableau-en-php/
robotsmeta:
  - index,follow
categories:
  - Non classé
lang: fr
---
La plupart du temps, pour tester si une clé est présente dans un tableau, il faut utiliser **array\_key\_exists**. Pourtant on trouve encore des **empty** et **isset** à sa place, en pensant que ces 3 fonctions sont interchangeables : ce n&rsquo;est pas le cas. Fin 2016 on trouve encore des confusions, donc cet article me servira de référence pour les futures revues de code 🙂

<!--more-->

Au premier coup d&rsquo;oeil, on a pourtant l&rsquo;impression qu&rsquo;elles font la même chose : 

<pre><code lang="php">

$a = ['AB' => 12, 'CB' => 34];

// 2 cas nominaux :
echo "Cas nominal : La clé est présente dans le tableau".PHP_EOL;
echo (int)array_key_exists('AB', $a).PHP_EOL;
echo (int)isset($a['AB']).PHP_EOL;
echo (int)!empty($a['AB']).PHP_EOL;

echo "Cas nominal : La clé n'est pas présente dans le tableau".PHP_EOL;
echo (int)array_key_exists('YZ', $a).PHP_EOL;
echo (int)isset($a['YZ']).PHP_EOL;
echo (int)!empty($a['YZ']).PHP_EOL;
</code></pre>

Ce bout de code produit la sortie suivate :

    Cas nominal : La clé est présente dans le tableau
    1
    1
    1
    Cas nominal : La clé n'est pas présente dans le tableau
    0
    0
    0
    

La sortie dans les cas nominaux est bien celle attendu, d&rsquo;où la confusion, mais nous allons voir dans quels cas celà peut poser problème.

## <a id="user-content-isset" class="anchor" href="#isset" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>isset

Je trouve régulièrement ce genre de bouts de code pour tester si une clé existe dans un tableau :

<pre><code lang="php">if (isset($values['reason'])) {
    // do something with $values['reason']
}
</code></pre>

Le problème, c&rsquo;est que ce bout de code ne fait pas **toujours** ce que son auteur pense.

Selon la documentation, [**isset**](php.net/isset)  » Retourne TRUE si var existe **et a une valeur autre que NULL**. FALSE sinon. « 

Donc si $values[&lsquo;reason&rsquo;] existe mais que sa valeur est nulle, le code à l&rsquo;intérieur du if ne sera pas exécuté, ce qui peut avoir des effets de bord pénibles.

## <a id="user-content-empty" class="anchor" href="#empty" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>empty

Un autre exemple de code qui peut poser problème ?

<pre><code lang="php">$exitCode = !empty($data['EXIT_CODE']) ? $data['EXIT_CODE'] : null
</code></pre>

Nous allons voir pourquoi, dans certains cas, $exitCode vaudra null, ce qui n&rsquo;est peut-être pas le comportement attendu.

Selon la documentation, [**empty**](php.net/empty): « Retourne FALSE si var existe *_et est non-vide, et dont la valeur n&rsquo;est pas zéro. *_« 

     Ce qui suit est considéré comme étant vide :
    
        "" (une chaîne vide)
        0 (0 en tant qu'entier)
        0.0 (0 en tant que nombre à virgule flottante)
        "0" (0 en tant que chaîne de caractères)
        NULL
        FALSE
        array() (un tableau vide)
        $var; (une variable déclarée, mais sans valeur)
    

Le risque d&rsquo;effet de bord, c&rsquo;est si la valeur de $data[&lsquo;EXIT_CODE&rsquo;] a une valeur « vide », par exemple 0 : à cause de la manière dont est écrit le test au début de cette section, $exitCode vaudra null et non 0, ce qui peut poser problème (par exemple si plus loin on teste si $exitCode === null).

## <a id="user-content-on-teste" class="anchor" href="#on-teste" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>On teste

Armé de nos connaissances précises sur le fonctionnement d&#8217;empty et isset, on peut écrire un bout de code pour voir qu&rsquo;effectivement, dans certains cas le test n&rsquo;aura pas le comportement attendu par le développeur _qui veut tester la présence de la clé dans un tableau_ :

<pre><code lang="php">echo "Cas limite : la clé est présente mais vaut 0".PHP_EOL;
$b = ['EF' => 0];
echo (int)array_key_exists('EF', $b).PHP_EOL;
echo (int)isset($b['EF']).PHP_EOL;
echo (int)!empty($b['EF']).PHP_EOL;
</code></pre>

Ce bout de code produit les sorties suivantes :

    Cas limite : la clé est présente mais vaut 0
    1
    1
    0
    

Quand la clé est présente mais vaut 0, **!empty** vaut false, car la valeur testée est (légitimement) vide.

Prenons un autre exemple, où la valeur est présente mais vaut **null**. Là **isset** également n&rsquo;a pas le comportement que croyait le développeur.

<pre><code lang="php">echo "Cas limite : la clé est présente mais vaut null".PHP_EOL;
$c = ['GH' => null];
echo (int)array_key_exists('GH', $c).PHP_EOL;
echo (int)isset($c['GH']).PHP_EOL;
echo (int)!empty($c['GH']).PHP_EOL;

Cas limite : la clé est présente mais vaut null
1
0
0
</code></pre>

Dans ce dernier exemple, seul array\_key\_exists a le comportement que veut le développeur.

# <a id="user-content-bref" class="anchor" href="#bref" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>bref

Ce comportment n&rsquo;est pas un bug de PHP : il faut bien voir que les fonctions isset et empty ont ce comportement car c&rsquo;est celui qu&rsquo;on attend d&rsquo;elles. En sont conçues pour celà. C&rsquo;est leur usage qui est inadapté dans certains cas. Il s&rsquo;est répandu à une époque où isset et empty étaient plus rapides qu&rsquo;array\_key\_exist pour le test d&rsquo;existence. Je ne sais pas si c&rsquo;est encore le cas, mais ça n&rsquo;a aucune importance : il faut bien comprendre que ce genre de micro-optimisations n&rsquo;a pas de sens (optimisez les portions du code qui comptent d&rsquo;abord !) et si vous voulez le faire quand même, faites le en comprenant les effets de bord et en vous assurant que vous les traitez comme il se doit.

Ceci étant dit, en général, si vous voulez tester qu&rsquo;une clé est présente dans un tableau, utilisez \*\*array\_key\_exists\*\*. Le code de ce [**gist**](https://gist.github.com/Keirua/35a32326606368a6a3beb7b4ead01803) est disponible sur github pour refaire le test chez vous.