from queue import Queue
from collections import namedtuple
import json

class MenuItem:
    def __init__(self, nombre:str, precio:float):
        self.nombre = nombre
        self.precio = precio

    def copy(self):
        return self.__class__(self.nombre, self.precio)

class Bebidas(MenuItem):
    def __init__(self, nombre, precio, tamaño:int = 0):
        super().__init__(nombre, precio)
        self.tamaño = tamaño
        if tamaño == 1:
            self.precio += 2000
            self.nombre += " Mediano"
        elif tamaño ==2:
            self.nombre += " Grande"
            self.precio += 3000
        #Aumenta el precio de la bebida dependiendo del tamaño

    def set_precio (self, precio):
        self.precio = precio
        
    def set_tamaño (self, tamaño):
        self.tamaño = tamaño
        if tamaño == 1:
            self.precio += 2000
            self.nombre = f"{self.nombre} Mediano"
        elif tamaño ==2:
            self.nombre = f"{self.nombre} Grande"
            self.precio += 3000
        else:
            self.nombre = f"{self.nombre}"
            self.nombre = f"{self.precio}"
        return self

    def get_precio (self):
        return self.precio
    def get_nombre (self):
        return self.nombre
    def get_tamaño (self):
        return self.tamaño

class Entradas(MenuItem):
    def __init__(self, nombre, precio, personas:int = 0):
        super().__init__(nombre, precio)
        self.personas = personas
        self.precio *= personas

    def set_nombre (self, nombre):
        self.nombre = nombre
    def set_precio (self, precio):
        self.precio = precio
    def set_personas (self, personas):
        self.precio /= self.personas
        self.precio *= personas
        self.personas = personas
        return

    def get_nombre (self):
        return self.nombre
    def get_precio (self):
        return self.precio
    def get_personas (self):
        return self.personas

class PlatoFuerte(MenuItem):
    def __init__(self, nombre, precio, sopa:bool = True):
        super().__init__(nombre, precio)
        if sopa:
            self.precio += 8000
            self.nombre += " con sopa"
        #Aumenta el precio del plato fuerte si se pide con sopa
    
    def set_nombre (self, nombre):
        self.nombre = nombre
        if self.sopa:
            self.nombre += " con sopa"
    def set_precio (self, precio):
        self.precio = precio
    def set_sopa (self, sopa):
        self.sopa = sopa
        if sopa:
            self.precio += 8000
            self.nombre += " con sopa"
        else:
            self.precio -= 8000
            self.nombre = f"{self.nombre}"
        return self

    def get_nombre (self):
        return self.nombre
    def get_precio (self):
        return self.precio
    def get_sopa (self):
        return self.sopa

class Postre(MenuItem):
    def __init__(self, nombre, precio, porcion:int = 0):
        super().__init__(nombre, precio)
        self.porcion = porcion
        self.precio *= porcion
        if porcion >= 10:
            self.precio *= 0.75
        #si hay 10 porciones del mismo postre, 25% de descuento

    def set_nombre (self, nombre):
        self.nombre = nombre
    def set_precio (self, precio):
        self.precio = precio
    def set_porcion (self, porcion):
        self.precio /= self.porcion
        self.precio *= porcion
        if porcion >= 10:
            self.precio *= 0.75
        self.porcion = porcion
        return self

class Orden:
    def __init__(self):
        self.orden = []
        #crea una lista vacia
    def ordenar(self, item:"MenuItem"):
        self.orden.append(item)
        #Añade el item a la lista
    def precio_total(self):
        total = 0
        print("Orden:")
        for i in self.orden:
            total += i.precio
            print(f"{i.nombre}\t\t\t${i.precio}")
        print(f"Precio total:\t\t\t${total}")
        self.total = total
        return int(total)
        #Itera por la lista, imprime los productos con su precio y su suma

    def calcular_descuentos(self):
        a = 0
        b = 0
        for i in self.orden:
            if isinstance(i, Bebidas):
                a += 1
                if a == 2:
                    i.precio *= 0.5
                    print(f"Descuento 50% en: {i.nombre}")
                    #Descuento del 50% a la segunda bebida
            if isinstance(i, PlatoFuerte):
                b += 1
                if b == 10:
                    i.precio = 0
                    print(f"{i.nombre} es el décimo plato fuerte, por lo que la casa invita!")
                    #Un plato fuerte gratis si se ordenaron 10 o mas

class MetodoDePago:
    def __init__(self):
        pass

