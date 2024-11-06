#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import lxml

# lineas para evitar error SSL
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

#----------------CARGAR

url="https://www.vinissimus.com/es/vinos/tinto/?cursor="

def cargar():
    respuesta= messagebox.askyesno("Cargar Datos", "¿Esta seguro de cargar los datos en la BBDD?")
    if respuesta:
        almacenar_bd()
   
def almacenar_bd():
    conn= sqlite3.connect("vinos.db")
    conn.text_factory=str
    conn.execute("DROP TABLE IF EXISTS VINOS")
    conn.execute("DROP TABLE IF EXISTS UVAS")
    conn.execute('''CREATE TABLE VINOS(
    VINO    TEXT NO NULL,
    PRECIO    REAL,
    DENOMINACION    TEXT,
    BODEGA    TEXT,
    UVA    TEXT);
    ''')
    conn.execute('''
    CREATE TABLE UVAS
    (NOMBRE TEXT NO NULL);
    ''')
    listaVinos,listaUvas=extraerDatos()
    print(listaVinos)
    for vino in listaVinos:
        conn.execute('''INSERT INTO VINOS VALUES (?,?,?,?,?)''',vino)
    for uva in listaUvas:
        conn.execute('''INSERT INTO UVAS (NOMBRE) VALUES (?)''',(uva,))
    conn.commit()
    cursor=conn.execute("SELECT COUNT(*) FROM VINOS").fetchone()[0]
    messagebox.showinfo("Tabla vinos", "La tabla vinos ha sido poblada con "+str(cursor)+" registros.")
    cursor=conn.execute("SELECT COUNT(*) FROM UVAS").fetchone()[0]
    messagebox.showinfo("Tabla uvas", "La tabla uvas ha sido poblada con "+str(cursor)+" registros.")
    conn.close()
    
def extraerDatos():
    listaVinos=[]
    setUvas=set()
    listaTodos=[]
    for i in range(0,3):
        urlSec=url+str(i*36)
        f=urllib.request.urlopen(urlSec)
        s=BeautifulSoup(f,"lxml")
        listaUnaPagina=s.find_all("div",class_="product-list-item")
        listaTodos.extend(listaUnaPagina)
    for dato in listaTodos:
        informacion=dato.find("div",class_="details")
        nombre=informacion.find("h2",class_="title heading").text
        denominacion=informacion.find("div",class_="region").text
        bodega=informacion.find("div",class_="cellar-name").text
        tiposUva=informacion.find("div",class_="tags").text
        setUvas=extraerDatosUvas(setUvas,tiposUva)
        tiposUva = ' '.join(tiposUva.split())
        precio = list(dato.find("p",class_=["price"]).stripped_strings)[0]
        #si tiene descuento el prcio es el del descuento
        dto = dato.find("p",class_=["price"]).find_next_sibling("p",class_="dto")
        if dto:
            precio = list(dto.stripped_strings)[0]
        print(precio)
        precio= float(precio.replace("€"," ").replace(",",".").strip())
        listaVinos.append((nombre,precio,denominacion,bodega,tiposUva))
        
    return listaVinos,setUvas

def extraerDatosUvas(setUvas,uvasNuevas):
    uvas=uvasNuevas.split("/")
    for u in uvas:
        setUvas.add(u.strip())
    return setUvas

#----------------CARGAR PRUEBA

