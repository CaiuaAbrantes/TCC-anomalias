from collections import deque

lista = deque(maxlen=2)
lista.append(2)
lista.append(3)
print(len(lista))
print(lista[len(lista)-1])
lista.pop()
print(lista)
