"""
Diffie Hellman 

1. A i B uzgadniają ze sobą w sposób jawny wybór dwóch dużych liczb całkowitych
n – duża liczba pierwsza i g – pierwiastek pierwotny modulo n, i gdzie 1<g<n.
2. A wybiera losową dużą liczbę całkowitą x (tajną) – to będzie jej klucz prywatny i
oblicza X=g^x mod n
3. B wybiera losową dużą liczbę całkowitą y (tajną) – to będzie klucz prywatny
osoby B i oblicza Y=g^y mod n
4. A i B przesyłają do siebie nawzajem obliczone X i Y.
5. A oblicza k= Y x mod n
6. B oblicza k= X y mod n
7. Mogą teraz używać k jako klucza sesji (np. do algorytmu blokowego).

g - liczba ok. 300 cyfr
x i y - co najmniej 100 cyfr

zapewni to, że nie będziemy wstanie sprawdzić klucza prywatnego drugiej osoby


"""
from typing import Hashable
import random as rn
import graphviz

class Client:
    def __init__(self, id: Hashable, N: int, g: int) -> None:
        self.client_id = id
        self.N = N
        self.g = g
        self.private_key = None
        self.public_key = {}
        self.session_key = {}

    def generate_private_key(self):
        self.private_key = rn.randint(100000, 1000000)

    def generate_public_key(self):
        self.public_key[self.client_id] = (self.g**self.private_key) % self.N

    def receive_public_key(self, sender_id: Hashable, public_key: int):
        self.public_key[sender_id] = public_key

    def generate_session_key(self, sender_id: Hashable):
        self.session_key[sender_id] = self.public_key[sender_id]**self.private_key % self.N

def diffie_hellman(N: int, g: int):
    """
    N - liczba pierwsza, wybrana przez A i B
    g - pierwiastek pierwotny modulo N, liczba, której potęgi dają wszystkie możliwe reszty modulo N
    """

    steps = []
    graph = graphviz.Digraph(
        node_attr={'color': 'lightblue2', 'style': 'filled'}, 
        graph_attr={'bgcolor': 'transparent', 'fontcolor': 'white'},
        edge_attr={'color': 'white', 'fontcolor': 'white'},
    )

    A = Client('A', N, g)
    B = Client('B', N, g)

    A.generate_private_key()
    steps.append(f'{A.client_id} choose {A.private_key} as private key')

    B.generate_private_key()
    steps.append(f'{B.client_id} choose {B.private_key} as private key')

    A.generate_public_key()
    steps.append(f'{A.client_id} calculate public key {A.public_key[A.client_id]}')
    graph.node('A1', f'{A.client_id} \nx: {A.private_key}')
    graph.node('A2', f'{A.client_id} \nx: {A.private_key}   X: {A.public_key[A.client_id]}')

    B.generate_public_key()
    steps.append(f'{B.client_id} calculate public key {B.public_key[B.client_id]}')
    graph.node('B1', f'{B.client_id} \ny: {B.private_key}')
    graph.node('B2', f'{B.client_id} \ny: {B.private_key}   Y: {B.public_key[B.client_id]}')

    B.receive_public_key(A.client_id, A.public_key[A.client_id])
    steps.append(f'{A.client_id} sends public key to {B.client_id}')

    A.receive_public_key(B.client_id, B.public_key[B.client_id])
    steps.append(f'{B.client_id} sends public key to {A.client_id}')
    
    graph.node('A3', f'{A.client_id} \nx: {A.private_key}   X: {A.public_key[A.client_id]}\nY: {A.public_key[B.client_id]}')
    graph.node('B3', f'{B.client_id} \ny: {B.private_key}   Y: {B.public_key[B.client_id]}\nX: {B.public_key[A.client_id]}')

    A.generate_session_key(B.client_id)
    steps.append(f'{A.client_id} generates session key = {A.session_key[B.client_id]}')
    graph.node('A4', f'{A.client_id} \nx: {A.private_key}   X: {A.public_key[A.client_id]}\nY: {A.public_key[B.client_id]}   k: {A.session_key[B.client_id]}')

    B.generate_session_key(A.client_id)
    steps.append(f'{B.client_id} generates session key = {B.session_key[A.client_id]}')
    graph.node('B4', f'{B.client_id} \ny: {B.private_key}   Y: {B.public_key[B.client_id]}\nX: {B.public_key[A.client_id]}   k: {B.session_key[A.client_id]}')


    with graph.subgraph(name='cluster_0', graph_attr={'color': 'white'}) as c:
        c.edges([('A1', 'A2'), ('A2', 'A3'), ('A3', 'A4')])
        c.attr(label='Client A')

    with graph.subgraph(name='cluster_1', graph_attr={'color': 'white'}) as c:
        c.edges([('B1', 'B2'), ('B2', 'B3'), ('B3', 'B4')])
        c.attr(label='Client B')

    graph.edge('Start', 'A1')
    graph.edge('Start', 'B1')
    graph.edge('B2', 'A3', label=f'send Y')
    graph.edge('A2', 'B3', label=f'send X')

    return steps, graph