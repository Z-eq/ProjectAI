# Manuell & Automatisk installation med skript

**** Manuell installation ***

Innan du börjar, se till att du har följande programvara installerad:

1. Extrahera projektet till den plats där du vill ha det.

2. Ställ in en virtuell miljö

Att ställa in en virtuell miljö är frillivilligt man kan hoppa över detta om mn vill).

Öppna kommandotolken (cmd) och gå till projektets mapp.

Skriv följande kommandon:

    # python -m venv venv

    # .\venv\Scripts\Activate

3. Installera alla nödvändiga dependecies

Körkommando i cmd:

    # pip install -r requirements.txt

4.Du måste se till att API nyklen finns tillgänglig , det finns 2 sätt. 

  1. Du behöver skapa en .env-fil i projektmappen OPENAI_API_KEY="din_openai_api_nyckel"

Spara filen som .env i root av din projekt.

ALternativ 2 är vilken är att föredra om vill hålla på dela projektet med andra är att lägga nyckeln i sitt 
egna miljövariable.. genom att ange kommandot :
 
setx OPENAI_API_KEY="DIN_API_NYCKEL"

Starta om cmd och gå in till din projet så är du klar att köra.

För att starta Flask-servern, skriv:

   # python app.py

Öppna en webbläsare och gå till: http://127.0.0.1:5000.

------------------------------------------------------------------------------------------

## Automatisk installation med skript

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
