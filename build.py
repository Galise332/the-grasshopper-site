"""Génère le site statique The Grasshopper (pages HTML, sitemap, robots).

Toutes les informations affichées proviennent de https://www.thegrasshopper.be/fr
(relevé du 2026-09-29). Aucune information n'a été inventée.

Usage : python build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
BASE_URL = "https://galise332.github.io/the-grasshopper-site/"
SHOP = "https://www.thegrasshopper.be/fr/"
# Version de démonstration : tant que DEMO est à True, les moteurs de recherche
# n'indexent pas cette copie (évite le contenu dupliqué avec le site officiel).
# Passer à False le jour de la mise en ligne sur le vrai nom de domaine.
DEMO = True

FACEBOOK = "https://www.facebook.com/thegrasshopperbrussels/"
INSTAGRAM = "https://www.instagram.com/the_grasshopper_brussels"

STORES = [
    {
        "id": "bruxelles",
        "name": "The Grasshopper Bruxelles",
        "street": "Rue du Marché aux Herbes 39-43",
        "zip": "1000",
        "city": "Bruxelles",
        "tel_display": "02/511 96 22",
        "tel": "+3225119622",
        "email": "buy@thegrasshopper.be",
        "hours": "Ouvert tous les jours (y compris les dimanches et jours fériés) de 10 à 19 heures",
        "hours_note": "Fermé le 25 décembre et le 1er janvier",
        "vat_display": "TVA BE 0737 840 792",
        "vat": "BE0737840792",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "10:00",
        "closes": "19:00",
    },
    {
        "id": "louvain",
        "name": "The Grasshopper Leuven",
        "street": "Mechelsestraat 24a",
        "zip": "3000",
        "city": "Louvain",
        "tel_display": "016/297 997",
        "tel": "+3216297997",
        "email": "leuven@thegrasshopper.be",
        "hours": "Ouvert du lundi au samedi de 10 à 18 heures",
        "hours_note": "",
        "vat_display": "TVA BE 0878 375 481",
        "vat": "BE0878375481",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "opens": "10:00",
        "closes": "18:00",
    },
]

# (libellé, slug sur la boutique en ligne, image)
CATEGORIES = [
    ("Bébêtes", "allemaalbeestjes", "cat-bebetes.webp"),
    ("Bébé", "baby", "cat-bebe.webp"),
    ("Bain", "bad-en-regenspeelgoed", "cat-bain.webp"),
    ("Construire", "bouwen", "cat-construire.webp"),
    ("Dehors", "buitenspeelgoed", "cat-dehors.webp"),
    ("Créatif", "knutselen", "cat-creatif.webp"),
    ("Einstein", "ontdekken", "cat-einstein.webp"),
    ("Châteaux forts", "kasteel", "cat-chateaux.webp"),
    ("Cuisiner", "koken", "cat-cuisiner.webp"),
    ("Maestro", "muziekinstrumenten", "cat-maestro.webp"),
    ("Nostalgie", "lekker-nostalgisch", "cat-nostalgie.webp"),
    ("Ça roule", "rijden", "cat-caroule.webp"),
    ("Bébé devient grand", "peuter", "cat-bebe-grand.webp"),
    ("Peluches", "knuffels", "cat-peluches.webp"),
    ("Poupées", "poppen", "cat-poupees.webp"),
    ("Maison de poupées", "poppenhuizen", "cat-maison-poupees.webp"),
    ("Puzzles", "puzzels", "cat-puzzles.webp"),
    ("Jeux de société", "gezelschapsspelletjes", "cat-jeux.webp"),
    ("À l'école", "terug-naar-school", "cat-ecole.webp"),
    ("Déguisements", "verkleedfeest", "cat-deguisements.webp"),
    ("Faire les courses", "winkelen", "cat-courses.webp"),
]

VOUCHERS = [20, 25, 30, 40, 50, 75, 100, 125, 150, 200]

FAQ = [
    ("La livraison est-elle gratuite ?",
     "Les frais de livraison et d'expédition sont à la charge du client. Toutefois, les commandes supérieures à 75€ bénéficient de la livraison gratuite."),
    ("Puis-je retirer ma commande en magasin ?",
     "Les clients ont également la possibilité de retirer leur colis en magasin."),
    ("Quels sont les moyens de paiement acceptés ?",
     "Le paiement peut être effectué via Bancontact, carte de crédit ou Paypal."),
    ("Qui livre les colis ?",
     "Les livraisons sont effectuées par bpost ou DPD. Dès que le colis est prêt à être expédié, le destinataire reçoit un e-mail contenant des informations sur la livraison prévue du colis, avec un créneau horaire indicatif pour la livraison."),
    ("Puis-je retourner un article ?",
     "Le consommateur a le droit de notifier au vendeur, dans un délai de 14 jours après réception du produit, qu'il souhaite exercer son droit de rétractation, sans frais et sans avoir à motiver sa décision."),
    ("Je ne trouve pas un jouet sur le site, que faire ?",
     "Tous nos trésors ne se trouvent pas sur notre site. N'hésitez pas à nous contacter pour savoir si nous avons ce que vous recherchez."),
    ("Combien de temps un chèque-cadeau est-il valable ?",
     "Les chèques-cadeaux ont une validité de 12 mois et peuvent être utilisés en plusieurs fois."),
]

NAV = [
    ("index.html", "Accueil"),
    ("index.html#categories", "Catégories"),
    ("cheque-cadeau.html", "Chèque cadeau"),
    ("listes.html", "Listes"),
    ("qui-sommes-nous.html", "Qui sommes-nous ?"),
    ("contact.html", "Contact"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def maps_url(s):
    q = f"The Grasshopper, {s['street']}, {s['zip']} {s['city']}".replace(" ", "+")
    return "https://www.google.com/maps/search/?api=1&query=" + q


def store_schema(s):
    return {
        "@type": "ToyStore",
        "@id": BASE_URL + "#" + s["id"],
        "name": s["name"],
        "url": BASE_URL,
        "image": BASE_URL + "assets/img/og-image.jpg",
        "logo": BASE_URL + "assets/img/icon-192.png",
        "telephone": s["tel"],
        "email": s["email"],
        "vatID": s["vat"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": s["street"],
            "postalCode": s["zip"],
            "addressLocality": s["city"],
            "addressCountry": "BE",
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": s["days"],
            "opens": s["opens"],
            "closes": s["closes"],
        }],
        "paymentAccepted": "Bancontact, carte de crédit, Paypal",
        "sameAs": [FACEBOOK, INSTAGRAM],
    }


def breadcrumb(name, path):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": name, "item": BASE_URL + path},
        ],
    }


def store_card(s, heading="h3"):
    note = f'<p class="store-note">{esc(s["hours_note"])}</p>' if s["hours_note"] else ""
    return f"""
