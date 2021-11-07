print("Criando arquivo:")
f = open("nomes.txt", "r")
for n in range(1, 5):
    linha = f.readline().strip()
    cols = linha.split("|")
    print("Nome:{} Valor:{}".format(cols[0], cols[1]))

f.close()
print("Finalizado!!!")
