# Manuell & Automatisk installation med skript för powershell

**** Manuell installation ***

Innan du börjar, se till att du har följande programvara installerad:

-  Python3 

1. Extrahera projektet till den plats där du vill ha det.

2. Ställ in en virtuell miljö

Att ställa in en virtuell miljö är frillivilligt man kan hoppa över detta om man vill men är rekommenderat
för att inte påverka andra program eller paket och för statbilitet, läs mera om "virtual environment in python").

Öppna kommandotolken (cmd) och gå till projektets mapp .


Skriv följande kommandon:
    
    # python -m venv venv

   ##### .\venv\Scripts\Activate
	
	När du är i (venv) miljö anger du kommandot: 
	
   #### pip install -r requirements.txt

3. Du måste se till att API nyklen finns tillgänglig  i .env filen 

  1. Du behöver skapa en fil som heter .env i projektmappen :
  
  OPENAI_API_KEY= din_openai_api_nyckel

Spara filen som .env i root av din projekt detta krävs för att köra vrituell miljö.

När du är klar kör programmet i cmd!

 ####  python app.py

---------------------- UTAN VENV ---------------------------------------------------
Altenativ 2 utan vitruell envoriemnt. 
 
Öppna cmd och kör kommandot nedan:

#### pip install -r requirements.txt
 
setx OPENAI_API_KEY "DIN_API_NYCKEL_HÄR"

Starta om cmd och gå in till din projet så är du klar att köra.

För att starta Flask-servern, skriv:

#### python app.py

Öppna en webbläsare och gå till: http://127.0.0.1:5000

------------------------------------------------------------------------------------------

## Automatisk installation med skript i powershell

( Av säkerhets skäl har vi valt att endast köra installationen i virtuell miljö med skript. 
vill ni köra utanför i vanligt miljö får ni köra manuell installation eller ändra i skriptfilen)

Tryck på Win+x och välj att öppna PowerShell som administratör.

Gå till projektets mapp.
Kör skriptet:
   # .\setup.ps1

Skriptet kommer nu att göra allt jobb åt dig och köra programmet i slutet om allt gick bra!
(OBS . API delen är inte inlagt i skriptet , men det kan du själv lägga in när du har en nyckel)

Om du får ett fel om exekveringspolicyer, kan du behöva ändra körpolicyerna.
Skriv följande kommando och välj YES (Y) och försök sedan att köra skriptet igen:

    # Set-ExecutionPolicy RemoteSigned

Efter att du har kört skriptet kan du återställa körpolicyn genom ange:

    # Set-ExecutionPolicy Restricted