<article class="store-card" id="{s['id']}">
  <div class="store-body">
    <{heading}>{esc(s['name'])}</{heading}>
    <address>
      {esc(s['street'])}<br>
      {s['zip']} {esc(s['city'])}
    </address>
    <p class="store-hours">{esc(s['hours'])}</p>
    {note}
    <ul class="store-links">
      <li><a href="tel:{s['tel']}">Tél. : {s['tel_display']}</a></li>
      <li><a href="mailto:{s['email']}">{s['email']}</a></li>
    </ul>
    <p class="store-vat">{s['vat_display']}</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="tel:{s['tel']}">Appeler</a>
      <a class="btn btn-ghost" href="{maps_url(s)}" target="_blank" rel="noopener">Itinéraire</a>
    </div>
  </div>
</article>"""


def layout(path, title, description, body, schema):
    url = BASE_URL + ("" if path == "index.html" else path)
    nav = "\n".join(
        '        <li><a href="{}"{}>{}</a></li>'.format(
            href, ' aria-current="page"' if href == path else "", label)
        for href, label in NAV
    )
    robots = "noindex, nofollow" if DEMO or path == "404.html" else "index, follow, max-image-preview:large"
    ld = json.dumps({"@context": "https://schema.org", "@graph": schema}, ensure_ascii=False, indent=2)
    b, l = STORES
    return f"""<!doctype html>
