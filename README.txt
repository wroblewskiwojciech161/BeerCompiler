PROJEKT KOMPILATORA
kurs : Języki Formalne i Techniki Translacji
autor : Wojciech Wróblewski


Projekt kompilatora prostego języka imperatywnego.


#################################
Wymagania 
#################################


- python 3 ( testowany na wersji python 3.8.5 )
- biblioteka sly

Dodatkowo testy przeprowadzane były z wykorzystaniem
maszyny wirtualnej wykorzystującej bibliotekę
dużych liczb :

-cln


#################################
instalacja wymaganych pakietów
#################################



sudo apt-get update
sudo apt install python3.8
sudo apt install python3-pip
pip3 install sly
sudo apt-get install libcln-dev



################################
# korzystanie z kompilatora 
################################




> python3 compiler.py  <in> <out>

gdzie:

 <in> - nazwa pliku  zawierającego kod języka imperatywnego


 <out> - nazwa pliku wyjściowego,który docelowo zawierał
 będzie wygenerowany kod maszyny wirtualnej




 ###############################
 Przykład uruchomienia
 ###############################
 
 
 

 dodajemy do pliku input.txt kod w języku imperatywnym
 poniższą komendą generujemy kod maszyny wirtualnej w pliku output.txt

 > python3 compiler.py input.txt output.txt




 ###############################
  Opis plików
 ###############################
 
 
 
 methods.py - zawiera główną klasę odpowiedzialną,
 za generowanie kodu wynikowego na podstawie 
 danych otrzymanych z parser.py

 instructions.py - zawiera możliwe w 
 specyfikacji instrukcje na rejestrach 

 register.py,objects.py - pliki w których
 przestawiona jest struktura obiektów 
 wykorzystywanych podczas kompilacji

 lexer.py - kod leksera

 parser.py -kod parsera

 errors.py - klasa zawierająca główne 
 błędy przechwytywane przez kompilator
 
 compiler.py - program odpowiedzialny za
 uruchomienie kompilacji na danych
 wejściowych.

 key_words.py - plik zawierający kluczowe
 nazewnictwo, występujące  w danych
 wygenerowanych przez parser.
