# IP_solver_phyton

## Bevezetés:
Az operácókutatás a jelenlegi kedvenc területem a matematikában, mivel másodéves hallgató vagyok jelenleg csak az Operációkutás 1 tárgyat végeztem le a 2 még folyamatban van. Ez ezen projekt szempontjából azért lényeges mert az első tárgy végén vezetik be az IP feladatok hasznosságát, de konkrét megoldó heurisztikákat csak idén áprilisban keztünk el tanulni. Engem érdekelt, hogy lehet ilyen feladatokat megoldani ezért úgy döntöttem ezek megoldásával szeretnék foglalkozni ezen projektben, votl már eleve egy saját ötletem, és a cél nem a már létező algoritmusok implementálása hanem a saját ötletem kidolgozása volt. Az input.txt-be kell írni a megoldandó feladatot, a main.py futatása után az output.txt-ben jelenik meg a megoldás.

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

 ## Sample.py

 Automatikusan megfelelő formátumú inputokat generál adott feltételekkel:

    n: Number of columns in A
    m: Numbers of rows
    k: max value of x
    size: Number of IPs to be created
    Percentage_of_wrong: Percentage of IPs in the sample NOT GAURANTED to be solvable, that does not mean this is the percentage of non-solvable exercises (maybe inverted) 
    file: the given file
    start, end: the interval from which A and b can get their elements

A percentage_of_wrong változó igazából az volt hogy teljesn random inputok helyett, amik nagyon ritkán rendelkeznek kis k-ra megoldással, beszórjunk néhány megoldható mégis random példát. Mivel ere a célre lett kitalálva ha mondjuk 70%-ra állítjuk az nem azt jelenti közeltőlegesen 70% nem megoldható, hanem azt, hogy 70% olyan módon lett generálva, hogy viszonylag kicsi az esélye a megoldhatóságnak

###A legérdekesebb rész itt a példa elkészítése:

Vesz egy következő azonosítót a generátorától:

        idstore = idgiver()

Fog egy random A mátrixot és vesz egy x megoldóvektort:

        #The program generates IP-s by taking a random x vector and a random A, and then we set b to A,x, which means x is a solution. Then we take a sample from indicator(p) and if it returns True, we distort b with a random vector, making x no longer a solution.
        for j in range(size):
            A = np.random.randint(start, end, (m,n))
            x = np.random.randint(0, k, (n,1))

Ha a feladat megoldható kell legyen akkor b A és x szorzata lesz, ha nem akkor hozzáadunk a kapott szorzathoz egy random vektort, így nem biztos hogy nem megoldható feladatot kapunk.

            b = A @ x
            if Percentage_of_wrong != 0:
                b = A @ x - (np.random.randint(-k* 0.05-1, k*0.05 +2, (m,1)) *indicator(Percentage_of_wrong))
            id = next(idstore)
            write_record(A,b,k,id)

Kell egy indikátor változó ami garantálja a megoldható feladatot jó arányát:

    def indicator(p): #an indicator probability distribution
        if np.random.randint(0,100) < p:
            x = 1
        else:
            x = 0
        return x

Beírjuk a kapott példát a fájlba:

    def createrndsample(n = 5, m = 5, k = 10, size = 10, Percentage_of_wrong = 50, file = "input.txt", start = -100, end = 100):
    with open(file, "a", encoding="utf-8") as f:
        def write_to_file(text):

                f.write(str(text) + "\n")

        def idgiver(): #id generator
            i = 0
            while True:
                i +=1
                yield i
        
        def write_record(A,b,k,id):
            write_to_file("id:")
            write_to_file(id)
            write_to_file("A:")
            for j in A:
                f.write(", ".join(map(str, j)) + "\n")
            write_to_file("b:")
            for i in b:
                for j in i:
                    write_to_file(j)
            write_to_file("k:")
            write_to_file(str(k))
            write_to_file("---------")

 ### Lehetséges Javítások, fejlesztések
 - Percentage_of_wrong javítássa, hogy tényleg a nem megoldható feladotok arányát adja
     - Ez könnyen megvalósítható beteszünk egy ifet ami meghívja az IP_solvert és addig generálja újra amíg ne mmegoldható lesz. Ez tapasztalataim szerint viszonlyag kevés ujrapróbálással meg tud lenni, de elképzelhető, hogy valamilyen nagyon inputok esetén kihívássá válik nemmegoldható feladatot kitalálni.
## output.py

Itt találhatók a végéeredmény kiírásával foglalkozó függvények a writeshort egyszerűen beírja a fájlba amit kap. A Write megkapja a feladat összes atributumát az alapján tagoltan kír egy részletes leírást

### Lehetséges Javítások, fejlesztések
- SmartWriter osztály: 
    A feladatok elvégzése közben az okos modul jegyzi a lépéseit a log.txt fájlba. Ennek az osztálynak az lett volna a célja, hogy e mellé jegyezze az eredeti script lépéseit egy második hasábba, de ennek a megalkotása nehezebb volt mint hasznos így felhagytam vele. Ennek befejezése lehet megérné a fáradságot.


