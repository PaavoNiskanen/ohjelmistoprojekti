# Vaatimusmäärittely — RocketGame

Päiväys: 2026-01-14

**Yleiskuvaus:**
Kevyt 2D-avaruuspeliprojekti (Python + Pygame) jossa pelaaja ohjastaa alusta, taistelee vihollisia vastaan ja kerää pisteitä/voittoehdot. Tämä vaatimusmäärittely määrittelee projektin toiminnalliset ja ei-toiminnalliset vaatimukset.

**Sidosryhmät:**
- Pelaajat
- Kehittäjät
- Opettaja / arvioija

**Laajuus:**
Sisältää yksinpelin tilan (yksi taso tai rajoitettu pelikierros), pelaajan ohjauksen, viholliset, törmäykset, pisteytyksen, äänen perustoiminnot ja tallennuksen (pisteet). Ei sisällä moninpelitoimintoja tai verkkoyhteyksiä tässä versiossa.

## Toiminnalliset vaatimukset (Functional Requirements)

F1 — Pelin käynnistys ja valikko
- Kuvaus: Sovellus käynnistyy päävalikkoon, josta voi aloittaa pelin, katsoa ohjeet, tai lopettaa pelin.
- Prioriteetti: Korkea
- Hyväksymiskriteeri: Päävalikko näkyy ja valikot toimivat näppäin-/hiiriohjaimella.

F2 — Pelaajan ohjaus
- Kuvaus: Pelaaja voi liikkua (vasen/oikea/ylös/alas tai vaihtoehtoiset näppäimet), ampua ja käyttää mahdollisia erikoistoimintoja (boost).
- Prioriteetti: Korkea
- Hyväksymiskriteeri: Ohjaukset reagoivat viiveettä ja animoinnit päivittyvät.

F3 — Viholliset ja tekoäly
- Kuvaus: Pelissä esiintyy erilaisia vihollisia, joilla on yksinkertainen käyttäytyminen (suora lento, kiertoliike, hyökkäys pelaajaa kohti).
- Prioriteetti: Keskitaso
- Hyväksymiskriteeri: Vähintään kaksi vihollistyyppiä näkyvissä ja toimivina.

F4 — Törmäykset ja vahingot
- Kuvaus: Osumat ammuista tai vihollisista aiheuttavat vahinkoa; pelaajalla on elämät/energia.
- Prioriteetti: Korkea
- Hyväksymiskriteeri: Vahinko ja elämien vähentyminen tapahtuvat oikein, kuolema johtaa peli- tai uudelleenaloitusnäkymään.

F5 — Pisteytys ja tulosnäyttö
- Kuvaus: Pelaaja saa pisteitä vihollisen tuhoamisesta ja kerättävistä esineistä; pelin lopussa näytetään tulos.
- Prioriteetti: Korkea
- Hyväksymiskriteeri: Pisteet kasvavat oikeista toiminnoista ja tallennetaan väliaikaisesti pelisession ajaksi.

F6 — Äänet ja musiikki
- Kuvaus: Taustamusiikki ja ääniefektit (ammus, räjähdys, valikoissa navigointi).
- Prioriteetti: Matala–keskitaso
- Hyväksymiskriteeri: Äänet toistuvat ja voivat olla pois päältä asetuksista.

F7 — Tallennus ja asetukset
- Kuvaus: Pelin perusasetukset (äänenvoimakkuus, avaimet) tallentuvat paikalliseen asetustiedostoon; korkein piste saavutetaan näkyviin.
- Prioriteetti: Keskitaso
- Hyväksymiskriteeri: Asetusten muutos pysyy sovelluksen uudelleenkäynnistyksen yli.

F8 — Ohjeet ja käyttötapa
- Kuvaus: Pelin sisäiset ohjeet, jotka selittävät ohjauksen ja pelitavoitteen.
- Prioriteetti: Matala
- Hyväksymiskriteeri: Ohjeet saavutettavissa päävalikosta.

## Ei-toiminnalliset vaatimukset (Non-Functional Requirements)

NFR1 — Suorituskyky
- Kuvaus: Peli tavoittaa vakaan ruudunpäivitysnopeuden (target 60 FPS) tyypillisellä kehityskoneella.
- Mittari: FPS ei putoa alle 30 normaalissa pelitilanteessa.

NFR2 — Yhteensopivuus
- Kuvaus: Peli toimii Windows 10/11 -ympäristössä Python 3.10+ ja Pygame-kirjaston avulla.
- Mittari: Asennusohjeilla pelin voi käynnistää vakiokokoonpanolla.

NFR3 — Luotettavuus ja vakaus
- Kuvaus: Peli ei kaadu tavallisten pelitapahtumien seurauksena; kriittiset virheet käsitellään siististi.
- Mittari: Ei kriittisiä poikkeuksia normaaleilla pelin sisäisillä toiminnoilla.

NFR4 — Käytettävyys
- Kuvaus: Peli tarjoaa selkeän käyttöliittymän ja käyttöohjeet; ohjaukset ovat intuitiiviset.
- Mittari: Ensimmäisen pelikerran jälkeen pelaaja ymmärtää pelin perusmekaniikan ilman ohjausta.

NFR5 — Huollettavuus
- Kuvaus: Lähdekoodi on kommentoitu ja modulaarinen; jokainen pääkomponentti (pelaaja, vihollinen, peli-logiikka, UI) on omassa moduulissaan.
- Mittari: Uuden vihollistyypin lisääminen vaatii enintään yhden uuden moduulin ja muutoksia alle kahteen olemassa olevaan tiedostoon.

NFR6 — Lokalisaatio
- Kuvaus: Pääasiallinen kieli on suomi, mutta tekstit tullaan pitämään erillisessä resurssitiedostossa, mikä mahdollistaa laajennuksen muihin kieliin.

NFR7 — Turvallisuus
- Kuvaus: Sovellus ei kerää henkilökohtaisia tietoja eikä lähetä dataa verkkoon.

NFR8 — Resurssien käyttö
- Kuvaus: Peli ei ylitä kohtuullista muistinkulutusta (esim. < 500 MB) normaaleissa tilanteissa ja vapauttaa resurssit suljettaessa.

## Hyväksymiskriteerit ja testaus
- Yksikkötestit tärkeimmälle pelilogiikalle (pisteytys, törmäystarkistus) missä mahdollista.
- Manuaaliset testit: käynnistys, valikkonavigointi, pelaajan liike, ampuminen, törmäykset, vihollisten ilmestyminen, äänen päälle/pois.
- Suorituskykytesti: peli pyörii 60 FPS tavoitellulla koneella.

## Rajoitukset ja oletukset
- Oletusympäristö: Windows + Python 3.10+ + Pygame.
- Verkko-ominaisuuksia tai moninpeliä ei toteuteta tässä projektissa.

## Avoimet kohdat / Mahdolliset laajennukset
- Lisää tasoja ja vaikeustasoja
- Peli-asetusten laajentaminen (kontrollerituki, grafiikka-asetukset)
- Tallennus pilveen ja leaderboards

---

Jos haluat, voin jatkossa jakaa tämän vaatimusmäärittelyn pienempiin tehtäviin ja lisätä yksityiskohtaiset käyttöliittymämockupit tai testitapaukset.
