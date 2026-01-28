Vaatimusmäärittely 	
Päiväys: 14.1.2026

Yleiskuvaus:
Kevyt 2D-avaruuspeliprojekti (Python + Pygame), jossa pelaaja ohjaa alusta, taistelee vihollisia vastaan ja kerää pisteitä/voittoehdot. Vaatimusmäärittelyssä määritellään projektin toiminnalliset ja ei-toiminnalliset vaatimukset.

Sidosryhmät:
- pelaajat
- kehittäjät
- opettaja.

Laajuus:
Sisältää yksinpelin tilan, mahdollisesti useamman eri tason, pelaajan ohjauksen, viholliset, törmäykset, pisteytyksen, äänen perustoiminnot ja pisteiden tallennuksen. Ei sisällä moninpelitoimintoja tai verkkoyhteyksiä tässä versiossa.

Toiminnalliset vaatimukset:
1. Pelin käynnistys ja valikko
- Kuvaus: sovellus käynnistyy päävalikkoon, josta voi aloittaa pelin, katsoa ohjeet tai lopettaa pelin.
- Tärkeysjärjestys: korkea
- Hyväksymisehto: päävalikko näkyy ja valikot toimivat näppäin-/hiiriohjaimella.

2. Pelaajan ohjaus
- Kuvaus: pelaaja voi liikkua (vasen/oikea/ylös/alas tai vaihtoehtoiset näppäimet), ampua (mahdolliset erikoistoiminnot?)
- Tärkeysjärjestys: korkea
- Hyväksymisehto: ohjaukset reagoivat viiveettä ja animoinnit päivittyvät.

3. Viholliset 
- Kuvaus: Pelissä esiintyy erilaisia vihollisia, joilla on yksinkertainen käyttäytyminen (suora lento, kiertoliike, hyökkäys pelaajaa kohti).
- Tärkeysjärjestys: keskitaso
- Hyväksymisehto: vähintään kaksi vihollistyyppiä näkyvissä ja toimivina.

4. Törmäykset ja vahingot
- Kuvaus: ammuksiin tai vihollisiin osuminen aiheuttaa vahinkoa. Pelaajalla on elämät tai energia (kolme sydäntä, jotka sijaitsevat pelin oikeassa ylälaidassa).
- Tärkeysjärjestys: korkea
- Hyväksymisehto: vahinko ja elämien vähentyminen toimivat oikein, ja kuolema johtaa peli- tai uudelleenaloitusnäkymään.

5. Pisteytys ja tulosnäyttö
- Kuvaus: pelaaja saa pisteitä vihollisen tuhoamisesta, ja pelin lopussa näytetään tulos.
- Tärkeysjärjestys: korkea
- Hyväksymisehto: pisteet kasvavat oikeista toiminnoista, ja ne tallennetaan väliaikaisesti pelisession ajaksi.

6. Äänet ja musiikki
- Kuvaus: taustamusiikki ja äänitehosteet (ammus, räjähdys, valikoissa navigointi).
- Tärkeysjärjestys: matala–keskitaso
- Hyväksymisehto: äänet toistuvat, ja ne voidaan poistaa käytöstä asetuksista.

7. Tallennus ja asetukset
- Kuvaus: pelin perusasetukset (äänenvoimakkuus, avaimet) tallentuvat paikalliseen asetustiedostoon; korkein piste saavutetaan näkyviin.
- Tärkeysjärjestys: keskitaso
- Hyväksymisehto: asetusten muutos pysyy sovelluksen uudelleenkäynnistyksen yli.

8. Ohjeet ja käyttötapa
- Kuvaus: pelin sisäiset ohjeet, jotka selittävät ohjauksen ja pelitavoitteen.
- Tärkeysjärjestys: matala
- Hyväksymisehto: ohjeet saavutetaan päävalikosta.
Pelisisältövaatimukset: tasot (1–5)
Tasojen yhteiset säännöt:
-	Pelaajalla on kolme elämää. Elämät vähenevät törmätessä viholliseen tai vihollisen ammuksiin (tasojen mukaan).
-	Perusvihollinen (tyyppi A) tuhoutuu yhdestä osumasta.
-	Jokaisessa tasossa on pistetavoite ja lopussa päävihollinen (päävihollinen ilmestyy, kun pistetavoite saavutetaan).
1. taso
-	Vihollisia yhteensä 20 (tyyppi A).
-	Viholliset ilmestyvät satunnaisesti yhdestä suunnasta kolmen ryhmissä.
-	Viholliset liikkuvat pelialueella edestakaisin eivätkä ammu.
-	Hyväksymisehto: 20 vihollista pitää tuhota, ennen kuin päävihollinen ilmestyy.
2. taso
-	Sama kuin taso 1, mutta vihollisten nopeus kasvaa (esim. +20–40 %).
-	Hyväksymisehto: vaikeus kasvaa mitattavasti (nopeusparametri muuttuu).
3. taso
- Mukana uusi B-tyypin vihollinen, joka vaatii kolme osumaa.
- Ilmestyy sekä A- että B-tyypin vihollisia.
- Hyväksymisehto: B-tyyppi ei tuhoudu ennen kolmatta osumaa, ja molempien vihollisten pisteytys toimii.
4. taso
- Vähintään yhden tyypin viholliset ampuvat takaisin.
- Uusi vihollistyyppi C (esim. viisi osumaa).
- Hyväksymisehto: vihollisammukset aiheuttavat vahinkoa, ja C-tyypillä on selvä kestävyys- tai mekaniikkaero.
5. taso
- Peli vaikeutuu. Tulee enemmän vihollisia, nopeammat ammukset tms.
- Pelaajalle uusi ase, kyky tai mekaniikka.
- Hyväksymisehto: uusi mekaniikka on käytettävissä ja ohjeistettu, ja se vaikuttaa pelitilanteisiin.

