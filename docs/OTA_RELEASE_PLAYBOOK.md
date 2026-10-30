# ESP8266 Ventilation — πλήρης διαδικασία ιδιωτικού firmware → δημόσιου OTA BIN

**Κατάσταση αναφοράς:** 30 Οκτωβρίου 2026 · **τρέχουσα παραγωγική έκδοση: V2.03**.  
**Σκοπός:** όταν ζητηθεί νέα έκδοση (π.χ. V2.04), να ολοκληρώνεται όλη η διαδικασία σε μία συνεργασία, από τον ιδιωτικό κώδικα μέχρι το επίσημο δημόσιο BIN και manifest, χωρίς να επαναληφθεί η αρχική ρύθμιση.

## Υποδομή που υπάρχει ήδη

- **Ιδιωτικό repository πηγαίου κώδικα:** `ApostolosGit/ESP8266-Ventilation`.
  Για V2.03 χρησιμοποιήθηκε `Ventilation_ESP8266_V2_03.ino` στο `main`.
- **Δημόσιο repository OTA:** `ApostolosGit/ESP8266-OTA.bin`.
- **Public GitHub Actions runner:** χρησιμοποιείται για build χωρίς κατανάλωση του ορίου included minutes των private repositories, υπό τους συνήθεις περιορισμούς/fair-use του GitHub.
- **Read-only private source access:** GitHub Actions Secret `VENTILATION_SOURCE_READ_TOKEN`
  **στο δημόσιο OTA repository**, με fine-grained Personal Access Token και
  `Contents: Read-only` **μόνο** για το `ESP8266-Ventilation`.
  Η τιμή του token δεν πρέπει ποτέ να αποσταλεί σε συνομιλία, logs ή δημόσιο αρχείο.
  Το token ενδέχεται να λήξει και να απαιτήσει ανανέωση.
- **Build workflow V2.03:** [build-ventilation-v203-public.yml](../.github/workflows/build-ventilation-v203-public.yml).
  Χειροκίνητο `workflow_dispatch` από τον ιδιοκτήτη στο `main`, με
  `publish_test_release=true`. **Είναι δεμένο στην V2.03** και πρέπει να
  προσαρμοστεί πριν χρησιμοποιηθεί για διαφορετική έκδοση.
- **Production promotion V2.03:** [promote-ventilation-v203-production.yml](../.github/workflows/promote-ventilation-v203-production.yml).
  Ήταν one-time workflow που ανέβασε επαληθευμένο BIN, manifest και validator
  **μαζί**. **Είναι δεμένο σε hashes/έκδοση V2.03**· δεν χρησιμοποιείται
  αυτούσιο για νέα έκδοση.
- **Public test HTTP ranges:** [verify-ventilation-v203-candidate.yml](../.github/workflows/verify-ventilation-v203-candidate.yml).
- **Regression checks:** `tests/verify_release.py`, `.github/workflows/release-checks.yml`.
  Ελέγχουν και άλλες συσκευές· δεν πρέπει να αλλαχθούν κατά λάθος.

## Τι ακριβώς έγινε στη V2.03

1. Επιλέχθηκε **private μόνο το `.ino`**, ενώ το τελικό OTA BIN και το manifest είναι **public**.
2. Δημιουργήθηκε public Actions workflow που διαβάζει το private sketch με
   fine-grained PAT, κάνει compile **μία φορά** για
   `esp8266:esp8266:nodemcuv2` / ESP8266 core **2.7.2**,
   χωρίς μεταφορά private πηγών σε artifacts/caches.