## Branch_andbound.py
Ez az eredeti első Solver aminek a működése a téma leadásakor a fejemben volt. Az ötlet arra alapul, hogy nézzük az LP relaxaációkat úgy, hogy sorra egyre több változó értékét egy adott egészre rögzítjük.
A program a Branch and Bound gondolatmenetet követi. Az alapfeladatot úgy osztjuk részfeladotkra, hogy mindig megkeressük az első változót amit nem rögzítettünk, annak rögzitünk egy még ki nem próbált értéket. ezt folytatjuk amíg minden változót valami értékre rögzítettünk, és megoldást kapunk, vagy mindent kipróbáltunk vagy levágtunk, azaz nem tudjuk tovább csinálni. A megoldás logikáját a köveetkező fával lehet szépen ábrázolni:

```
Start
├── x₁ = 0
│ ├── x₂ = 0
│ │ ├── x₃ = 0
│ │ └── x₃ = 1
│ └── x₂ = 1
│ ├── x₃ = 0 
│ └── x₃ = 1 
└── x₁ = 1
├── x₂ = 0
│ ├── x₃ = 0 
│ └── x₃ = 1 
└── x₂ = 1
├── x₃ = 0 
└── x₃ = 1 
```

### Ágak levágása
Ha az első néhány változót valamilyen értékre rögzítettük, és így már egy olyan részfeladatot kapunk, ami nem megoldható, akkor biztosak lehetünk benne, hogy így nem kezdőthet megoldás, a többi ezt folytató feladatot eldobhatjuk

            if solveable(CurrentA,b,NoSolution, checkeq= checkeq, checkLP= checkLP):
            ...
            
A levágást úgy oldjuk meg hogy csak akkor adjuk hozzá az új feladatot, ha az őse megoldható

###Részfeladatot ellenőrzése
Nézzük meg egy adott feladatról hogy az LP relaxáltja megoldható-e. Ha nem akkor nyílván egyész megoldás se létezhet. Hasonlóan meg lehet nézni hogy az Ax = b lináris egyenletrendszer megoltható-e

    def solveable(A,b, NoSolution:list,checkeq = True, checkLP = True):
    NoSolution[2] +=1
    if checkeq:
        x, s, q, d = np.linalg.lstsq(A,b)
        is_exact = np.allclose(A @ x, b)
        if not is_exact:
            NoSolution[1] += "\n Ax = b egyenlőség rendszer nemmegoldható"
            return False
    
    if checkLP:
        bounds = [(0, None)] * len(A[0])  # x >= 0 constraints
        result = linprog(c=[0] * len(A[0]), A_eq=A, b_eq=b, bounds=bounds, method='highs')
        if not result.success:
            NoSolution[1] += "\n LP relaxáció hiba \n"
            return False

    return True

### Új feladat létrehozása
Könnyen csinálhatunk új részfeladatokat egy változó rögzitése után. Ha mondjuk x i-edik komponensét c-re rögzítjük, nem kell mást tennünk mint levonni a c i-edik oszloppal vet szorzatát b-ből és utána kitörlni az oszlopot A-ból. Ha az így kapott A'x'=b' feladatot megoldja egy x' akkor az i-edik komponens beszúrásával kapott x megoldja az eredti Ax=b feladatot

                    ...
                    newA = np.delete(CurrentA,0,axis= 1)
                    newb = b.copy() - (A[:,i] * z)
                    newx = x.copy()
                    newx[i] = z
                    stuff_to_do.append([newA, newb, newx.copy()])

### Bejárás
Minden levélben van egy potenciális megoldás, és mivel a célunk egyetlen megengedett megoldás megtalálása a leghatékonyabb bejárás egy mélységi bejárás ami addig futt amíg egy megengedett levélbe nem érünk. Ezt legkönnyebb úgy implementálni, hogy a részfeladatokat egy stackben tároljuk.

                while stuff_to_do and NoSolution[0]:
                    nextone = stuff_to_do.pop()
                    __IP_solver__(A,nextone[0],nextone[1],k,nextone[2], b_original, NoSolution, checkeq= checkeq, checkLP= checkLP)
Amíg nincs minden komponens rögzítve és a részfeladat megoldható mindig rögzítsünk újat, ha már minden komponens adott nézzük meg, hogy megengedett megoldást kaptunk-e:

Nézzük meg minden komponensnek rögizettünk e értéket:

        if -1 in x:

Ha nem nézzük meg, hogy eddig megoldható-e a feladat:


            if solveable(CurrentA,b,NoSolution, checkeq= checkeq, checkLP= checkLP):
            
Ha igen rögzítsünk egy újat:

            i = 0
                while x[i] != -1:
                    i += 1

                for z in range(0,k):
                    newA = np.delete(CurrentA,0,axis= 1)
                    newb = b.copy() - (A[:,i] * z)
                    newx = x.copy()
                    newx[i] = z
                    stuff_to_do.append([newA, newb, newx.copy()])
                ...

Ha már mindent rögzítettünk: Nézzük meg hogy megoldás-e?

        else:
            NoSolution[3] +=1
            if np.allclose(A @ x, b_original):
                NoSolution[0] = False
                NoSolution[1] = str(x) + "\n Megoldja a rendszert \n"
            else:
                NoSolution[1] += " " + str(x) + "\n nem megoldás \n"


## Smartbranches