def almacenar_bd_Prueba():
    listaVinos=[('Pago de Carraovejas 2021', 81.4, 'Ribera del Duero (España)', 'Bodega Pago de Carraovejas', 'Tempranillo / Cabernet sauvignon / Merlot'), ('Ultreia Saint Jacques 2021', 11.7, 'Bierzo (España)', 'Raúl Pérez Viticultor', 'Mencía'), ('Aalto 2022', 79.9, 'Ribera del Duero (España)', 'Aalto', 'Tempranillo'), ('El Enemigo Malbec 2021', 22.95, 'Mendoza (Argentina)', 'Bodega Aleanna', 'Malbec / Cabernet franc / Petit verdot'), ('Ramón Bilbao Crianza 2021', 9.95, 'Rioja (España)', 'Bodegas Ramón Bilbao', 'Tempranillo'), ('Lindes de Remelluri Viñedos de Labastida 2020', 18.9, 'Rioja (España)', 'Granja Ntra. Sra de Remelluri', 'Tempranillo / Garnacha / Graciano'), ('Pago de los Capellanes Roble 2023', 15.5, 'Ribera del Duero (España)', 'Pago de los Capellanes', 'Tempranillo'), ('Emilio Moro 2021', 13.9, 'Ribera del Duero (España)', 'Emilio Moro', 'Tempranillo'), ('Pago de Valdoneje Mencía 2023', 8.35, 'Bierzo (España)', 'Vinos Valtuille', 'Mencía'), ('Catena Malbec 2022', 29.9, 'Mendoza (Argentina)', 'Bodega Catena Zapata', 'Malbec'), ('Valtravieso Finca Santa María 2022', 9.1, 'Ribera del Duero (España)', 'Bodegas y Viñedos Valtravieso', 'Tempranillo / Cabernet sauvignon / Merlot'), ('Tarima Hill 2020', 12.5, 'Alicante (España)', 'Bodegas Volver', 'Monastrell'), ('Viña Ardanza Reserva 2017', 15.5, 'Rioja (España)', 'La Rioja Alta', 'Tempranillo / Garnacha'), ('La Montesa 2020', 30.75, 'Rioja (España)', 'Bodegas Palacios Remondo', 'Garnacha / Uvas tintas'), ('Pruno 2021', 29.95, 'Ribera del Duero (España)', 'Finca Villacreces', 'Tempranillo / Cabernet sauvignon'), ('Pétalos del Bierzo 2022', 17.5, 'Bierzo (España)', 'Descendientes de J. Palacios', 'Mencía / Uvas tintas / Uvas blancas'), ('Marqués de Murrieta 2019', 55.5, 'Rioja (España)', 'Marqués de Murrieta', 'Tempranillo / Mazuelo / Graciano / Garnacha'), ('Dido La Universal 2022', 16.9, 'Montsant (España)', 'Venus "La Universal"', 'Garnacha / Syrah / Cabernet sauvignon / Cariñena / Merlot'), ('Muga Selección Especial 2019', 70.6, 'Rioja (España)', 'Bodegas Muga', 'Tempranillo / Garnacha / Mazuelo / Graciano'), ('Contino Reserva 2020', 29.2, 'Rioja (España)', 'Viñedos del Contino', 'Tempranillo / Graciano / Mazuelo / Garnacha'), ('Carmelo Rodero 9 Meses 2022', 14.9, 'Ribera del Duero (España)', 'Bodegas Rodero', 'Tempranillo'), ('Pago de los Capellanes Crianza 2022', 27.9, 'Ribera del Duero (España)', 'Pago de los Capellanes', 'Tempranillo'), ("Les Cousins L'Inconscient 2023", 24.5, 'Priorat (España)', 'Les Cousins Marc & Adrià', 'Cariñena / Garnacha / Cabernet sauvignon / Merlot / Syrah'), ('El Enemigo Cabernet Franc 2021', 23.2, 'Mendoza (Argentina)', 'Bodega Aleanna', 'Cabernet franc / Malbec'), ('Azpilicueta Crianza 2020', 8.95, 'Rioja (España)', 'Bodegas Campo Viejo', 'Tempranillo / Graciano / Mazuelo'), ('Viña Cubillo 2016', 16.5, 'Rioja (España)', 'Bodegas R. López de Heredia ', 'Tempranillo / Garnacha / Mazuelo / Graciano'), ('Barón de Ley Reserva 2019', 10.5, 'Rioja (España)', 'Barón de Ley', 'Tempranillo'), ('GR-174 Priorat 2022', 13.95, 'Priorat (España)', 'GR - Vi de Gran Recorregut', 'Garnacha / Cariñena / Cabernet sauvignon / Merlot / Syrah'), ('Sericis Monastrell 2019', 10.5, 'Alicante (España)', 'Bodegas Murviedro', 'Monastrell'), ('Les Argelieres Pinot Noir 2023', 8.7, "Pays d'Oc IGP (Francia)", 'LGI Wines', 'Pinot noir'), ('El Linze 2022', 20.9, 'Castilla (España)', 'Bodegas El Linze', 'Tinto Velasco / Syrah'), ('Lalama 2021', 46.6, 'Ribeira Sacra (España)', 'Dominio do Bibei', 'Mencía / Garnacha tintorera / Mouratón / Sousón / Brancellao'), ('Emilio Moro Finca Resalso 2023', 20.5, 'Ribera del Duero (España)', 'Emilio Moro', 'Tempranillo'), ('Camins del Priorat 2022', 55.5, 'Priorat (España)', 'Álvaro Palacios', 'Garnacha / Cabernet sauvignon / Cariñena / Syrah / Merlot'), ('Els Pics 2021', 35.5, 'Priorat (España)', 'Bodegas Mas Alta', 'Garnacha / Cariñena / Syrah / Cabernet sauvignon'), ('Guímaro Camiño Real 2022', 16.0, 'Ribeira Sacra (España)', 'Guímaro', 'Garnacha tintorera / Caiño tinto / Mouratón / Mencía / Sousón'), ('Tinto Figuero 12 Meses 2020', 11.95, 'Ribera del Duero (España)', 'Bodegas y Viñedos García Figuero', 'Tempranillo'), ('Hacienda López de Haro Reserva 2018', 22.75, 'Rioja (España)', 'Hacienda López de Haro', 'Tempranillo / Graciano'), ('Juan Gil Etiqueta Plata 2021', 12.25, 'Jumilla (España)', 'Bodegas Juan Gil', 'Monastrell'), ('PradoRey Finca Valdelayegua 2020', 14.5, 'Ribera del Duero (España)', 'Bodegas Pradorey', 'Tempranillo / Cabernet sauvignon / Merlot'), ('Abadía Retuerta Selección Especial 2020', 145.5, 'Abadía Retuerta (España)', 'Abadía Retuerta', 'Tempranillo / Cabernet sauvignon / Syrah'), ('Aalto PS 2021', 199.5, 'Ribera del Duero (España)', 'Aalto', 'Tempranillo'), ('Trus Roble 2023', 18.9, 'Ribera del Duero (España)', 'Bodegas Trus', 'Tempranillo'), ('Fèlsina Chianti Classico 2021', 18.4, 'Chianti Classico DOCG (Italia)', 'Fèlsina', 'Sangiovese'), ('Sexto Elemento 2022', 21.15, 'Valencia (España)', 'Bodega Sexto Elemento', 'Bobal'), ('Larchago Reserva 2017', 16.5, 'Rioja (España)', 'Bodegas Familia Chávarri', 'Tempranillo'), ('Finca Valpiedra Reserva 2016', 19.6, 'Rioja (España)', 'Finca Valpiedra', 'Tempranillo / Graciano / Maturana tinta'), ('Azpilicueta Reserva 2018', 13.6, 'Rioja (España)', 'Bodegas Campo Viejo', 'Tempranillo / Graciano / Mazuelo'), ('Marqués de Vargas Reserva 2019', 23.72, 'Rioja (España)', 'Marqués de Vargas', 'Tempranillo / Mazuelo / Garnacha'), ('Muga Crianza  2020', 11.2, 'Rioja (España)', 'Bodegas Muga', 'Tempranillo / Garnacha / Mazuelo / Graciano'), ('Tomás Postigo 3er Año 2021', 35.9, 'Ribera del Duero (España)', 'Bodega Tomás Postigo', 'Tempranillo / Cabernet sauvignon / Merlot / Malbec'), ('Frontonio Microcósmico Garnacha 2022', 13.85, 'Valdejalón (España)', 'Bodegas Frontonio', 'Garnacha'), ('Cune Imperial Reserva 2019', 57.9, 'Rioja (España)', 'Compañía Vinícola del Norte de España - CVNE', 'Tempranillo / Graciano / Mazuelo'), ('Cims de Porrera Vi de Vila 2019', 17.9, 'Priorat (España)', 'Cims de Porrera', 'Cariñena / Garnacha'), ('Ceci Otello NerodiLambrusco', 12.45, 'Emilia IGT (Italia)', 'Cantine Ceci', 'Lambrusco Maestri'), ('Luna Beberide Mencía 2023', 6.95, 'Bierzo (España)', 'Bodegas y Viñedos Luna Beberide', 'Mencía'), ('Izadi Larrosa Negra 2021', 9.55, 'Rioja (España)', 'Bodegas Izadi', 'Garnacha'), ('Marqués de Cáceres Crianza 2020', 5.25, 'Rioja (España)', 'Marqués de Cáceres', 'Tempranillo / Garnacha / Graciano'), ('La Forcallà de Antonia 2022', 13.95, 'Valencia (España)', 'Bodega Rafael Cambra', 'Forcayat del arco'), ('Sió 2022', 27.5, 'Mallorca (España)', 'Bodega Ribas', 'Mantonegro / Syrah / Cabernet sauvignon / Merlot'), ('Corimbo 2019 (Magnum)', 22.95, 'Ribera del Duero (España)', 'Bodegas La Horra', 'Tempranillo'), ('Viña Salceda Crianza 2019', 8.95, 'Rioja (España)', 'Bodegas Viña Salceda', 'Tempranillo / Mazuelo / Graciano'), ('Torre Muga 2019', 76.5, 'Rioja (España)', 'Bodegas Muga', 'Tempranillo / Mazuelo / Graciano'), ('Viña Sastre Roble 2022', 11.6, 'Ribera del Duero (España)', 'Viña Sastre', 'Tempranillo'), ('Ramón Bilbao Reserva 2018', 30.25, 'Rioja (España)', 'Bodegas Ramón Bilbao', 'Tempranillo / Mazuelo / Graciano'), ('Familia Valdelana Crianza 2021', 8.95, 'Rioja (España)', 'Bodegas Valdelana', 'Tempranillo / Mazuelo'), ('Sindicat La Figuera 2022', 10.5, 'Montsant (España)', 'Agrícola Aubacs i Solans', 'Garnacha'), ('Viña Pomal Reserva 2017', 14.9, 'Rioja (España)', 'Bodegas Bilbaínas', 'Tempranillo'), ('Remelluri Reserva 2016', 57.5, 'Rioja (España)', 'Granja Ntra. Sra de Remelluri', 'Tempranillo / Garnacha / Graciano / Viura / Malvasía'), ('Regina Viarum Mencía 2022', 9.95, 'Ribeira Sacra (España)', 'Bodegas Regina Viarum', 'Mencía'), ('Pepe Yllera Roble 2019', 9.55, 'Ribera del Duero (España)', 'Yllera', 'Tempranillo / Cabernet sauvignon'), ('Fariña Lágrima 2022', 8.95, 'Toro (España)', 'Bodegas Fariña', 'Tinta de Toro')]
    setUvas={'Tempranillo', 'Cabernet franc', 'Mencía', 'Merlot', 'Tinta de Toro', 'Cariñena', 'Pinot noir', 'Mantonegro', 'Monastrell', 'Garnacha tintorera', 'Lambrusco Maestri', 'Malvasía', 'Petit verdot', 'Graciano', 'Uvas tintas', 'Viura', 'Maturana tinta', 'Malbec', 'Bobal', 'Brancellao', 'Caiño tinto', 'Forcayat del arco', 'Cabernet sauvignon', 'Syrah', 'Garnacha', 'Uvas blancas', 'Tinto Velasco', 'Sousón', 'Sangiovese', 'Mouratón', 'Mazuelo'}
    conn= sqlite3.connect("vinos.db")
    conn.text_factory=str
    conn.execute("DROP TABLE IF EXISTS VINOS")
    conn.execute("DROP TABLE IF EXISTS UVAS")
    conn.execute('''CREATE TABLE VINOS(
    VINO    TEXT NO NULL,
    PRECIO    REAL,
    DENOMINACION    TEXT,
    BODEGA    TEXT,
    UVA    TEXT);
    ''')
    conn.execute('''
    CREATE TABLE UVAS
    (NOMBRE TEXT NO NULL);
    ''')
    for vino in listaVinos:
        conn.execute('''INSERT INTO VINOS VALUES (?,?,?,?,?)''',vino)
    for uva in setUvas:
        conn.execute('''INSERT INTO UVAS (NOMBRE) VALUES (?)''',(uva,))
    conn.commit()   
    conn.close()
    print("Base de datos creada y poblada")
    
