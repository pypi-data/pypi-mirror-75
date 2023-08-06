class Cnpj:
    def __init__(self):
        pass

    def validate(self, cnpj):
        lista_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        lista_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        cnpj = cnpj.replace("-", "")
        cnpj = cnpj.replace(".", "")
        cnpj = cnpj.replace("/", "")

        verif = cnpj[-2:]

        if len(cnpj) != 14:
            return False

        soma = 0
        id = 0
        for numero in cnpj:
            try:
                lista_um[id]
            except:
                break

            soma += int(numero) * int(lista_um[id])
            id += 1

        soma = soma % 11
        if soma < 2:
            digito_um = 0
        else:
            digito_um = 11 - soma

        digito_um = str(digito_um)

        soma = 0
        id = 0

        for numero in cnpj:
            try:
                lista_dois[id]
            except:
                break

            soma += int(numero) * int(lista_dois[id])
            id += 1

        soma = soma % 11
        if soma < 2:
            digito_dois = 0
        else:
            digito_dois = 11 - soma

        digito_dois = str(digito_dois)

        if bool(verif == digito_um + digito_dois) == True:
            print(Cnpj().format(cnpj))
        else:
            print("CNPJ Incorreto!")

    def format(self, cnpj):
        return "%s.%s.%s/%s-%s" % (cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14])