9. Hahmon valitseminen
- Kuvaus: Pelaaja voi valita haluamansa hahmon (aluksen). Kaikki hahmot näyttävät erilaiselta (joko erivärisiä tai kokonaan erilainen alus). Hahmo ampuu myös eri tavalla.
- Prioriteetti: Matala
- Hyväksymiskriteeri: Pelaaja voi valita eri hahmon, joka muuttaa ulkonäköä.

10. Taukotoiminto (?)
- Kuvaus: Pelaaja voi keskeyttää pelin (pause) ja jatkaa myöhemmin.
- Prioriteetti: Keskitaso/matala
- Hyväksymiskriteeri: Peli pysähtyy tauon aikana eikä pelitila muutu.

11. Visuaalinen palaute
- Kuvaus: Osumista ja tapahtumista annetaan visuaalista palautetta (välähdys, räjähdysanimaatio, ruudun tärähdys).
- Prioriteetti: Matala
- Hyväksymiskriteeri: Osuma tai vihollisen tuhoutuminen näkyy selkeästi pelaajalle.

12. Kerättävät esineet (power-upit) (?)
- Kuvaus: Pelissä voi esiintyä kerättäviä esineitä, jotka antavat väliaikaisia etuja (nopeampi ammus, lisäelämä).
- Prioriteetti: Matala
- Hyväksymiskriteeri: Power-up vaikuttaa pelaajan toimintaan määräajan tai pysyvästi.


Ei-toiminnalliset vaatimukset 
1. Suorituskyky
- Kuvaus: Peli tavoittaa vakaan ruudunpäivitysnopeuden (target 60 FPS) tyypillisellä kehityskoneella.
- Mittari: FPS ei putoa alle 30 normaalissa pelitilanteessa.

2. Yhteensopivuus
- Kuvaus: Peli toimii Windows 10/11-ympäristössä, Python 3.10+ ja Pygame-kirjaston avulla.
- Mittari: Asennusohjeilla pelin voi käynnistää vakiokokoonpanolla.

3. Luotettavuus ja vakaus
- Kuvaus: peli ei kaadu tavallisista pelitapahtumista, ja kriittiset virheet käsitellään siististi.
- Mittari: normaaleilla pelin sisäisillä toiminnoilla ei tule kriittisiä poikkeuksia.

4. Käytettävyys
- Kuvaus: peli tarjoaa selkeän käyttöliittymän ja käyttöohjeet, ja ohjaukset ovat intuitiiviset.
- Mittari: ensimmäisen pelikerran jälkeen pelaaja ymmärtää pelin perusmekaniikan ilman ohjausta.

5. Huollettavuus
- Kuvaus: lähdekoodi on kommentoitu ja modulaarinen; jokainen pääkomponentti (pelaaja, vihollinen, pelilogiikka, UI) on omassa moduulissaan.
- Mittari: uuden vihollistyypin lisääminen vaatii enintään yhden uuden moduulin, ja muutoksia pitää tehdä alle kahteen olemassa olevaan tiedostoon.

6. Lokalisaatio
- Kuvaus: pääasiallinen kieli on suomi, mutta tekstit pidetään erillisessä resurssitiedostossa, mikä mahdollistaa muihin kieliin laajentamisen.
- Mahdollinen tavoite: Olisi vaihtoehtona valita englannin kieli. 

7. Turvallisuus
- Kuvaus: sovellus ei kerää henkilökohtaisia tietoja eikä lähetä dataa verkkoon.

8. Resurssien käyttö
- Kuvaus: normaaleissa tilanteissa peli ei ylitä kohtuullista muistinkulutusta (esim. < 500 MB) ja suljettaessa vapauttaa resurssit.

Hyväksymiskriteerit ja testaus
- Yksikkötestit tärkeimmälle pelilogiikalle (pisteytys, törmäystarkistus), missä mahdollista.
- Manuaaliset testit: käynnistys, valikkonavigointi, pelaajan liike, ampuminen, törmäykset, vihollisten ilmestyminen, ääni käyttöön ja pois käytöstä.
- Suorituskykytesti: peli pyörii 60 FPS tavoitellulla koneella.

 Rajoitukset ja oletukset
- Oletusympäristö: Windows + Python 3.10+ + Pygame.
- Verkko-ominaisuuksia tai moninpeliä ei toteuteta tässä projektissa.

Mahdolliset laajennukset
- Lisää tasoja ja vaikeustasoja.
- Peliasetusten laajentaminen (kontrollerituki, grafiikka-asetukset).
- Pilvitallennus ja pistetaulukko.
- Kamera seuraa pelaajaa, ja alusta pystyy liikuttamaan 360 astetta.
