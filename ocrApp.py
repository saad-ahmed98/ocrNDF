from flask import Flask
from flask import request,abort
import json
import os
import easyocr
import numpy as np
from dataFinder import *
import re

app = Flask("ocrApp")

@app.route("/")
def hello_world():
    return "<p>NDFocr</p>"

# views of the website, each function corresponds to a page
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def convert(o):
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError

@app.route("/ocr",methods=['POST'])
def easyOCR():
    if request.method == 'POST':
        query = request.files['img'].stream.read()
        if not query:
                abort(404)
        reader = easyocr.Reader(['fr', 'en'], gpu=False)

        resultatOCR = {
            "base64":{
                "value":""
            },
            "siret": {
                "value":"",
                "boxes":[]
            },
            "totalHT": {
                "value":"",
                "calculated":False,
                "boxes":[]
            },
            "totalTTC": {
                "value":"",
                "calculated":False,
                "boxes":[]
            },
            "totalTVA": {
                "value":"",
                "calculated":False,
                "boxes":[]
            },
            "categorie": {
                "value":""
                },
            "date": {
                "value":"",
                "boxes":[]
            },
        }

        boxHT = {
            "x1":0,
            "x2":0
        }

        boxTTC = {
            "x1":0,
            "x2":0
        }

        boxTVA = {
            "x1":0,
            "x2":0
        }

        errorManager = {
            "siret":3,
            "HT":2
        }
        findingSIRET = False
        findingHT = False
        findingTTC = False
        findingTVA = False
        result = reader.readtext(query, output_format='dict')
        for ob in result:
            if len(resultatOCR["categorie"]["value"]) == 0:
                catres = isCategorie(ob["text"].replace(":", ""))
                if len(catres) > 0:
                    resultatOCR["categorie"]["value"] = catres
            if len(resultatOCR["date"]["value"]) == 0:
                resultatOCR["date"]["value"] = isDate(ob["text"])
                resultatOCR["date"]["boxes"] = ob["boxes"]

            if isDataToFind(ob["text"].replace(":", ""), "SIRET"):
                resultatOCR["siret"]["boxes"] = ob["boxes"]
                findingSIRET = True
            
            if isDataToFind(ob["text"].replace(":", ""), "HT") and "TTC" not in ob["text"]:
                boxHT["x1"] = ob["boxes"][0][0]
                boxHT["x2"] = ob["boxes"][1][0]
                findingHT = True
                errorManager["HT"] = 3

            if findingHT and (((abs(ob["boxes"][0][0]-boxHT["x1"])<220 or ob["boxes"][0][0]>boxHT["x1"]) and ((abs(ob["boxes"][1][0]-boxHT["x2"])<220 or ob["boxes"][1][0]<boxHT["x2"]))) or errorManager["HT"]>0) :
                # verifie si toute la string est un chiffre
                try:
                    spl = ob["text"].replace(" ", "").replace(",",".").replace("€","")
                    res = float(spl)
                    if "." in spl:
                        resultatOCR["totalHT"]["value"] = res
                        resultatOCR["totalHT"]["boxes"] = ob["boxes"]
                        findingHT = False
                except:
                    None
                # verifie si un bout du string contient un chiffre
                if findingHT:
                    splitxt = ob["text"].replace(":", "").replace(",",".").replace("€","").split()
                    if len(splitxt) > 1:
                        for spl in splitxt:
                            try:
                                res = float(spl)
                                if "." in spl:
                                    resultatOCR["totalHT"]["value"] = res
                                    resultatOCR["totalHT"]["boxes"] = ob["boxes"]
                                    findingHT = False
                            except:
                                None                  
                if findingHT:
                    errorManager["HT"]-=1

            if isDataToFind(ob["text"].replace(":", ""), "TTC"):
                boxTTC["x1"] = ob["boxes"][0][0]
                boxTTC["x2"] = ob["boxes"][1][0]
                findingTTC = True
                errorManager["TTC"] = 3

            if findingTTC and (((abs(ob["boxes"][0][0]-boxTTC["x1"])<200 or ob["boxes"][0][0]>boxTTC["x1"]) and ((abs(ob["boxes"][1][0]-boxTTC["x2"])<200 or ob["boxes"][1][0]<boxTTC["x2"]))) or errorManager["TTC"]>0) :
                # verifie si toute la string est un chiffre
                try:
                    spl = ob["text"].replace(" ", "").replace(",",".").replace("€","")
                    res = float(spl)
                    if "." in spl:
                        resultatOCR["totalTTC"]["value"] = res
                        resultatOCR["totalTTC"]["boxes"] = ob["boxes"]
                        findingTTC = False
                except:
                    None
                # verifie si un bout du string contient un chiffre
                if findingTTC:
                    splitxt = ob["text"].replace(":", "").replace(",",".").replace("€","").split()
                    if len(splitxt) > 1:
                        for spl in splitxt:
                            try:
                                res = float(spl)
                                if "." in spl:
                                    resultatOCR["totalTTC"]["value"] = res
                                    resultatOCR["totalTTC"]["boxes"] = ob["boxes"]
                                    findingTTC = False
                            except:
                                None                  
                if findingTTC:
                    errorManager["TTC"]-=1

            if isDataToFind(ob["text"].replace(":", ""), "TVA"):
                boxTVA["x1"] = ob["boxes"][0][0]
                boxTVA["x2"] = ob["boxes"][1][0]
                findingTVA = True
                errorManager["TVA"] = 3

            if findingTVA and (((abs(ob["boxes"][0][0]-boxTVA["x1"])<200 or ob["boxes"][0][0]>boxTVA["x1"]) and ((abs(ob["boxes"][1][0]-boxTVA["x2"])<200 or ob["boxes"][1][0]<boxTVA["x2"]))) or errorManager["TVA"]>0) :
                # verifie si toute la string est un chiffre
                try:
                    spl = ob["text"].replace(" ", "").replace(",",".").replace("€","")
                    res = float(spl)
                    if "." in spl and "%" not in spl:
                        resultatOCR["totalTVA"]["value"] = res
                        resultatOCR["totalTVA"]["boxes"] = ob["boxes"]
                        findingTVA = False
                except:
                    None
                # verifie si un bout du string contient un chiffre
                if findingTVA:
                    splitxt = ob["text"].replace(":", "").replace(",",".").replace("€","").split()
                    if len(splitxt) > 1:
                        for spl in splitxt:
                            try:
                                res = float(spl)
                                if "." in spl and "%" not in splitxt:
                                    resultatOCR["totalTVA"]["value"] = res
                                    resultatOCR["totalTVA"]["boxes"] = ob["boxes"]
                                    findingTVA = False
                            except:
                                None                  
                if findingTVA:
                    errorManager["TVA"]-=1
            # lecture SIRET
            if findingSIRET:
                splitxt = ob["text"].replace(":", "").split()
                if len(splitxt) > 1:
                    for spl in splitxt:
                        if len(resultatOCR["siret"]["value"]) < 13 and errorManager["siret"] > 0:
                            regres = re.sub("[^0-9]", "", spl)
                            if len(regres) == 0:
                                errorManager["siret"] -= 1
                            resultatOCR["siret"]["boxes"] = updateSiretBox(resultatOCR["siret"]["boxes"],ob["boxes"])
                            resultatOCR["siret"]["value"] += regres
                else:
                    regres = re.sub("[^0-9]", "", ob["text"].replace(" ", ""))
                    if len(regres) == 0:
                        errorManager["siret"] -= 1
                    resultatOCR["siret"]["boxes"] = updateSiretBox(resultatOCR["siret"]["boxes"],ob["boxes"])
                    resultatOCR["siret"]["value"] += regres

            if errorManager["siret"] == 0:
                findingSIRET = False

            if len(resultatOCR["siret"]["value"]) >= 13 and findingSIRET:
                findingSIRET = False
        calculFini = False
        # si on connait les totaux HT et TTC, on calcule la TVA à la main
        if type(resultatOCR["totalHT"]["value"]) is float and type(resultatOCR["totalTTC"]["value"]) is float:
            if resultatOCR["totalTTC"]["value"]>resultatOCR["totalHT"]["value"]:
                resultatOCR["totalTVA"]["value"] = round(resultatOCR["totalTTC"]["value"]-resultatOCR["totalHT"]["value"],2)
                calculFini = True
                resultatOCR["totalTVA"]["calculated"] = True

        # si on connait les totaux TVA et TTC, on calcule le HT à la main
        if type(resultatOCR["totalTVA"]["value"]) is float and type(resultatOCR["totalTTC"]["value"]) is float and not calculFini:
            if resultatOCR["totalTTC"]["value"]>resultatOCR["totalTVA"]["value"]:
                resultatOCR["totalHT"]["value"] = round(resultatOCR["totalTTC"]["value"]-resultatOCR["totalTVA"]["value"],2)
                resultatOCR["totalHT"]["calculated"] = True
                calculFini = True

        # si on connait les totaux TVA et HT, on calcule le TTC à la main
        if type(resultatOCR["totalTVA"]["value"]) is float and type(resultatOCR["totalHT"]["value"]) is float and not calculFini:
            if resultatOCR["totalHT"]["value"]>resultatOCR["totalTVA"]["value"]:
                resultatOCR["totalTTC"]["value"] = round(resultatOCR["totalHT"]["value"]+resultatOCR["totalTVA"]["value"],2)
                resultatOCR["totalTTC"]["calculated"] = True
        resultatOCR["base64"]["value"] = drawDataOnImage(query,resultatOCR)
        jsonstring = json.dumps(resultatOCR, default=convert)
        return json.loads(jsonstring)
    abort(404)