<html lang="fr-BE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#2f7d4f">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_BE">
<meta property="og:site_name" content="The Grasshopper">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{BASE_URL}assets/img/og-image.jpg">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip-link" href="#contenu">Aller au contenu</a>
<div class="topbar">
  <div class="container topbar-inner">
    <span>Bruxelles : ouvert tous les jours de 10 à 19 heures</span>
    <span class="topbar-sep" aria-hidden="true">•</span>
    <span>Louvain : du lundi au samedi de 10 à 18 heures</span>
  </div>
</div>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="The Grasshopper, accueil">
      <img src="assets/img/logo.webp" alt="" width="320" height="303">
      <span class="brand-text">
        <span class="brand-name">The Grasshopper</span>
        <span class="brand-tag">Magasin de jouets à Bruxelles et Louvain</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu">
      <span class="nav-toggle-bars" aria-hidden="true"></span>
      <span class="sr-only">Menu</span>
    </button>
    <nav id="menu" class="site-nav" aria-label="Navigation principale">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>
<main id="contenu">
{body}
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <p class="footer-brand">The Grasshopper</p>
      <p>Magasin de jouets à Bruxelles et Louvain</p>
      <ul class="social">
        <li><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
      </ul>
    </div>
    <div>
      <p class="footer-title">{esc(b['name'])}</p>
      <address>{esc(b['street'])}<br>{b['zip']} {esc(b['city'])}</address>
      <p><a href="tel:{b['tel']}">Tél. : {b['tel_display']}</a><br><a href="mailto:{b['email']}">{b['email']}</a></p>
      <p>{b['vat_display']}</p>
    </div>
    <div>
      <p class="footer-title">{esc(l['name'])}</p>
      <address>{esc(l['street'])}<br>{l['zip']} {esc(l['city'])}</address>
      <p><a href="tel:{l['tel']}">Tél. : {l['tel_display']}</a><br><a href="mailto:{l['email']}">{l['email']}</a></p>
      <p>{l['vat_display']}</p>
    </div>
    <div>
      <p class="footer-title">Informations</p>
      <ul class="footer-links">
        <li><a href="qui-sommes-nous.html">Qui sommes-nous ?</a></li>
        <li><a href="cheque-cadeau.html">Chèque cadeau</a></li>
        <li><a href="listes.html">Listes</a></li>
        <li><a href="conditions-generales.html">Conditions générales</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>The Grasshopper Brussels BV · Rue du Marché aux Herbes 39-43, 1000 Bruxelles, Belgique</p>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def page_header(title, intro=""):
    p = f'<p class="page-intro">{intro}</p>' if intro else ""
    return f"""<section class="page-head">
  <div class="container">
    <h1>{title}</h1>
    {p}
  </div>
</section>"""


# ---------------------------------------------------------------- pages

