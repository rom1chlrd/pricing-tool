# PayPlug — Analyse concurrentielle
### Secteur bébé / enfant — Préparation entretien SDR

---

## 1. Positionnement PayPlug

PayPlug est une **solution de paiement française** (groupe BPCE), conçue pour les **PME et ETI** qui vendent en ligne et en magasin. Son modèle économique repose sur le **GMV transactionnel** : plus les marchands encaissent, plus PayPlug gagne. Ça aligne les intérêts.

**Forces structurelles :**
- Support client 100% en français, réactif (argument fort vs Stripe/Adyen)
- Intégration **native** sur PrestaShop, WooCommerce, Magento, Shopify
- Module **Oney** intégré (3x/4x) — différenciant fort en France
- Virements quotidiens (meilleure trésorerie vs cycles hebdomadaires Stripe)
- Adossé au groupe BPCE → confiance, stabilité, conformité SEPA
- Back-office transparent : raisons d'échec de paiement visibles en temps réel
- Liens de paiement (utiles en omnicanal ou si le site plante)

**Sweet spot :** PME française, 5–150M€ de CA, PrestaShop/WooCommerce/Shopify, panier moyen >50€

---

## 2. Tableau comparatif rapide

| Critère | PayPlug | Stripe | Shopify Payments | HiPay | Adyen | Alma | Klarna |
|---|---|---|---|---|---|---|---|
| Origine | 🇫🇷 France | 🇺🇸 USA | 🇺🇸 USA | 🇫🇷 France | 🇳🇱 Pays-Bas | 🇫🇷 France | 🇸🇪 Suède |
| Cible | PME/ETI | Toutes tailles | Marchands Shopify | PME/ETI | Enterprise | Tous | Tous |
| Support FR | ✅ Oui | ⚠️ Limité | ⚠️ Limité | ✅ Oui | ❌ Non | ✅ Oui | ⚠️ Limité |
| Oney 3x/4x | ✅ Natif | ❌ Non | ❌ Non | ✅ Via HiPay | ✅ Via module | ❌ (concurrent) | ❌ (concurrent) |
| PrestaShop natif | ✅ | ✅ | ❌ | ⚠️ Module tiers | ❌ | ✅ | ✅ |
| Shopify | ✅ Module | ✅ Natif | ✅ Natif | ✅ App | ✅ App | ✅ App | ✅ App |
| Virements quotidiens | ✅ | ❌ (hebdo) | ❌ | ✅ | ❌ | N/A | N/A |
| Tarifs PME | ✅ Compétitif | ⚠️ Variable | ⚠️ Frais extra si tiers | ⚠️ | ❌ Minimums élevés | ⚠️ Commission/vente | ⚠️ |

---

## 3. PayPlug vs Stripe

**Contexte prospect :** Le Biberon Français (PrestaShop + Stripe), Mustela (Shopify Payments = Stripe)

### Pourquoi Stripe est là
Stripe est le choix par défaut des développeurs et des DNVBs nées sur internet. API puissante, documentation excellente, intégration rapide. C'est souvent le premier PSP d'une startup.

### Où PayPlug gagne

**Oney vs rien.** Stripe ne propose pas Oney nativement en France. Pour une marque avec un panier moyen >80€, ne pas proposer de 3x/4x c'est laisser de la conversion sur la table. PayPlug l'apporte clé en main.

**Support en français.** Stripe = support anglophone, tickets, délais. PayPlug = account manager dédié, ligne directe, réponse dans l'heure (cf. cas Tajinebanane). Pour une PME qui a un bug de paiement un vendredi soir, ça change tout.

**Virements quotidiens.** Stripe vire les fonds tous les 7 jours par défaut. PayPlug tous les jours. Sur un volume de 500K€/mois, c'est plusieurs dizaines de milliers d'euros de trésorerie immobilisée en moins.

**Migration sans dev sur PrestaShop.** Le module PayPlug s'installe en quelques clics sur PrestaShop. Pas besoin de toucher au code, pas de ticket dev, pas de régression à risquer.

### Où Stripe reste fort
- API plus puissante pour les cas complexes (abonnements, marketplaces)
- Présence internationale plus large
- Écosystème dev plus riche

### Pitch type
> *"Vous êtes sur Stripe + PrestaShop. La migration vers PayPlug prend 2h sans dev, vous gardez exactement les mêmes fonctionnalités, vous ajoutez Oney 3x/4x immédiatement, et vous avez un interlocuteur français qui répond dans la journée. Qu'est-ce qui vous retient ?"*

---

## 4. PayPlug vs Shopify Payments

**Contexte prospect :** Mustela, Tartine et Chocolat

### Pourquoi Shopify Payments est là
C'est le PSP par défaut de Shopify. Installation zéro, intégré nativement. Shopify pousse dessus en appliquant des frais de transaction supplémentaires si on passe par un tiers.

### Où PayPlug gagne

