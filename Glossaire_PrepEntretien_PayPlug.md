# Glossaire — Préparation entretien PayPlug
> À lire avant la présentation. Tout ce qu'il faut savoir pour répondre sans hésiter.

---

## DNVB — Digitally Native Vertical Brand

Une DNVB est une marque née sur internet, qui vend **directement au consommateur** sans passer par des distributeurs (pas de Carrefour, pas d'Amazon au départ).

**Les 3 caractéristiques clés :**
- Née en ligne (pas de magasins physiques au départ)
- Vend en direct (D2C = Direct-to-Consumer) sur son propre site
- Maîtrise toute la chaîne : produit → communication → vente → SAV

**Exemples dans le deck :** Le Biberon Français, Trois Kilos Sept — nées sur le web, pas de réseau de distribution.

**Pourquoi c'est important pour PayPlug :** PayPlug co-publie un baromètre annuel des DNVBs avec Digital Native Group. Les DNVBs sont leur cible prioritaire — elles ont des volumes suffisants, un site propre, et sont sensibles à la conversion.

---

## PSP — Payment Service Provider

Le PSP est le prestataire qui traite les paiements en ligne entre le client, la banque, et le marchand.

**Ce qu'il fait concrètement :**
- Sécurise la transaction (cryptage, 3D Secure)
- Vérifie que la carte est valide
- Transfère l'argent du client vers le compte du marchand
- Gère les remboursements et les litiges

**Exemples de PSP :** PayPlug, Stripe, HiPay, Shopify Payments, Adyen, up2pay (Crédit Agricole), Sogenactif (Société Générale).

**À retenir :** Sans PSP, un site e-commerce ne peut pas encaisser de paiement CB.

---

## Stack (Stack technique)

La "stack" c'est l'ensemble des outils technologiques qu'utilise une entreprise pour faire tourner son site.

**La stack d'un site e-commerce typique :**
- **CMS** (le moteur du site) : PrestaShop, Shopify, WooCommerce, ou du sur-mesure ("custom")
- **PSP** (les paiements) : PayPlug, Stripe…
- **BNPL** (le fractionné) : Alma, Oney, Klarna…
- **CRM/Email** : Klaviyo, Mailchimp…
- **Analytics** : Snowplow, Google Analytics…

**Pourquoi c'est important :** Avant de prospecter, identifier la stack permet de savoir si l'intégration PayPlug sera simple (module natif PrestaShop = 2h) ou complexe (site custom = intégration API).

---

## BNPL — Buy Now Pay Later

Le BNPL (payer maintenant, rembourser plus tard) permet au client de fractionner son achat en 3 ou 4 fois, souvent sans frais pour lui.

**Comment ça marche :**
- Le client choisit "payer en 3x" au checkout
- Le PSP/BNPL avance l'argent intégralement au marchand
- Le client rembourse en 3 mensualités
- Le marchand paie une commission (~1,5%) au prestataire BNPL

**Les acteurs principaux :** Oney (France, lié à BPCE), Alma (startup française), Klarna (suédois, très présent en Europe).

**Pourquoi c'est un argument fort pour PayPlug :** PayPlug intègre Oney nativement. Pour un marchand sur PrestaShop sans BNPL, PayPlug apporte CB + Oney en un seul contrat, sans ajouter un prestataire supplémentaire.

**Seuil Oney :** généralement à partir de 100€ de panier. En dessous, le fractionné est moins pertinent (d'où la nuance sur Mustela avec un panier moyen de 50-70€).

---

## HiPay

HiPay est un PSP français fondé en 2002, concurrent de PayPlug.

**Ce qu'il faut savoir :**
- Positionné sur les moyennes et grandes entreprises
- Interface marchand moins moderne que les nouveaux PSP
- Tarification souvent moins compétitive que Stripe ou PayPlug
- N'intègre pas Oney nativement → les marchands doivent ajouter Alma ou Klarna en plus, ce qui fait deux contrats séparés

**Dans le deck :** Aubert utilise HiPay + Alma (deux prestataires séparés). L'argument PayPlug : un seul contrat pour CB + Oney, et une interface plus moderne.

---

## PSP bancaire traditionnel vs PSP moderne

### PSP bancaires traditionnels (Sogenactif, up2pay, Mercanet…)
Ces solutions sont les **gateways de paiement des grandes banques françaises** :
- Sogenactif = Société Générale
- up2pay / e-transactions = Crédit Agricole
- Mercanet = BNP Paribas
- Paybox = Banque Populaire / Caisse d'Épargne

**Leurs limites :**
- Interfaces marchands vieillissantes, peu intuitives
- Intégration technique complexe, souvent nécessite un développeur
- Virements J+3 à J+5 (lent pour la trésorerie)
- Pas d'intégration BNPL native (pas d'Oney, pas d'Alma)
- Support client lent, passant par la banque
- Taux de transaction parfois moins compétitifs

**PayPlug en face :**
- Interface moderne, tableau de bord clair
- Module natif PrestaShop/Shopify → intégration en 2h sans développeur
- Virements quotidiens → meilleure trésorerie pour le marchand
- Oney intégré directement
- Support dédié en français

---

## Pourquoi un marchand Shopify passerait à PayPlug ?

C'est la bonne question, parce que Shopify Payments est intégré et simple. La réponse honnête : **c'est difficile**, mais pas impossible.

**Les freins :**
- Si un marchand quitte Shopify Payments pour un PSP externe, Shopify facture des **frais de gateway externe** (0,5% à 2% selon le plan) — ce qui peut renchérir le coût total
- Shopify Payments est simple et déjà en place

**Les cas où ça vaut quand même le coup :**
- **L'argument Oney** : Shopify Payments ne propose pas Oney. Si le marchand veut du BNPL français (meilleur taux d'acceptation qu'Alma ou Klarna côté consommateur français), PayPlug est la solution la plus simple
- **Les virements quotidiens** : Shopify Payments vire J+3 minimum. PayPlug vire chaque jour → argument trésorerie
- **Le support** : Shopify Payments = support anglophone, automatisé. PayPlug = interlocuteur français dédié
- **Volumes importants** : à partir d'un certain volume, PayPlug peut proposer des taux négociés inférieurs

**À retenir pour l'entretien :** Pour Mustela sur Shopify, l'argument PayPlug c'est **Oney uniquement**, pas le remplacement du PSP (qui serait contre-productif financièrement). Le pitch est : "activez Oney via PayPlug en parallèle de Shopify Payments".

---

## UX marchande datée

"UX marchande" = l'expérience utilisateur côté marchand, c'est-à-dire l'interface que voit l'équipe e-commerce au quotidien pour suivre les paiements, gérer les remboursements, analyser les transactions.

**Ce que veut dire "datée" :**
- Interface des années 2005-2010 (grise, dense, peu intuitive)
- Pas de tableau de bord clair pour suivre les conversions
- Exports manuels pour réconcilier les paiements
- Pas d'alertes en temps réel
- Connexion parfois par certificat électronique

**En pratique :** les équipes e-commerce qui utilisent Sogenactif ou up2pay au quotidien se plaignent souvent de devoir naviguer dans des interfaces peu ergonomiques pour gérer des remboursements ou analyser des pics de trafic. PayPlug propose une interface moderne avec analytics intégrés.

---

## Klaviyo, Yotpo, Snowplow

Ces trois outils apparaissent dans la slide Mustela comme indicateurs d'une infrastructure marketing avancée.

**Klaviyo** — outil d'email marketing et CRM
- Le standard des marques e-commerce DTC
- Permet d'envoyer des emails automatisés basés sur le comportement (abandon de panier, relance post-achat…)
- Très populaire chez les DNVBs et marques Shopify
- Signal : une marque sur Klaviyo investit dans la conversion → sensible aux arguments taux de conversion

**Yotpo** — plateforme d'avis clients et fidélisation
- Collecte et affiche les avis clients sur le site
- Gère les programmes de fidélité et de parrainage
- Signal : la marque travaille sa preuve sociale et sa rétention → pense ROI

**Snowplow** — analytics avancée / tracking comportemental
- Outil de collecte de données comportementales (plus technique que Google Analytics)
- Utilisé par des équipes data matures qui veulent maîtriser leur propre data
- Signal : Mustela a une équipe data sérieuse, ils mesurent tout → ils savent calculer un ROI et seront réceptifs à un argument chiffré comme la simulation Oney

**Ce que ça dit de Mustela :** une infrastructure marketing sophistiquée = une équipe qui pense conversion, data, ROI. L'argument "Oney booste votre conversion de +22% sur les coffrets" est exactement le bon angle.

---

## D'où viennent les stats activité en ligne / physique ?

**Réponse honnête : ce sont des estimations raisonnées, pas des chiffres officiels publiés.**

Pour chaque prospect, j'ai estimé la répartition en fonction du modèle économique :

| Prospect | Estimation | Raisonnement |
|---|---|---|
| Le Biberon Français | 85% online | DNVB pure player, quelques corners en boutique |
| Mustela | 45% online | Vendu en pharmacie, parapharmacies, grande surface — distribution physique dominante |
| Aubert | 40% online | Réseau de magasins physiques depuis 1931, site e-commerce secondaire |
| Trois Kilos Sept | 90% online | DNVB, vente directe sur site, présence physique quasi nulle |
| Made in Bébé | 100% online | Pure player e-commerce, pas de magasin physique |

**Si on te demande ta source en entretien :** *"Ce sont des estimations basées sur le modèle économique de chaque entreprise — je n'ai pas trouvé de données officielles publiées sur la répartition canal par canal. Pour Mustela par exemple, leur distribution en pharmacie représente clairement la majorité des volumes, donc j'ai estimé l'online à 45%."*

C'est une réponse honnête et elle montre ta rigueur analytique.

---

*Document préparé pour l'entretien stage SDR PayPlug — Avril 2026*