#----------------LISTAR TODOS

def listarComand():
    conn= sqlite3.connect("vinos.db")
    conn.text_factory=str
    cursor= conn.execute("SELECT * FROM VINOS")
    listarTodos(cursor)
    conn.close()
    
def listarTodos(cursor):
    v=Toplevel()
    v.title("LISTADO DE VINOS")
    sc=Scrollbar(v)
    sc.pack(side=LEFT,fill=Y)
    lb=Listbox(v,width=150,yscrollcommand=sc.set)
    for row in cursor:
        print(row)
        lb.insert(END,"VINO "+row[0].upper())
        lb.insert(END,"PRECIO: "+str(row[1])+" €")
        lb.insert(END,"BODEGA: "+row[3])
        lb.insert(END,"DENOMINACION: "+row[2])
        lb.insert(END,"\n")
    lb.pack(side=RIGHT,fill=BOTH)
    sc.config(command=lb.yview)

#----------------BUSCAR POR DENOMINACION

def buscarDenominacion():
    def listar(event=None):
        conn=sqlite3.connect("vinos.db")
        conn.text_factory=str
        cursor=conn.execute("SELECT * FROM VINOS WHERE DENOMINACION LIKE '%"+denominacion.get()+"%'")
        listarTodos(cursor)
        conn.close()
    conn=sqlite3.connect("vinos.db")
    conn.text_factory=str
    cursor=conn.execute("SELECT DISTINCT DENOMINACION FROM VINOS")
    opciones=set()
    for row in cursor:
        generos=row[0].split(",")
        for genero in generos:
            opciones.add(genero.strip())
    v=Toplevel()
    v.title("BUSCAR POR DENOINACION")
    label=Label(v, text="Seleccionar Denominacion: ")
    label.pack(side=LEFT)
    
    denominacion=Spinbox(v,text="Denominacion",values=list(opciones))
    denominacion.bind("<Return>",listar)
    b=Button(v,text="Buscar",command=listar)
    b.pack(side=RIGHT)
    denominacion.pack(side=RIGHT)
    conn.close()
    
