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

Vi gjorde en skript som mäter tiden för dem olika funktioner vi har . och får lite olika tider 
beroende på vad man gör, förfrågninar tar längre tid då det är nätverksbaserat.

INFO:root:Running benchmark for: Generate a new web page
INFO:root:Generate a new web page took 16.6012 seconds with status code 200
INFO:root:Running benchmark for: Query list my files
INFO:root:Query list my files took 0.6518 seconds with status code 200
INFO:root:Running benchmark for: Query summarize my files
INFO:root:Query summarize my files took 5.0333 seconds with status code 200



## Observationer
- Implementeringen av filhantering var lite enklare men än mycket att lära sig, svårare var web generering 
var utmanande att göra rätt från början, alla detaljer måste var nogran planerade och man bör kunna html 
eller nogrant inspektera genereade koden för att få rätt uppdatering. 
- Filförfrågning kan bli fel ibland bereoende på vad man frågar i början. Finns mcyekt att lära och förfina.

- Att även använda sklearn modulen hade varit ett bra sätt att göra skriptet självlärande

- Använda GPT-4-Turbo kan bidra till mer avancerad och nograre apimen dyrare!

- Måste vara välduigt noga med koden så att man inte slösar toeksn o man råkar ha en loop där stora filer finns.



## Slutsats

Tanken var endast vi skulle bygga en web generator men när vi insåg att man även skulle ha fil funktion för att man ska kunna spara/uppdatera websidor tyckte vi det var intressant att ha en fil assistent. Efter att ha testat vår egna fil assistent och webgenerator kan vi bara konstantera att OpenAI API är något man verkligen ska lära sig om man vill hänga med AI trenden och spara tid. Det går att göra mycket mer med API än med det vanliga chattbaserade boten.

ChatGPT kan även vara en stor vilseledare om man inte känner till lite grund programmering. Vi är övertygade om att AI är ny tidens Industrialisering och för dem som gillar teknik är detta en dröm som man än inte fattat har blivit verklighet och för dem som är oroliga att AI ska ta deras jobb vill vi avsluta med en citat som ej vem 

> "AI May Not Take Your Job, But Someone Using AI Likely Will"  
> — Richard Baldwin, an economist and professor