def home():
    cats = "\n".join(
        f"""      <li><a class="cat-card" href="{SHOP}{slug}" target="_blank" rel="noopener">
        <img src="assets/img/{img}" alt="Catégorie {esc(label)}" width="640" height="360" loading="lazy" decoding="async">
        <span class="cat-label">{esc(label)}</span>
      </a></li>"""
        for label, slug, img in CATEGORIES
    )
    faq = "\n".join(
        f"""      <details>
        <summary>{esc(q)}</summary>
        <p>{esc(a)}</p>
      </details>"""
        for q, a in FAQ
    )
    stores = "\n".join(store_card(s) for s in STORES)
    body = f"""<section class="hero">
  <div class="container hero-grid">
    <div class="hero-text">
      <p class="eyebrow">Bruxelles · Louvain</p>
      <h1>The Grasshopper, magasin de jouets à Bruxelles et Louvain</h1>
      <p class="lead">The Grasshopper, les plus beaux magasins de jouets de Bruxelles et de Louvain, vous souhaitent la bienvenue sur leur site.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="#categories">Voir les catégories</a>
        <a class="btn btn-ghost" href="#magasins">Nos magasins</a>
      </div>
    </div>
    <div class="hero-media">
      <img src="assets/img/magasin-1.webp" alt="Façade d'un magasin de jouets The Grasshopper" width="1000" height="667" fetchpriority="high">
      <img class="hero-badge" src="assets/img/magasin-2.webp" alt="Enseigne sauterelle The Grasshopper" width="458" height="720" loading="lazy" decoding="async">
    </div>
  </div>
</section>

<section class="notice">
  <div class="container notice-inner">
    <p><strong>Petit rappel :</strong> tous nos trésors ne se trouvent pas sur notre site. N'hésitez pas à <a href="contact.html">nous contacter</a> pour savoir si nous avons ce que vous recherchez.</p>
  </div>
</section>

<section class="section" id="categories">
  <div class="container">
    <h2>Catégories</h2>
    <ul class="cat-grid">
{cats}
    </ul>
  </div>
</section>

<section class="section section-alt">
  <div class="container about-grid">
    <div>
      <h2>Qui sommes-nous ?</h2>
      <p>The Grasshopper possède deux magasins physiques à Bruxelles et à Louvain. La toute première Grasshopper a été fondée par une mère souhaitant rassembler des jouets de qualité, des jeux, des gadgets amusants et de la décoration pour enfants venus du monde entier.</p>
      <a class="btn btn-ghost" href="qui-sommes-nous.html">En savoir plus</a>
    </div>
    <div class="duo">
      <a class="duo-card" href="cheque-cadeau.html">
        <h3>Chèque cadeau</h3>
        <p>Hésitez-vous quant aux envies ou besoins de votre bénéficiaire ? Offrez-lui un bon d'achat !</p>
      </a>
      <a class="duo-card" href="listes.html">
        <h3>Liste de naissance</h3>
        <p>Vous pouvez choisir vos propres cadeaux et avertir vos amis et famille via le site !</p>
      </a>
    </div>
  </div>
</section>

<section class="section" id="magasins">
  <div class="container">
    <h2>Nos magasins</h2>
    <div class="store-grid">
{stores}
    </div>
  </div>
</section>

<section class="section section-alt" id="questions">
  <div class="container narrow">
    <h2>Questions fréquentes</h2>
    <div class="faq">
{faq}
    </div>
    <p class="muted">Réponses extraites des <a href="conditions-generales.html">conditions générales</a>.</p>
  </div>
</section>"""
    schema = [
        {"@type": "WebSite", "@id": BASE_URL + "#site", "url": BASE_URL, "name": "The Grasshopper", "inLanguage": "fr-BE"},
        {"@type": "Organization", "@id": BASE_URL + "#organisation", "name": "The Grasshopper Brussels BV",
         "url": BASE_URL, "logo": BASE_URL + "assets/img/icon-192.png", "vatID": "BE0737840792",
         "email": "buy@thegrasshopper.be", "sameAs": [FACEBOOK, INSTAGRAM]},
        store_schema(STORES[0]),
        store_schema(STORES[1]),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]
    return layout(
        "index.html",
        "The Grasshopper | Magasin de jouets à Bruxelles et Louvain",
        "The Grasshopper, magasin de jouets à Bruxelles (Rue du Marché aux Herbes 39-43) et à Louvain. Jouets de qualité, jeux, peluches, puzzles, déguisements.",
        body, schema)


