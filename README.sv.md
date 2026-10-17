# Kollektivtrafik Sverige för Tessera

Avgångar från Trafiklab Timetables på din ESP32-skärm. Installera pluginen en gång och lägg till flera rutor med egna hållplatser och filter.
Kräver plugin-API 0.10: Tessera 0.4.88 och skärmfirmware 0.56.0 eller senare kompatibel version.

## Installation

1. Skaffa en API-nyckel för **Trafiklab Realtime APIs** på https://developer.trafiklab.se/.
2. Öppna Plugins i Tessera och lägg till länken https://github.com/ExhaleSthlm/tessera-plugin-sweden-public-transport.
3. Lägg till pluginen på skärmen och bygg firmware.
4. Ange API-nyckeln i pluginens hemliga inställning. Den ska inte ligga i Git eller YAML.
5. Lägg till två **Avgångar**-rutor. Skriv hållplatsnamnet i **Sök hållplats**, lämna fältet och välj träffen i **Hållplats**. Välj trafikslag och linjer enligt tabellen nedan.
6. Spara och skicka layouten. Använd gärna två kolumners bredd per ruta för listvisning.

| Inställning | Blåsut tunnelbana | Dalens sjukhus buss |
| --- | --- | --- |
| Hållplats-ID | `740021703` | `740065542` |
| Trafikslag | Tunnelbana | Buss |
| Första linjen | Tomt | `163` |
| Andra linjen | Tomt | `816` |
| Destinationsfilter | Tomt | Tomt |

Tomt destinationsfilter visar båda riktningarna. Destinationen visas på varje rad.
Blåsuts hållplatsområde innehåller även bussar, så välj uttryckligen Tunnelbana där.

## På skärmen

- `+2` betyder två minuters försening.
- `TT` betyder tidtabellstid utan realtidsprognos.
- Gångtiden filtrerar bort avgångar du inte hinner till; nedräkningen visar tiden till avgång, inte tiden tills du behöver gå.
- Inställda avgångar visas inte. API:et visar kommande 60 minuter.
- Vid hämtningsfel visas tidigare data med varningen ”Gamla tider”, växelvis med källhänvisningen Trafiklab.se.

Varje hållplats hämtas var 60:e sekund och delar svar mellan rutorna. Två hållplatser dygnet runt motsvarar cirka 89 280 avgångsanrop på 31 dagar, plus sökningar, omstarter och eventuella återförsök. Namnsökningar cachas ett dygn per söktext. Realtime Brons har enligt Trafiklab 100 000 anrop/månad; standarden ryms inom den kvoten för två hållplatser. Fler hållplatser eller andra appar med samma nyckel behöver räknas med.

Intervallet är tills vidare fast i manifestet. Inställbart intervall, dygnsschema och beräknad förbrukning i editorn kräver stöd utanför pluginens nuvarande manifest. Se ROADMAP.md.

Första versionen är en beta. Se engelska README för tekniska begränsningar och VALIDATION.md för genomförda tester.
