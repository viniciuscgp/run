def signal(valor):
    if valor < 0:
        return -1
    elif valor == 0:
        return 0
    else:
        return 1


def consume(valor, fric):
    if fric == 0:
        return valor

    sinal = signal(valor)
    valor = abs(valor)

    if abs(valor) > 0:
        valor -= fric
        if valor < 0:
            valor = 0
    return valor * sinal