def about():
    body = page_header("Qui sommes-nous ?") + """
<section class="section">
  <div class="container about-page">
    <div class="prose">
      <p>The Grasshopper possède deux magasins physiques à Bruxelles et à Louvain. La toute première Grasshopper a été fondée par une mère souhaitant rassembler des jouets de qualité, des jeux, des gadgets amusants et de la décoration pour enfants venus du monde entier. Pour découvrir ces produits et rendre visite à nos fournisseurs, nous participons chaque année à différentes foires nationales et internationales.</p>
      <p>Dans nos magasins, nous proposons plusieurs milliers de produits différents, ce qui rend impossible la mise en ligne de tout notre assortiment. Avez-vous vu quelque chose dans l'un de nos magasins qui n'est pas disponible en ligne ? N'hésitez pas à nous envoyer un e-mail !</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="contact.html">Nous contacter</a>
        <a class="btn btn-ghost" href="index.html#magasins">Nos magasins</a>
      </div>
    </div>
    <div class="gallery">
      <img src="assets/img/magasin-1.webp" alt="Façade d'un magasin de jouets The Grasshopper" width="1000" height="667" loading="lazy" decoding="async">
      <img src="assets/img/magasin-2.webp" alt="Enseigne sauterelle The Grasshopper" width="458" height="720" loading="lazy" decoding="async">
      <img src="assets/img/magasin-3.webp" alt="Vitrine d'un magasin The Grasshopper dans une rue piétonne" width="1000" height="1333" loading="lazy" decoding="async">
    </div>
  </div>
</section>"""
    return layout(
        "qui-sommes-nous.html",
        "Qui sommes-nous ? | The Grasshopper, magasin de jouets",
        "The Grasshopper possède deux magasins physiques à Bruxelles et à Louvain : jouets de qualité, jeux, gadgets amusants et décoration pour enfants venus du monde entier.",
        body, [breadcrumb("Qui sommes-nous ?", "qui-sommes-nous.html"),
               {"@type": "AboutPage", "url": BASE_URL + "qui-sommes-nous.html", "name": "Qui sommes-nous ?", "inLanguage": "fr-BE"}])


def vouchers():
    cards = "\n".join(
        f"""      <li class="voucher">
        <span class="voucher-name">Chèque cadeau {v} euros</span>
        <span class="voucher-price">{v},00 €</span>
      </li>"""
        for v in VOUCHERS
    )
    body = page_header("Chèque cadeau", "Hésitez-vous quant aux envies ou besoins de votre bénéficiaire ? Offrez-lui un bon d'achat !") + f"""
<section class="section">
  <div class="container narrow">
    <div class="prose">
      <p>Nous envoyons le chèque-cadeau avec Bpost pour € 6,00, ou vous pouvez le retirer dans le magasin et payer sur place. Vous pouvez également réserver le bon au nom de votre bénéficiaire dans le magasin. Inscrivez-le dans la rubrique « note à ajouter » lorsque vous consultez votre panier.</p>
      <p>Si vous souhaitez un chèque-cadeau d'un montant différent, ce n'est pas un problème ! Il suffit de nous envoyer un courriel pour le commander.</p>
      <p class="callout">Les chèques-cadeaux ont une validité de 12 mois et peuvent être utilisés en plusieurs fois.</p>
    </div>
    <h2>Montants disponibles</h2>
    <ul class="voucher-grid">
{cards}
    </ul>
    <div class="btn-row">
      <a class="btn btn-primary" href="{SHOP}cadeaubon" target="_blank" rel="noopener">Commander sur la boutique en ligne</a>
      <a class="btn btn-ghost" href="mailto:buy@thegrasshopper.be">Demander un autre montant</a>
    </div>
  </div>
</section>"""
    return layout(
        "cheque-cadeau.html",
        "Chèque cadeau de 20 € à 200 € | The Grasshopper",
        "Offrez un chèque cadeau The Grasshopper : de 20 € à 200 €, valable 12 mois et utilisable en plusieurs fois. Envoi avec Bpost ou retrait dans le magasin.",
        body, [breadcrumb("Chèque cadeau", "cheque-cadeau.html")])


def lists():
    body = page_header("Liste de naissance") + f"""
<section class="section">
  <div class="container about-page">
    <div class="prose">
      <p>Avez-vous une liste de souhaits, attendez-vous un bébé, fêtez-vous bientôt une communion ou un anniversaire ? Vous pouvez choisir vos propres cadeaux et avertir vos amis et famille via le site ! Contactez-nous si vous souhaitez composer une liste et nous la composerons avec vous.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="contact.html">Composer une liste</a>
        <a class="btn btn-ghost" href="{SHOP}geboortelijsten" target="_blank" rel="noopener">Voir les listes sur le site</a>
      </div>
    </div>
    <div class="gallery gallery-two">
      <img src="assets/img/liste-1.webp" alt="Enfant endormi entouré de peluches" width="934" height="598" loading="lazy" decoding="async">
      <img src="assets/img/liste-2.webp" alt="Nouveau-né endormi dans un panier" width="1000" height="666" loading="lazy" decoding="async">
    </div>
  </div>
</section>"""
    return layout(
        "listes.html",
        "Liste de naissance et liste de souhaits | The Grasshopper",
        "Liste de naissance, communion ou anniversaire : choisissez vos propres cadeaux et avertissez vos amis et famille. The Grasshopper compose la liste avec vous.",
        body, [breadcrumb("Listes", "listes.html")])


