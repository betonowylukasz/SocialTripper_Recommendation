Większość plików jest powiązana z procesem oczyszczania oraz generowania kolejnych danych. 
Głównym plikiem jest predict.py w którym wczytywany jest nauczony model. W pliku tym można podać dane przykładowego użytkownika, dla którego model zwraca oceny rekomendacji w zestawieniu z pozostałymi użytkownikami (w tym wypadku dane użytkowników ze Stravy).
Można łatwo zmienić, żeby zamiast dodawać użytkowników w pętli, stworzyć własną parę użytkowników dla których model zwróci ocenę.
