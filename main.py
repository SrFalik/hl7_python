import csv
import re
from datetime import datetime
from random import randint

LOC_ENVIO = "IBMEC"
RECEBEDOR = "CESAR"
LOC_RECEB = "CONCLINICA"
INICIO = "OBR|1|"
INICIO_DOIS = "OBX|1|SN|"
FINALMENTE = "<cr>"

listPront = []
listObr = []

header = {
                "INICIO": "MSH|^~\\&|",
                "ENVIANTE": "FALIK PROGRAM",
                "DATA": datetime.now().strftime("%Y%m%d%H%M%S"),
                "TIPO": "ORU^R01",
                "CONTROLE": "CNTRL-",
                "MISTERIO": "|P|",
                "VERSAO": "2.4"
            }

with open('Paciente.csv', encoding="utf8") as arquivo:
    with open('ProntuarioEndoscopia.csv', encoding="utf8") as arquivo2:
        arquivo_csv = csv.reader(arquivo, delimiter=";")
        for i, linha in enumerate(arquivo_csv):
            while len(linha) < 52:
                linha.append("NULL")
            if not i == 0:
                if not linha[1].upper() == "NULL":
                    cebola = linha[1].split()
                    cebola.reverse()
                    linha[1] = (' '.join(cebola))

                if not linha[10].upper() == "NULL":
                    cebola = linha[10].split("/")
                    cebola.reverse()
                    linha[10] = (' '.join(cebola).replace(" ", ""))
                if not linha[16] == "NULL":
                    linha[16] = re.sub('\\D', '', linha[16])
                if not linha[23] == "NULL":
                    linha[23] = re.sub('\\D', '', linha[23])
            paciente = {
                "CODIGO": linha[0].upper(),
                "NOME": linha[1].upper(),
                "NASCIMENTO": linha[10].upper(),
                "SEXO": linha[11].upper(),
                "LOGRADOURO": linha[43].upper(),
                "NUMERO": linha[45].upper(),
                "BAIRRO": linha[47].upper(),
                "CIDADE": linha[48].upper(),
                "UF": linha[49].upper(),
                "TELEFONE_CELULAR": linha[23].upper(),
                "RG": linha[16].upper(),
                "ORGAO_EMISSOR": linha[17].upper()
            }

            listPront.append(paciente)

            arquivo2_csv = csv.reader(arquivo2, delimiter=";")
            for j, linha2 in enumerate(arquivo2_csv):
                while len(linha2) < 41:
                    linha2.append("NULL")

                if not linha2[1] == "NULL":
                    cebola = linha2[1].split("/")
                    cebola.reverse()
                    linha2[1] = (' '.join(cebola).replace(" ", ""))

                req = {
                    "CODIGO": linha2[0],
                    "DATA": linha2[1],
                    "QUEIXA": linha2[2],
                    "HDA": linha2[3],
                    "HIPOTESE": linha2[28]
                }

                listObr.append(req)

with open('output.txt', 'w', encoding="utf8") as output:
    for paciente in listPront:
        for req in listObr:
            if paciente["CODIGO"] == req["CODIGO"]:
                print(header["INICIO"] + header["ENVIANTE"] + "|" + LOC_ENVIO + "|" + RECEBEDOR + "|" + LOC_RECEB + "|"
                      + header["DATA"] + header["TIPO"] + "|" + header["CONTROLE"] + str(randint(1000, 9999)) +
                      header["VERSAO"] + FINALMENTE, file=output)
                print("PID|||" +
                      paciente["CODIGO"] + "||" +
                      paciente["NOME"] + "|" +
                      paciente["NASCIMENTO"] + "|" +
                      paciente["SEXO"] + "|||" +
                      paciente["LOGRADOURO"] + "^" +
                      paciente["NUMERO"] + "^" +
                      paciente["BAIRRO"] + "^" +
                      paciente["CIDADE"] + "^" +
                      paciente["UF"] + "||" +
                      paciente["TELEFONE_CELULAR"] + "||" +
                      paciente["RG"] +
                      paciente["ORGAO_EMISSOR"] +
                      FINALMENTE, file=output)
                print(INICIO + str(randint(100000, 999999)) + "^" + LOC_RECEB + "|" + str(randint(10000, 99999)) +
                      "^" + LOC_ENVIO + "|||" + req["HDA"] + "||" + req["DATA"] + "|||||||||" + FINALMENTE, file=output)
                print(INICIO_DOIS + req["HIPOTESE"] + "|H|||F" + FINALMENTE, file=output)
                print("", file=output)
print("ARQUIVO SALVO EM: output.txt")

