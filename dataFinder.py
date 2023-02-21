from unidecode import unidecode
import re
from PIL import Image, ImageDraw, ImageOps, ImageFont
import io
from io import BytesIO
import base64

categorie = {
    "restauration": ["restaurant", "cafe", "buvette", "cabaret", "bar", "bistrot", "restauration", "fast-food", "grill-room", "rotisserie", "self-service", "cremerie", "grillade", "pizzeria", "menu", "terrasse", "magasin", "salle", "discotheque", "cuisinier", "brasserie", "addition", "pizza", "gastronomie", "boulangerie", "restaurateur", "mcdonald's", "garcon", "chef", "crêperie", "buffet", "snack", "resto", "poulet", "grill", "mcdo", "vegetarien", "serveur", "dejeuner", "casse-croûte", "menu", "taverne", "diner", "routier", "traiteur", "pub", "restoroute", "bouillon", "gastronomique", "palace", "restau", "sommelier", "table", "serveuse", "reservation", "snack-bar", "resto-bar", "cantine", "aire de restauration", "asiatique", "chinois", "nombre", "dessert", "hamburger", "plat du jour", "sushi", "pâtissier", "tapas", "vietnamien", "guinguette", "mcdo", "refectoire", "huitres", "manger", "Burger King", "assiette", "boissons", "bouillabaisse", "friterie", "grec", "quick", "cafetiere", "cafeine", "tasse", "chocolat", "expresso", "the", "creme", "jus", "moulu", "lait", "cacao", "comptoir", "noisette", "boire", "grain", "arome", "decafeine", "cafe au lait", "tiramisu", "vanille", "cappuccino", "latte", "cannelle", "cerise", "croissant", "tartine", "biscuit", "caramel", "chaude", "muffin", "petit", "noir", "Starbucks", "biere", "irish", "coffee", "noix", "cafetard", "leffee", "nespresso", "banane", "cafe", "filtre", "cafe-concert", "canne a sucre", "coffee", "liquide", "crevettes", "ananas", "espresso", "rhum", "nestle", "cafe", "noir", "riz", "epice", "gamelle", "macchiato", "pousse-cafe", "repas", "frappe", "aromatique", "confiture", "gobelet", "saveur", "petit-dejeuner", "soupe", "cafe", "americain", "capuccino", "nescafe", "glace", "glaces", "sauce", "raisin", "citron", "sirop", "formule", "vinaigre", "orange", "fruit", "limonade", "pulpe", "tomate", "fermente", "presse", "pamplemousse", "betterave", "grenadine", "soda", "sodas", "huile", "abricot", "ail", "marinade", "oignon", "persil", "bouillir", "citronnade", "grenade", "litchi", "grappe", "mandarine", "canette", "cocktail", "framboise", "poire", "coriandre", "fermentation", "gingembre", "mangue", "volaille", "concombre", "citron", "piment", "legumes", "melange", "cola", "salade", "sel", "mayonnaise", "olive", "viande", "veau", "beurre", "carottes", "datte", "bœuf", "boeuf", "cacahuete", "yaourt", "smoothie", "huile", "mate", "the", "menthe"],
    "transports": ["transports", "transporteur", "logistique", "routier","auto", "autobus", "autocar", "deplacement", "ferroviaire", "vehicule", "circulation", "tramway", "voiture", "taxi", "train", "metro", "avion", "transport en commun", "aerien", "bateau", "camion", "automobile", "ratp", "sncf", "bus", "navette", "tarif", "terminus", "velo", "passager", "port", "autoroute", "tgv", "aeroport", "gare", "fourgon", "minibus", "billetterie", "van", "voyage", "carburant", "vol", "route", "tram", "garage", "aller-retour", "essence", "gasoil", "plomb", "stationnement", "parking", "souterrain", "payant", "peage", "aire de stationnement", "location"],
    "commerce": ["magasin", "supermarche", "hypermarche", "epicerie", "caissier", "casino", "superette", "carrefour", "auchan", "centre", "commercial", "leclerc", "aldi", "alimentaire", "bio", "surface", "produit", "caisse", "Intermarche", "surgele", "danette", "danone", "vanille", "chocolat", "dessert", "saveur", "creme", "lait", "fermente", "parfum", "cacao", "cafe", "boisson", "alcool", "biere", "vin", "limonade", "jus", "the", "eau", "gazeuse", "sirop", "citron", "sucre", "coca-cola", "gingembre", "vodka", "cannelle", "pepsi", "soja", "poivre", "safran", "miel", "menthe", "moutarde", "riz", "pattes", "article", "articles", "poulet", "vinaigre", "concombre", "brocoli", "poire", "huile", "pomme", "saucisses", "veloute", "anchois", "herbes", "sel", "mayonnaise", "olive", "viande", "veau", "beurre", "carottes", "datte", "mangue", "volaille", "framboise", "orange", "litchi", "grappe", "mandarine", "oignon", "persil", "abricot", "ail", "pamplemousse", "betterave", "banane", "pain", "croissant", "raisins", "nutella", "fraise", "œufs", "cerise", "biscuit", "chips", "tomate"],
    "hebergement": ["hebergement", "gite", "hotellerie", "hotel", "auberge", "location", "lit", "double", "hotelier", "hoteliere", "logement", "sejours", "meuble", "abri", "airbnb", "camping", "reservation", "chalet", "reception", "residence"]
}