3. Το πρώτο build [#41081199671](https://github.com/ApostolosGit/ESP8266-OTA.bin/actions/runs/41081199671)
   απέτυχε λόγω Arduino auto-prototype για `LegacyVentCredentialRecord`.
   Η λύση ήταν forward declaration **μόνο στο προσωρινό αντίγραφο build**
   και περιορισμός δημόσιων compiler logs. Το private sketch δεν άλλαξε.
4. Το επόμενο build [#41081881950](https://github.com/ApostolosGit/ESP8266-OTA.bin/actions/runs/41081881950)
   πέρασε και δημοσίευσε το
   [V2.03 test prerelease](https://github.com/ApostolosGit/ESP8266-OTA.bin/releases/tag/ventilation-v2.03-test-41081881950-1).
5. Cloud check [#41083294111](https://github.com/ApostolosGit/ESP8266-OTA.bin/actions/runs/41083294111)
   πέρασε full download, MD5, SHA-256, HTTP `206 Partial Content`,
   `Content-Range`/bytes πρώτου και τελευταίου 4KB chunk,
   και **ένα** redirect προς `release-assets.githubusercontent.com`.
6. Ελέγχθηκε στατικά ότι V2.02 → V2.03 διατηρούν
   `ota_protocol=2`, `profile=ventilation-3ds18b20-2dht11-none`,
   εντολή MQTT `ota_https_v2|size|md5|https_url|profile`,
   pre-OTA fan OFF και SafeMode. Η στατική ανάλυση **δεν** υποκαθιστά
   δοκιμή σε φυσικό ESP8266.
7. Με **ρητή έγκριση του ιδιοκτήτη**, το production workflow
   [#41084674947](https://github.com/ApostolosGit/ESP8266-OTA.bin/actions/runs/41084674947)
   επαλήθευσε ξανά το ακριβές test BIN και έκανε ένα commit με
   `Ventilation_ESP8266_V2_03.bin`, `manifest-ventilation.txt` και
   `tests/verify_release.py`. Πέρασαν όλοι οι τοπικοί και δημόσιοι έλεγχοι.
8. Δημιουργήθηκε το [επίσημο public V2.03 release](https://github.com/ApostolosGit/ESP8266-OTA.bin/releases/tag/ventilation-v2.03).
   **Δεν στάλθηκε MQTT OTA εντολή / δεν εγκαταστάθηκε firmware στη συσκευή.**
   Η προηγούμενη V2.02 παραμένει ως αρχείο στο δημόσιο repo.

**Παραγωγικά στοιχεία V2.03:**

```text
version=2.03
file=Ventilation_ESP8266_V2_03.bin
size=587952
md5=bfe43da5608f113b79519d65563c6da6
sha256=5f28d1247425522a5b0c9785115cae8873902494481d835d8d287f6e0625a35d
build=c9b5df3edd92a67426becae2a5c071f15f2c2af2
source_sha256=b938cf44f2272fff5492f895115944914bcf96e396a74875f46aa05579cbf29e
platform_version=1.04
profile=ventilation-3ds18b20-2dht11-none
ota_protocol=2
hardware_validation=UNVERIFIED
```

## Οδηγός επόμενης έκδοσης — ενιαία ροή

**Είσοδος:** νέα επιθυμητή έκδοση (π.χ. V2.04), διαδρομή
`Ventilation_ESP8266_V2_04.ino` στο private repository και ρητή
έγκριση να δημοσιευτεί ως παραγωγική. Εάν ο πηγαίος κώδικας δεν έχει
ακόμη προετοιμαστεί, πρώτα φτιάχνεται/ελέγχεται στο **private** repo.

1. **Έλεγχος πηγής και ασφάλειας:** επιβεβαίωση `VERSION`,
   `PLATFORM_VERSION`, hardware profile, GPIO/relay polarity,
   OTA protocol, MQTT command parser, safe boot, SafeMode, μνήμη και
   συμπεριφορά OTA. Κρατάμε κρυφά ονόματα/τιμές ιδιωτικών credentials
   και PINs. **Δεν μπαίνει κώδικας στο public repo.**
2. **Προσαρμογή builder στη νέα έκδοση:** νέο versioned workflow (ή
   ελεγμένη γενίκευση) στο public OTA repo. Private source checkout
   με το υφιστάμενο `VENTILATION_SOURCE_READ_TOKEN`, μόνο από
   επιτρεπτό branch/ιδιοκτήτη, χωρίς pull-request untrusted code.
   Εγκατάσταση ESP8266 core 2.7.2 και δημοσίων libraries. Η
   δήλωση `LegacyVentCredentialRecord` στο build copy παραμένει
   μόνο αν εξακολουθεί να χρειάζεται. Δεν δημοσιεύουμε compiler
   snippets ή private artifacts.
3. **Μία δημόσια μεταγλώττιση:** επαλήθευση επιτυχημένου Actions run,
   BIN header `0xE9`, εύλογου μεγέθους, ακριβούς private source
   commit/SHA, MD5, SHA-256. Δημιουργία **δημόσιου TEST prerelease**.
4. **Έλεγχος πραγματικού public CDN:** κατέβασμα ολόκληρου BIN,
   επαλήθευση checksums, ακριβές `206 Partial Content` και
   `Content-Range` για πρώτα/τελευταία (και κατά προτίμηση μεσαία)
   4KB, redirects εντός ορίου firmware. Το production URL πρέπει να
   επιτρέπει τις ίδιες byte-range λήψεις.
5. **Έλεγχος παραγωγικής καταλληλότητας:** ίδια OTA profile/έκδοση
   πρωτοκόλλου στην ήδη εγκατεστημένη συσκευή, ελεύθερος sketch
   χώρος >= μέγεθος νέου BIN, διαθέσιμο TLS heap, ανεμιστήρας OFF
   κατά OTA, δυνατότητα USB recovery. Αν δεν έχουν γίνει επιτόπιες
   μετρήσεις/δοκιμές, **μην παρουσιαστούν ως επιτυχείς**.
6. **Μία ατομική παραγωγική αλλαγή:** αντίγραφο του **ίδιου ήδη
   επαληθευμένου BIN** ως `Ventilation_ESP8266_V2_XX.bin`,
   ενημέρωση `manifest-ventilation.txt` με την ακριβή
   `version`, `file`, `size`, `md5`, `sha256`, `build`,
   `source_sha256`, `platform_version` και αμετάβλητο σωστό
   `profile`, μαζί με προσαρμογή `tests/verify_release.py`.
   Διατήρηση `hardware_validation=UNVERIFIED` όταν δεν έχει
   αποδειχθεί hardware validation.
7. **Υποχρεωτικά release checks:** `python3 tests/verify_release.py`
   και `python3 tests/verify_release.py --remote`; ελέγχουμε
   όλα τα άλλα προϋπάρχοντα OTA profiles, όχι μόνο Ventilation.
   Ελέγχουμε το παραγωγικό `main` manifest και public binary.
8. **Τελική δημοσίευση:** public non-prerelease GitHub Release
   `ventilation-v2.XX` με το production BIN. Αναφέρουμε URLs,
   Actions run links, checksums, αριθμό bytes και κατάσταση
   hardware validation. **Καμία MQTT εντολή/flash** εκτός εάν
   ζητηθεί χωριστά και υπάρχει ασφαλής τρόπος ελέγχου της συσκευής.

**Μην ξαναφτιάξεις token χωρίς λόγο.** Πρώτα χρησιμοποίησε το
υπάρχον GitHub Actions Secret. Αν έχει λήξει, ο ιδιοκτήτης
ενημερώνει το GitHub Secret μέσα από το GitHub UI· δεν γράφει token σε chat.

**Ειδικές προειδοποιήσεις:**

- Η δημοσίευση BIN **δεν σημαίνει** ότι έγινε OTA εγκατάσταση.
- Στην V2.03 και στα προηγούμενα firmware MQTT/OTA το
  `BearSSL::WiFiClientSecure::setInsecure()` δεν επαληθεύει
  το πιστοποιητικό TLS του server. Το MD5 δεν παρέχει
  αυθεντικότητα εκδότη. Απαιτείται σχέδιο ενίσχυσης ασφάλειας.
- Η V2.03 έγινε παραγωγική με **`hardware_validation=UNVERIFIED`**,
  κατόπιν ρητής εντολής. Δεν πρέπει να λέμε ότι έχει δοκιμαστεί
  σε πραγματικό fan relay. Πριν από unattended rollout:
  ελεύθερος χώρος, TLS heap, GPIO12 LOW=OFF, critical sensor
  SafeMode, power-cycle, credential persistence και Recovery.
- Κάθε νέα έκδοση χρειάζεται **νέους versioned SHA/checksum/size**
  και αναθεώρηση version-pinned workflows. Τα V2.03 workflow
  αρχεία **δεν είναι ακόμη ένα γενικό one-click release εργαλείο**.

## Έτοιμη εντολή για νέα συνομιλία

> Διάβασε το `docs/OTA_RELEASE_PLAYBOOK.md` στο δημόσιο GitHub
> `ApostolosGit/ESP8266-OTA.bin` και ολοκλήρωσε **όλη τη
> διαδικασία** για την καινούργια Ventilation ESP8266 V2.XX:
> έλεγχο ιδιωτικού `.ino`, δωρεάν build σε public Actions,
> checksum, HTTP 206, δοκιμαστικό public release, ατομική
> ενημέρωση production BIN + manifest + validator, τελικούς
> τοπικούς/remote ελέγχους, και επίσημο public Release.
> Μην αλλάξεις άλλη συσκευή και μην στείλεις MQTT εντολή OTA.
> Αν η δοκιμή πραγματικού υλικού δεν έχει γίνει, γράψε
> `hardware_validation=UNVERIFIED` και ενημέρωσέ με καθαρά
> για τον κίνδυνο. Η έκδοση είναι V2.XX.

Η διαδικασία εκτελείται στην ενεργή συνομιλία με τις διαθέσιμες
συνδέσεις/Actions· δεν υπονοείται μόνιμη μνήμη του βοηθού,
αυτόματη ενεργοποίηση απεριόριστων builds ή εργασία στο παρασκήνιο.
