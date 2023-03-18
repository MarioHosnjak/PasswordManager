# SKRIPTA ZA TESTIRANJE NA LINUXU

echo '-> Stvaranje baze i postavljanje master passworda'
python3 -c 'import pwManager; pwManager.init()' "masterPassword"

echo '-> Dodavanje adrese="address" i pripadne lozinke="password"'
python3 -c 'import pwManager; pwManager.put()' "masterPassword" "address" "password"

echo '-> Dohvacanje lozinke sa adresom "address"'
python3 -c 'import pwManager; pwManager.get()' "masterPassword" "address"

echo '-> Dodavanje nove adrese="www.fer.hr" i pripadne lozinke="ferPassword"'
python3 -c 'import pwManager; pwManager.put()' "masterPassword" "www.fer.hr" "ferPassword"

echo '-> Dodavanje nove adrese="www.gmail.com" i pripadne lozinke="gmailPassword"'
python3 -c 'import pwManager; pwManager.put()' "masterPassword" "www.gmail.com" "gmailPassword"

echo '-> Promjena lozinke s adresom="www.fer.hr" na lozinku="novaFerLozinka"'
python3 -c 'import pwManager; pwManager.put()' "masterPassword" "www.fer.hr" "novaFerLozinka"

echo '-> Provjera je li lozinka promijenjena'
python3 -c 'import pwManager; pwManager.get()' "masterPassword" "www.fer.hr"

echo '-> Pokušaj dohvaćanje lozinke s krivim masterPassword-om'
python3 -c 'import pwManager; pwManager.get()' "kriviMasterPassword" "www.fer.hr"

echo '-> Pokušaj dohvaćanja lozinke s krivom adresom'
python3 -c 'import pwManager; pwManager.get()' "masterPassword" "www.krivaAdresa.com"

