***CZECH***

Aplikace QA týmu, kterou jsem pomáhal vylepšovat a implementovat nové funkce po čas mé praxe.

*static/css* - obsahuje CSS soubor. Upravení vzhledu webové stránky používající bootstrap.

*templates* - obsahuje base a rozšiřující index HTML stránky. Base soubor obsahuje hlavičku index souboru kde  se importuje bootstrap a jQuery.
Index soubor obsahuje rozložení webové stránky včetně skriptů JavaScript nebo Ajax. Funkce přepínání stylů vzhledu, funkce s výstupovým textem jako kopírování, uložení jako soubor, smazání obsahu.

*TestingUI.py* - obsahující testovací funkce, načtení serverů z YAML souboru a inicializace. Komunikace se souborem authorization, který z důvodu zranitelnosti není součástí repozitáře.

*UpdateBRE.py* - soubor pro aktualizaci a nahrání souborů vzdáleně na win serveru do BRE funkce.

*servers.yml* - YML soubor obsahující konfigurace jednotlivých serverů pro aplikaci.

***ENGLISH***

Application QA team that I helped improve and implement new features during my internship.

 *static/css* - contains a CSS file.  Customizing the appearance of a website using bootstrap.
 
 *templates* - contains the base and expanding index of the HTML page.  The base file contains the file index header where bootstrap and jQuery are imported.
 The index file contains the layout of the web page including JavaScript or Ajax scripts.  Features to switch appearance styles, features with output text such as copy, save as file, delete content.
 
 *TestingUI.py* - containing testing functions, loading servers from a YAML file and initialization.  Communication with the authorization file, which is not part of the repository due to a vulnerability.
 
 *UpdateBRE.py* - file for updating and uploading files remotely on a win server to the BRE function.
 
 *servers.yml* - YML file containing configurations of individual servers for the application.
