# Projektrapport

## Introduktion
Detta projekt är till att utveckla en applikation som använder OpenAI API för att generera websidor
uppdatera websidor och analysera filer på egen dator. Projektet är delvis byggt med hjälp av ChatGPT, 
Vi har använt kod av redan skapade projekt och sedan gjort om till vår önskemål.

## Logg

- Implementering av grundläggande file query och webgenerator:
- Testning och felsökning: Att få den att förstå rätt uppdrag , att få den att lära sig visa uppdrag
- Granskning för inlämning: Efter att vi fått önskat funktion har vi beslutat att avsluta det.
- Detta projekt är av en typ som kräver otroligt mcyekt tid och inlärning för att utvkeckla och få den att bli perfekt.
- Att få den att läsa fil innehåll och följdfrågor.
- Sist har vi impelemnterat tidtagning.

## Benchmark
Vi har lagt in kod i utils för att spåra oliak funktioner och automatisk ta tidsmätning !
Tid för läsa fil namn OpenAI API response time: 1.7 ( hade vi inte använt indexerat databas som lagat info skulle det ta minst dubbla tiden.)
Skapa en sida tog ca 10 secunder
Spara versionen av den tog ca 0.009sekunder

## Observationer
- Implementeringen av filhantering var lite enklare men än mycket att lära sig, svårare var web generering 
var utmanande att göra rätt från början, alla detaljer måste var nogran planerade och man nbör kunna html 
eller nogrant inspektera genereade koden för att få rätt uppdatering. 

- Användningen av OpenAI API var effektiv men man måste veta syfte och veta hur man bygger upp koden för att 
inte slösa för många tokens. Man måste också vara väldigt tydlig i allt man gör och rätt från början. 

## Slutsats
Tanken var endast vi skulle bygga en web generator men när vi insåg att man även skulle ha fil funktion för att 
man ska kunna spara/uppdatera websidor tyckte vi det var intressant att ha en filassitant.
Efter att ha testat vår egna fil assitent och webgerator kan vi bara konstantera att AI API är något man verkligen
ska lära sig om man vill hänga med AI trenden, det går att göra otroligt intresanta projekt med det.
ChatGPT kan vra både till stor hjälp men även en stor vilseledare om man inte känner till lite grundprogrammering.
Vi är övertygade om att AI är nytidens Induastrilisering , vi vet ej hur bra den är för människan men för dem
som gillar teknik är detta en dröm som man än inte fattat har blivit verklighet!