**Oney — l'argument numéro 1.** Shopify Payments ne propose pas Oney en France. C'est la seule vraie brèche. Pour Mustela (paniers jusqu'à 350€) ou Tartine et Chocolat (manteaux à 200€, robes à 120€), le 3x/4x peut augmenter la conversion de 15 à 20% sur les paniers élevés.

**Virements quotidiens.** Shopify Payments vire les fonds avec un décalage de plusieurs jours. PayPlug vire quotidiennement.

**Support français.** Même argument que vs Stripe.

### La vraie contrainte
Shopify facture des frais de transaction (0,5 à 2%) si on utilise un PSP externe à la place de Shopify Payments. Ça réduit l'écart de marge. Le pitch doit donc se concentrer sur la **valeur Oney** : si Oney génère +15% de conversion sur les paniers >100€, ça absorbe largement les frais.

### Pitch type
> *"Vous n'avez pas de paiement fractionné aujourd'hui. Avec PayPlug + Oney, vos clientes peuvent payer leur poussette en 3x sans frais. Sur vos paniers à 200-350€, c'est un levier de conversion direct. Les frais de transaction Shopify sont compensés dès le 1er mois si la conversion monte de 10%."*

---

## 5. PayPlug vs HiPay

**Contexte prospect :** Aubert (HiPay + Alma)

### Pourquoi HiPay est là
HiPay est un PSP français historique, souvent recommandé par les agences e-commerce françaises il y a 5-10 ans. Présent sur des sites custom ou Magento.

### Où PayPlug gagne

**Intégrations CMS plus modernes.** PayPlug a des modules natifs mieux maintenus sur les CMS actuels. HiPay a vieilli dans son positionnement.

**Oney intégré vs Alma séparé.** Aubert a HiPay pour les CB + Alma séparé pour le fractionné. C'est deux contrats, deux tableaux de bord, deux équipes support. PayPlug centralise CB + Oney en un seul contrat.

**Notoriété et expérience marchande.** PayPlug a investi dans l'UX marchande (back-office, raisons d'échec, liens de paiement). HiPay est perçu comme plus technique, moins orienté PME.

**Backing BPCE.** PayPlug est adossé à un grand groupe bancaire français, ce qui rassure sur la pérennité et la conformité réglementaire.

### Pitch type
> *"Vous avez HiPay pour vos paiements CB et Alma pour le fractionné. Deux prestataires, deux contrats, deux interfaces. PayPlug vous permet de centraliser les deux, avec Oney inclus, un seul interlocuteur, et un back-office où vous voyez en temps réel pourquoi un paiement a échoué."*

---

## 6. PayPlug vs Adyen

**Contexte :** Jacadi, Okaïdi (hors liste prospects — trop enterprise)

### Pourquoi ce n'est généralement pas le bon terrain pour PayPlug
Adyen est un PSP enterprise (Uber, Spotify, H&M). Minimums contractuels élevés, équipes dédiées, intégrations complexes. Une PME sous Adyen a probablement un contrat négocié et une équipe tech qui maintient l'intégration.

### Quand PayPlug peut quand même entrer
Si une boîte mid-size est sur Adyen mais sous-utilise ses fonctionnalités (pas de BNPL, pas d'omnicanal) et paye les minimums → PayPlug peut proposer un meilleur rapport qualité/prix avec plus de service.

### À retenir pour l'entretien
Ne pas aller chasser sur Adyen. Si un prospect est sur Adyen, c'est un signal qu'ils sont hors ICP PayPlug.

---

## 7. PayPlug vs Alma & Klarna (BNPL)

**Important :** Alma et Klarna ne sont **pas des PSPs**, ce sont des solutions de **paiement fractionné uniquement**. Ils viennent toujours en complément d'un PSP principal (HiPay, Shopify Payments, etc.).

### Alma
- Français, très bien implanté dans le secteur bébé (Aubert, Bébé 9, Orchestra, Trois Kilos Sept)
- Spécialiste du 2x/3x/4x, interface simple, bonne réputation marchande
- **Ne gère pas les paiements CB standard** → toujours associé à un PSP
- **Vs PayPlug :** PayPlug inclut Oney (concurrent d'Alma) en natif. Si un prospect a déjà Alma, l'argument c'est la consolidation : un seul contrat, un seul tableau de bord.

### Klarna
- Suédois, fort en Europe du Nord, monte en France (Babymoov, Allobébé, Okaïdi)
- BNPL + expérience shopping (wishlist, app)
- Plus orienté consumer brand que merchant tool
- **Vs PayPlug :** même logique — Klarna ne remplace pas un PSP, il le complète. Si un prospect a Klarna, PayPlug peut entrer sur la couche PSP.

---

## 8. Application aux 5 prospects

| Prospect | PSP actuel | Concurrent principal | Angle PayPlug | Force de l'argument |
|---|---|---|---|---|
| Le Biberon Français | Stripe | Stripe | Migration PrestaShop sans dev + Oney | ⭐⭐⭐ Fort |
| Mustela | Shopify Payments | Shopify Payments | Oney sur paniers 100-350€, pas de BNPL en place | ⭐⭐⭐ Fort |
| Aubert | HiPay + Alma | HiPay | Centraliser PSP + Oney en 1 contrat, remplacer HiPay | ⭐⭐ Moyen |
| Trois Kilos Sept | Inconnu + Alma | Alma (BNPL) | Module PrestaShop natif, identifier le PSP base | ⭐⭐ À confirmer |
| Tartine et Chocolat | Shopify Payments | Shopify Payments | Oney sur paniers luxe >150€, pas de BNPL | ⭐⭐ Moyen |

---

## 9. Ce que PayPlug ne dit pas (mais que tu dois savoir)

- Sur Shopify, Shopify Payments impose des **frais de transaction supplémentaires** si on utilise un PSP externe → à anticiper dans le calcul ROI
- Oney nécessite un **scoring** de chaque transaction → taux d'acceptation variable selon le profil client (moins fluide que Alma sur ce point)
- PayPlug est moins adapté aux **abonnements complexes** (Stripe gagne sur ce terrain)
- La **taille minimale** pour que PayPlug soit vraiment rentable côté merchant : environ 500K€ de GMV/an en ligne

---

*Document préparé pour l'entretien PayPlug — Stage SDR — Avril 2026*
