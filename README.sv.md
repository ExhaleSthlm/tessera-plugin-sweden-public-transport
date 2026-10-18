# Public transport (SE) för Tessera

Avgångar från Trafiklab Timetables på din ESP32-skärm. Installera pluginen en gång och lägg till flera rutor med egna hållplatser och filter.
Kräver plugin-API 0.12: Tessera 0.4.89 och skärmfirmware 0.57.0 eller senare kompatibel version.

## Installation

1. Skaffa en API-nyckel för **Trafiklab Realtime APIs** på https://developer.trafiklab.se/.
2. Öppna Plugins i Tessera och lägg till länken https://github.com/ExhaleSthlm/tessera-plugin-sweden-public-transport.
3. Lägg till pluginen på skärmen och bygg firmware.
4. Ange API-nyckeln i pluginens hemliga inställning. Den ska inte ligga i Git eller YAML.
5. Lägg till två **Avgångar**-rutor. Öppna **Hållplats**, skriv minst två tecken och välj en träff direkt i sökningen. Namnet sparas med valet.
6. Under **Linjer**, lägg till 1–8 linjer från hållplatsen. Ta bort en vald linje med ×. Välj trafikslag enligt tabellen.
7. Spara och skicka layouten. Bredare rutor visar en lista, även Guition med 1×3-raster.

| Inställning | Blåsut tunnelbana | Dalens sjukhus buss |
| --- | --- | --- |
| Hållplats-ID | `740021703` | `740065542` |
| Trafikslag | Tunnelbana | Buss |
| Linjer | `18` | `163`, `816` |
| Destinationsfilter | Tomt | Tomt |

Minst en linje måste väljas. Tar du bort alla visas **Välj linjer**, och rutans schemalagda avgångshämtningar upphör. En öppen editor kan fortfarande hämta linjealternativ. Linjerna delar samma avgångs-URL och 60-sekunderscache som hållplatsens övriga rutor.

Varje linje visas en gång i väljaren, oavsett riktning. Alternativen bygger på kommande 60 minuters avgångar och kan därför sakna linjer som inte går då. Alla trafikslag på hållplatsen ingår i linjevalen; trafikslagsfiltret styr avgångarna på skärmen. Vid byte av hållplats behöver du ta bort gamla linjeval och välja nya själv.

Tomt destinationsfilter visar båda riktningarna. Destinationen visas på varje rad. Blåsuts hållplatsområde innehåller även bussar, så välj Tunnelbana där.

## Uppgradering från 0.1.x eller 0.2.0

Uppdatera först Tessera till minst 0.4.89. Från 0.1.x behöver du välja hållplats igen i den nya sökväljaren. Från både 0.1.x och 0.2.0 behöver du välja linjer igen under **Linjer**; pluginen kan inte automatiskt konvertera de gamla två linjefälten. Spara/skicka layouten och bygg om/installera skärmens firmware. Gångtid, trafikslag, destinationsfilter och förseningsinställning behåller sina fält-ID:n.

## På skärmen

- `+2` betyder två minuters försening.
- `TT` betyder tidtabellstid utan realtidsprognos.
- Gångtiden filtrerar bort avgångar du inte hinner till; nedräkningen visar tiden till avgång, inte tiden tills du behöver gå.
- Inställda avgångar visas inte. API:et visar kommande 60 minuter.
- Källhänvisningen Trafiklab.se använder temats minsta textstorlek och ligger separat under avgångarna, så att alla tider ligger på samma lodräta linje.
- Vid hämtningsfel visas tidigare data med varningen ”Gamla tider”, växelvis med källhänvisningen Trafiklab.se.

Varje hållplats hämtas var 60:e sekund och delar svar mellan rutorna. Två hållplatser dygnet runt motsvarar cirka 89 280 avgångsanrop på 31 dagar, plus sökningar, omstarter och eventuella återförsök. Sökningen startar efter en kort skrivpaus och Tessera cachar sökträffar i tio minuter. Realtime Brons har enligt Trafiklab 100 000 anrop/månad; standarden ryms inom den kvoten för två hållplatser. Fler hållplatser eller andra appar med samma nyckel behöver räknas med.

Intervallet är tills vidare fast i manifestet. Inställbart intervall, dygnsschema och beräknad förbrukning i editorn kräver stöd utanför pluginens nuvarande manifest. Se ROADMAP.md.

Första versionen är en beta. Se engelska README för tekniska begränsningar och VALIDATION.md för genomförda tester.

## Varför visas Trafiklab.se?

Trafiklab kräver källhänvisning på skärmar och webbwidgets som visar deras data. Därför behåller pluginen texten **Trafiklab.se** på skärmen. Se [Trafiklabs villkor för Timetables](https://www.trafiklab.se/api/our-apis/trafiklab-realtime-apis/timetables/#license). Data omfattas av [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); pluginen filtrerar och omformaterar uppgifterna till avgångar med nedräkning.

Kravet innebär inte att en hel rad måste reserveras för texten. Vi använder temats minsta textstorlek och ligger separat under avgångarna, så att alla tider ligger på samma lodräta linje. Behåll källhänvisningen om du anpassar layouten. Pluginens egen kod har MIT-licens; datans licens är separat.

## Automatiska kontroller med GitHub Actions

Arbetsflödet **Plugin CI** körs vid push och pull request och kan startas manuellt under **Actions**:

- Validerar manifestet mot Tessera API 0.12 i Tessera 0.4.89 och kör testerna med exempeldata.
- Kompilerar C++-koden för Guition-simulatorn och kontrollerar layouten, inklusive rastret 1×3.
- Sparar bilder, loggar och rapport i **guition-preview**, som kan laddas ned från körningen i sju dagar.

Ingen API-nyckel behövs och inga Trafiklab-anrop görs. Arbetsflödet publicerar eller installerar ingenting. Simulatorbygget ersätter inte ett riktigt ESP32-bygge i Tessera eller test på din skärm. Den första körningen på GitHub behöver kontrolleras efter att filerna pushats.