class Tarjeta(MetodoDePago):
    def __init__(self, nombre, numero, cvv):
        self.__nombre = nombre
        self.__numero = numero
        self.__cvv = cvv

    def pagar (self, monto):
        print(f"Se confirma pago de {monto} a nombre de {self.__nombre}, con la tarjeta numero *******{self.__numero[-4::]}.")

class Efectivo(MetodoDePago):
    def __init__(self, monto_entregado):
        self.monto_entregado = int(monto_entregado)
    def pagar (self, monto):
        if self.monto_entregado == monto:
            print("Pago completado")
        elif self.monto_entregado >= monto:
            vueltas = self.monto_entregado - monto
            print(f"Se reciben {self.monto_entregado} para pagar {monto}. Se devuelven {vueltas}")
        else:
            faltante = monto - self.monto_entregado
            print(f"Faltan {faltante}. Tocó lavar platos")

def crear_menu():
    nombre = input("¿Cómo quieres llamar este menú?")
    tipos = ("Bebidas", "Entradas", "Platos_fuertes", "Postres")
    Menu = namedtuple("Menu", ("productos", "precios", "tipos", "Nombre"))
    menu = Menu([], [], [], nombre)
    while True:
        tipo = int(input("""
              ¿Qué tipo de alimento deseas añadir al menú?
              0. Bebida
              1. Entrada
              2. Plato fuerte
              3. Postre"""))
        menu.tipos.append(tipos[tipo])
        nombre_prod = input("¿Qué nombre tiene el producto?")
        menu.productos.append(nombre_prod)
        precio = input("¿Qué precio tiene?")
        menu.precios.append(precio)

        otro_producto = input("¿Quieres agregar otro producto?\n0. No\n1. Si")
        while otro_producto not in ("0", "1"):
            otro_producto = input("Ingresa un número válido\n0. No\n1. Si")
        if otro_producto == "0":
            return menu_to_dict(menu)
        
def menu_to_dict(menu:namedtuple):
    menu_dict = {"Bebidas" : {}, "Entradas" : {},
                 "Platos_fuertes" : {}, "Postres" : {}}
    for i in range (len(menu.productos)):
        menu_dict[f"{menu.tipos[i]}"][f"{menu.productos[i]}"] = menu.precios[i]
    menu_dict["Nombre"] = menu.Nombre
    with open("menus.json", "r", encoding = "utf-8") as yeison:
        menus = json.load(yeison)
        menus.append(menu_dict)
    with open("menus.json", "w", encoding = "utf-8") as yeison:
        menus = json.dump(menus, yeison, indent = 2)
    return menu_dict

def editar_menu():
    with open("menus.json", "r", encoding = "utf-8") as yeison:
        menus = json.load(yeison)
    print("¿Qué menú deseas editar?")
    for i in range (len(menus)):
        print(f"{i}. {menus[i]["Nombre"]}")
    indice_menu = int(input())
    print(f"""¿Qué quieres hacer con el menu {menus[indice_menu]["Nombre"]}
0. Eliminarlo
1. Editar productos""")
    accion = int(input())
    if accion == 0:
        menus.pop(indice_menu)
    else:
        print(f"Este es el menu actual:\n {menus[indice_menu]}")
        while True:
            editar = int(input("""Qué quieres editar?
                  0. Bebidas
                  1. Entradas
                  2. Platos fuertes
                  3. Postres
                  4. Nombre
                      """))
            tipo_platos = ("Bebidas", "Entradas", "Platos_fuertes", "Postres")
            if editar == 4:
                nuevo_nombre = input("Ingresa el nuevo nombre: ")
                menus[indice_menu]["Nombre"] = nuevo_nombre
            elif editar in (0,1,2,3):
                for n, prod in enumerate(menus[indice_menu][tipo_platos[editar]]):
                    print(f"{n}. Editar {prod}?")
                producto = int(input())
                atributo = int(input("Qué desea editar?\n0. Nombre\n1. Precio"))
                if atributo == 0:
                    n_nombre = input("¿Qué nombre deseas colocarle?")
                    precio = menus[indice_menu][tipo_platos[editar]].pop(producto)
                    menus[indice_menu][tipo_platos[editar]][n_nombre] = precio
                if atributo == 1:
                    n_precio = input("¿Qué precio quieres que tenga ahora el producto:")
                    menus[indice_menu][tipo_platos[editar]][n_nombre] = n_precio
    with open("menus.json", "w", encoding = "utf-8") as yeison:
        json.dump(menus, yeison, indent = 2)