def contact():
    stores = "\n".join(store_card(s, "h2") for s in STORES)
    body = page_header("Contact", "N'hésitez pas à nous contacter pour vos demandes ou remarques !") + f"""
<section class="section">
  <div class="container">
    <p class="prose center">Nous restons bien sûr à votre disposition soit par téléphone soit lors de votre visite dans nos établissements.</p>
    <div class="store-grid">
{stores}
    </div>
    <div class="contact-cta">
      <a class="btn btn-primary" href="mailto:buy@thegrasshopper.be">Écrire au magasin de Bruxelles</a>
      <a class="btn btn-primary" href="mailto:leuven@thegrasshopper.be">Écrire au magasin de Louvain</a>
    </div>
  </div>
</section>"""
    return layout(
        "contact.html",
        "Contact et horaires | The Grasshopper Bruxelles et Louvain",
        "Contactez The Grasshopper : Bruxelles, Rue du Marché aux Herbes 39-43, tél. 02/511 96 22. Louvain, Mechelsestraat 24a, tél. 016/297 997. Adresses et horaires.",
        body, [breadcrumb("Contact", "contact.html"),
               {"@type": "ContactPage", "url": BASE_URL + "contact.html", "name": "Contact", "inLanguage": "fr-BE"},
               store_schema(STORES[0]), store_schema(STORES[1])])


def terms():
    content = (ROOT / "content" / "conditions-generales.html").read_text(encoding="utf-8")
    toc = "\n".join(f'        <li><a href="#article-{i}">Article {i}</a></li>' for i in range(1, 13))
    body = page_header("Conditions générales") + f"""
<section class="section">
  <div class="container terms-grid">
    <nav class="toc" aria-label="Sommaire des conditions générales">
      <p class="toc-title">Sommaire</p>
      <ol>
{toc}
      </ol>
    </nav>
    <div class="prose terms">
{content}
    </div>
  </div>
</section>"""
    return layout(
        "conditions-generales.html",
        "Conditions générales de vente | The Grasshopper",
        "Conditions générales de la boutique en ligne The Grasshopper : prix, paiement, livraison par bpost ou DPD, garantie de 2 ans et droit de rétractation de 14 jours.",
        body, [breadcrumb("Conditions générales", "conditions-generales.html")])


def not_found():
    body = page_header("Page introuvable") + """
<section class="section">
  <div class="container narrow">
    <div class="btn-row">
      <a class="btn btn-primary" href="index.html">Accueil</a>
      <a class="btn btn-ghost" href="contact.html">Contact</a>
    </div>
  </div>
</section>"""
    return layout("404.html", "Page introuvable | The Grasshopper", "Page introuvable.", body, [])


PAGES = {
    "index.html": home,
    "qui-sommes-nous.html": about,
    "cheque-cadeau.html": vouchers,
    "listes.html": lists,
    "contact.html": contact,
    "conditions-generales.html": terms,
    "404.html": not_found,
}


def main():
    for name, fn in PAGES.items():
        (ROOT / name).write_text(fn(), encoding="utf-8", newline="\n")
    urls = "\n".join(
        f"  <url><loc>{BASE_URL}{'' if n == 'index.html' else n}</loc><lastmod>2026-09-29</lastmod></url>"
        for n in PAGES if n != "404.html"
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
        encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8", newline="\n")
    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": "The Grasshopper", "short_name": "Grasshopper", "lang": "fr-BE",
        "start_url": "./", "display": "browser", "background_color": "#fff8ec", "theme_color": "#2f7d4f",
        "icons": [{"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("OK :", ", ".join(PAGES))


if __name__ == "__main__":
    main()
