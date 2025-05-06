# IP_solver_phyton

## Összegzés:

## Működés:
A könyvtárban a következő fájlok megtalálhatóak:
- main.py
- input.py
- output.py
- Sample.py
- Branch_andbound.py
- Smartbranches.py
- input.txt
Ezen kívül vannak egyéb fájlok és mappák is, ezek közül néhányra itt majd kitérek ha említésre méltók, de a a program működésében semmilyen szerepet nem játszanak.

## Main.py

Itt csak meghívjuk a kész függvényeket a megfelelő paramétereinkkel, a fájl elején szerepel a következő leírás (amit angol nyelven írtam, főleg megszokásból) ami ezek működését leírja. Mivel meglevő modulokat hívunk meg itt semmi különleges nem történik. Az állítható paraméterek:

    model:string                            #Which solver should run, can be "legacy", "both" (runs one the other on teh same task), or "smart" by deafult
    long:bool                               #The style of description in the output.txt file
    Samplecreation:bool                     #If set True the program wipes the input.txt and fills it with a randomly generated sample of exercies according to the Sample
    Sample:iterable                         #n, m, k, size = 10, Percentage_of_wrong = 50. Extra parameters can be set with rewriting the function call in row 44
    checkeq:bool                            #Applies to legacy only. Determines if it should check The Linear equation: {x:Ax=b} != <Emptyset> at subtasks
    checkLP:bool                            #Determines if it should check the LP: {x:Ax=b, x >= 0} != <Emptyset> at subtasks
## input.py
Itt találhatók a beolvasással kapcsolatos függvények. Az elvárt alak:

    id:
    id
    A:
    A_1 #Each row of a
    A_2
    ...
    b:
    b_1
    b_2
    ...
    k:
    k
    ---------
    ...
    ---------
    ...
    ---------
Itt minden blokk két ------- között egy külön feladat. ahol az A: utáni szegmens az a mátrix soronként leírva b: b komponensei k: a felső korlát x-re id: hogy több feladat esetén könnyebb legyen beazonosítani melyikről van szó

A kód müködése:

Mivel sok feladat lehet az inputban és nem szükséges őket mind előre beolvasni, és lehet hogy nem is akarjuk, készítsünk inkább generátort ami mindig egy következő feladatot ad majd vissza:

    ...
    yield id_value, A, b, k_value****

Vissza kell majd adnunk ezeket az adotokat egy megfelelő formátumban ehez inicializáljunk megfelelő változókat a fv-be amiket majd visszadhatunk

    A_lines = []
    b_lines = []
    k_value = None
    id_value = None
    section = None

Elkezdjük az eléjétől olvasni a az adott szövegfájlt:

    ...
    for line in lines:

Bontsuk szekciókra attól függően, hogy éppen milyen adatot olvasunk be:

        ...
        elif line.startswith("id:"):
            section = "id"
            continue
        elif line.startswith("A:"):
            section = "A"
            continue
        elif line.startswith("b:"):
            section = "b"
            continue
        elif line.startswith("k:"):
            section = "k"
            continue

Mindig miután egy adatról tudjuk hova tartazik írjuk be a megfelelő sor adatait tartalmazó listába:

        ...
        if section == "A":
            A_lines.append(list(map(int, line.split(","))))
        elif section == "b":
            b_lines.append(int(line.split(",")[0]))  # Egy szám minden sorban
        elif section == "k":
            k_value = int(line)
        elif section == "id":
            id_value = int(line)
            
Amikor "--------" sort találunk akkor adjuk vissza az eddig beírt adatokat mint következő feladat:

        if line == "---------":
            # Átalakítás NumPy tömbökké
            A = np.array(A_lines)
            b = np.array(b_lines)

            # Validáció: b hossza = A sorainak száma
            if A.shape[0] != b.shape[0]:
                raise ValueError(f"Hibás méretek! A mátrix {A.shape[0]} sorból áll, de b {b.shape[0]} elemet tartalmaz.")
            
            yield id_value, A, b, k_value
            A_lines = []
            b_lines = []
            k_value = None
            id_value = None
            section = None


 ### Lehetséges Javítások, fejlesztések
   - Egy lehetséges függvény ami megkeres egy adott id-vel rendelkező feladatot és csak azt tölti be
     -  Ez viszonyylag kevés változtatással megkapható egyszerűen csak akkor adjuk vissza a feladatot ha id_value = keresett érték  
   - függvény ami bizonyos tulajdonságú feladatokat ad vissza
     -  id-hez hasonló módon megoldható 