def proceso_pedidos(menu = None):
    if menu == None:
        menu = dict(Bebidas = dict(Jugo = 5000, Malteada = 8000, Limonada = 7000),
                    Entradas = dict(Empanada = 5000, Palitos_de_queso = 5000),
                    Platos_fuertes = dict(Pollo = 18000, Costillas = 21000, Pasta = 17000),
                    Postres = dict(Cheesecake = 8000, Helado = 5000),
                    Nombre = "Menu Default")

    print("""
        Bienvenido.
        Para elegir su comida, ingrese los índices de los productos
        separados por espacios. Para elegir las demás opciones,
        digite el número separado de un punto.
        (Ejemplo: Limonada mediana -> 2.1):
        """)


    fila_ordenes = Queue(maxsize = 5)
    ordenar = True
    while ordenar == True:  

        productos = []
        print("\tBebidas:")
        n = 0
        for a, b in menu["Bebidas"].items():
            productos.append(Bebidas(a, b))
            print(f"\t{n}. {a}\t -------- {b}")
            n+=1
        print("""\tTamaño:
                    0. Pequeño
                    1. Mediano
                    2. Grande
            
            Entradas:""")

        for a, b in menu["Entradas"].items():
            productos.append(Entradas(a, b))
            print(f"\t{n}. {a}\t -------- {b}\n")
            n+=1
        print("""\tPorciones:
                    # Porciones
            
            Plato principal:""")

        for a, b in menu["Platos_fuertes"].items():
            productos.append(PlatoFuerte(a, b))
            print(f"\t{n}. {a}\t -------- {b}\n")
            n+=1
        print("""\tSopa:
                    0. No
                    1. Si
            
            Postre:""")
        
        for a, b in menu["Postres"].items():
            productos.append(Postre(a, b))
            print(f"\t{n}. {a}\t -------- {b}\n")
            n+=1
        print("""\tPorciones:
                    # Porciones""")
        
        pedido = input("Ingresa tu pedido: ")
        pedido = pedido.split()

        orden = Orden()
        for i in pedido:
            i_splited = list(map(int, i.split(".")))
            if len(i_splited) == 2:
                if isinstance(productos[i_splited[0]], Bebidas):
                    bebida = productos[i_splited[0]].copy().set_tamaño(i_splited[1])
                    orden.ordenar(bebida)
                elif isinstance(productos[i_splited[0]], Entradas):
                    entrada = productos[i_splited[0]].copy().set_personas(int(i_splited[1]))
                    orden.ordenar(entrada)
                elif isinstance(productos[i_splited[0]], PlatoFuerte):
                    plato_fuerte = productos[i_splited[0]].copy().set_sopa(bool(int(i_splited[1])))
                    orden.ordenar(plato_fuerte)
                else:
                    postre = productos[i_splited[0]].copy().set_porcion(int(i_splited[1]))
                    orden.ordenar(postre)
            else:
                orden.ordenar(productos[i])

        fila_ordenes.put(orden)

        opcion = input("""¿Vas a hacer una orden más o ya vas a pagar?
                        1. Ordenar algo más
                        2. Pagar
                        """)
    
        if fila_ordenes.full():
            print("Ya pediste mucho, paga porfa.")
            break
        
        if opcion == "2":
            ordenar = False
        elif opcion != "1":
            print(f"¿{opcion}? muy chistoso, ahora paga.")
            ordenar = False

    while not fila_ordenes.empty():

        orden_pagar = fila_ordenes.get()
        orden_pagar.calcular_descuentos()
        orden_pagar.precio_total()
        print("""
        Qué método de pago desea usar?
            0. Efectivo
            1. Tarjeta
        """)
        metodo = int(input())
        if metodo == 0:
            monto_entregado = input("Ingrese la cantidad de efectivo que va a entregar")
            pago = Efectivo(monto_entregado)
            pago.pagar(int(orden_pagar.precio_total()))
        else:
            nombre = input("Ingrese a nombre de quien está la tarjeta")
            numero = input("Ingrese el numero de la tarjeta")
            cvv = input("Ingrese el CVV de la tarjeta")
            pago = Tarjeta(nombre, numero, cvv)
            pago.pagar(int(orden_pagar.precio_total()))

if __name__ == "__main__":

    inicio = int(input("""Hola, ¿vas a hacer un pedido, a crear o editar lo menús?
                   0. Crear menú
                   1. Editar menus
                   2. Realizar pedido"""))

    if inicio == 0:
        crear_menu()
    elif inicio == 1:
        editar_menu()
    elif inicio == 2:
        print("¿Con cuál menú quieres hacer tu pedido?")
        proceso_pedidos()