#----------------BUSCAR POR PRECIO

def buscarPrecio():
    def listar(event=None):
        conn=sqlite3.connect("vinos.db")
        conn.text_factory=str
        cursor=conn.execute("SELECT * FROM VINOS WHERE PRECIO < '%"+str(precio.get())+"%' ORDER BY PRECIO ASC")
        listarTodos(cursor)
        conn.close()
    v=Toplevel()
    v.title("BUSCAR POR PRECIO")
    label=Label(v,text="Indique un precio maximo: ")
    label.pack(side=LEFT)
    precio=Entry(v,text="XX.XX")
    precio.pack(side=LEFT)
    precio.bind("<Return>",listar)
    b=Button(v,text="Buscar",command=listar)
    b.pack(side=LEFT)


#----------------BUSCAR POR PRECIO

def buscarUva():
    def listar(event=None):
        conn=sqlite3.connect("vinos.db")
        conn.text_factory=str
        cursor=conn.execute("SELECT * FROM VINOS WHERE UVA LIKE '%"+str(uva.get())+"%'")
        v=Toplevel()
        v.title("LISTADO DE VINOS")
        sc=Scrollbar(v)
        sc.pack(side=LEFT,fill=Y)
        lb=Listbox(v,width=150,yscrollcommand=sc.set)
        for row in cursor:
            print(row)
            lb.insert(END,"VINO "+row[0].upper())
            lb.insert(END,"TIPOS DE UVAS: "+str(row[4]))
            lb.insert(END,"\n")
        lb.pack(side=RIGHT,fill=BOTH)
        sc.config(command=lb.yview)
        conn.close()
    conn=sqlite3.connect("vinos.db")
    conn.text_factory=str
    cursor=conn.execute("SELECT DISTINCT NOMBRE FROM UVAS")
    opciones=set()
    for row in cursor:
        for r in row:
            opciones.add(r)
    print(opciones)
    v=Toplevel()
    v.title("BUSCAR POR UVA")
    label=Label(v,text="Indique un tipo de uva: ")
    label.pack(side=LEFT)
    uva=Spinbox(v,text="Tipo de Uva",values=list(opciones))
    uva.pack(side=LEFT)
    uva.bind("<Return>",listar)
    b=Button(v,text="Buscar",command=listar)
    b.pack(side=LEFT)
    
    



#----------------VENTANA PRINCIPAL

def ventana_principal():
    raiz = Tk()

    menu = Menu(raiz)

    #DATOS
    menudatos = Menu(menu, tearoff=0)
    menudatos.add_command(label="Cargar", command=almacenar_bd_Prueba)
    menudatos.add_command(label="Listar", command=listarComand)
    menudatos.add_command(label="Salir", command=raiz.quit)
    menu.add_cascade(label="Datos", menu=menudatos)

    #BUSCAR
    menubuscar = Menu(menu, tearoff=0)
    menubuscar.add_command(label="Denominacion", command=buscarDenominacion)
    menubuscar.add_command(label="Precio", command=buscarPrecio)
    menubuscar.add_command(label="Uvas", command=buscarUva)
    menu.add_cascade(label="Buscar", menu=menubuscar)

    raiz.config(menu=menu)

    raiz.mainloop()



if __name__ == "__main__":
    ventana_principal()