regexdatelitteral = "^[0-9]{1,2}(?:janvier|fevrier|mars|avril|mai|juin|aout|septembre|octobre|novembre|decembre)[0-9]{2,4}$"
mois = ["janvier","fevrier","mars","avril","mai","juin","aout","septembre","octobre","novembre","decembre"]
dataToFind = {
    "TTC": ["T.T.C.", "TTC", "ITC", "TIC","T.T.C"],
    "TVA": ["TVA", "T.V.A", "TWA", "TWAA", "1WA", "1VA", "IVA", "TYA", "TY=A", "TVAA", " WA", " VA", "VRA", "TUA", "TOA"],
    "HT": ["HT","NET", "H.T.", "H.T","HT", "H,T,", "H,T","HI", "H.I.", "H.I", "H1", "HF", "H|"],
    "SIRET": ["SIRET", "BIRET", "SIREN", "S1RET", "S1RE1", "SIRE1", "SIRE1"],
    "NAF": ["NAF", "NAT", "MAF", "MAT", "WIF"]
}


def isDataToFind(v, key):
    value = v.upper()
    if value in dataToFind[key]:
        return True
    splitval = value.split()
    for spl in splitval:
        if spl in dataToFind[key]:
            return True
        if len(spl) == len(key):
            if len(lcs(spl, key)) >= 3:
                return True
    if value.replace(" ", "") in dataToFind[key]:
        return True
    return False


def isCategorie(value):
    splitval = value.split()
    for k in categorie:
        for spl in splitval:
            if unidecode(spl.lower()) in categorie[k]:
                return k
            for val in categorie[k]:
                if abs(len(spl)-len(val)) < 2:
                    if len(lcs(unidecode(spl.lower()), val)) >= len(val) and len(spl) > 3:
                        return k
    return ""


def isDate(value):
    spl = value.replace(" ", "")
    # dates au format jj/mm/yy ou jj/mm/yyyy uniquement
    found = re.search("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{2,4}$", spl)
    if found is not None:
        return found.group(0)

    # dates au format jj-mm-yy ou jj-mm-yyyy uniquement
    found = re.search("^[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{2,4}$", spl)
    if found is not None:
        return found.group(0).replace("-","/")
    #dates au format jj mois yyyy
    found = re.search(regexdatelitteral, unidecode(spl.lower()))
    if found is not None:
        return dateConverter(found.group(0))
    return ""

def dateConverter(val):
    spl = re.split(r'\D+',val)
    return spl[0]+"/"+str(mois.index(re.sub(r'[0-9]+', '', val))+1).zfill(2)+"/"+spl[1]

def lcs(S, T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = []
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = []
                    longest = c
                    lcs_set.append(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.append(S[i-c+1:i+1])
    if len(lcs_set) > 0:
        lcs_set.sort(key=len, reverse=True)
        return lcs_set[0]
    return ""

def drawDataOnImage(image_data,resOCR):
    og_image = Image.open(io.BytesIO(image_data))
    image = ImageOps.exif_transpose(og_image)
    draw = ImageDraw.Draw(image)
    
    siret = resOCR["siret"]["boxes"]
    tva = resOCR["totalTVA"]["boxes"]
    ht = resOCR["totalHT"]["boxes"]
    ttc = resOCR["totalTTC"]["boxes"]
    date = resOCR["date"]["boxes"]
    #font = ImageFont.truetype("Acme-Regular.ttf", size=200)

    if len(siret)>0:
        draw.polygon(((siret[0][0], siret[0][1]), (siret[1][0], siret[1][1]), (siret[2][0], siret[2][1]),(siret[3][0], siret[3][1])),
                    outline="yellow",width=15)
        #draw.text((siret[0][0],siret[0][1]), "SIRET", (255,255,0),font=font)
    if len(ht)>0:
        draw.polygon(((ht[0][0], ht[0][1]), (ht[1][0], ht[1][1]), (ht[2][0], ht[2][1]),(ht[3][0], ht[3][1])),
                    outline="red",width=15)
        #draw.text((ht[0][0],ht[0][1]), "HT", (255, 99, 71),font=font)
    if len(ttc)>0:
        draw.polygon(((ttc[0][0], ttc[0][1]), (ttc[1][0], ttc[1][1]), (ttc[2][0], ttc[2][1]),(ttc[3][0], ttc[3][1])),
                    outline="green",width=15)
        #draw.text((ttc[0][0],ttc[0][1]), "TTC", (0,255,0),font=font)

    if len(tva)>0:
        draw.polygon(((tva[0][0], tva[0][1]), (tva[1][0], tva[1][1]), (tva[2][0], tva[2][1]),(tva[3][0], tva[3][1])),
                    outline="purple",width=15)
        #draw.text((tva[0][0],tva[0][1]), "TVA", (128,0,128),font=font)

    if len(date)>0:
        draw.polygon(((date[0][0], date[0][1]), (date[1][0], date[1][1]), (date[2][0], date[2][1]),(date[3][0], date[3][1])),
                    outline="blue",width=15)
        #draw.text((date[0][0],date[0][1]), "DATE", (0,0,255),font=font)

    image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
    #image.save("res.jpg")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('ascii')


def updateSiretBox(box,newbox):
    finalbox = [[],[],[],[]]
    if box[0][0]<newbox[0][0]:
        finalbox[0] = box[0]
        finalbox[3] = box[3]
    else :
        finalbox[0] = newbox[0]
        finalbox[3] = newbox[3]

    if box[1][0]>newbox[1][0]:
        finalbox[1] = box[1]
        finalbox[2] = box[2]
    else :
        finalbox[1] = newbox[1]
        finalbox[2] = newbox[2]
    return finalbox
