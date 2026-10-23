# FORMA — Pocket Beat Studio

React, Tailwind CSS und Web Audio. Start: `npm install`, dann `npm run dev`.
`npm run build` erstellt `dist/`. `npm test` prüft Aufnahme, Arrangement, Migration und Audio-Steuerung mit einem Audio-Mock.

## Einspielen und komponieren

1. Clip A–D wählen. Jeder Clip enthält eine eigene Variante für jede der vier Spuren.
2. Eine Instrumentenzeile auswählen, um deren Klang einzustellen: Classic, Dream, Rage oder Melodic sowie Lautstärke, Tonhöhe und Ausklang. Presets verändern keine gesetzten Schritte.
3. Schritte anklicken oder „Pads aufnehmen“ starten und mit den Pads beziehungsweise 1–4 spielen. Schläge ergänzen den gewählten Clip im 16-Schritt-Raster. Aufnahme stoppen beendet nur die Aufnahme; der Loop läuft weiter. Play/Pause stoppt auch die Aufnahme.
4. Akzente verändern die Stärke jedes Schlags. Bei Bass kann pro Schritt eine Note in C-Moll gewählt werden. Ein Akzentwert von null schaltet den Schritt aus.
5. Kopieren überträgt den ausgewählten Instrumentenclip in den nächsten Buchstaben. Das ersetzt dessen bisherige Schritte und Noten. Leeren und Zufall betreffen ebenfalls nur die ausgewählte Spur und den ausgewählten Clip.
6. Unter Compose pro Spur und Takt A–D oder „–“ für Stille wählen. „Song · 8 Takte“ auswählen und Play drücken. Das Arrangement wiederholt sich nach acht Takten. Clip-Loop wiederholt den aktuell gewählten Clip auf allen Spuren.

Die Aufnahme wechselt zum Clip-Loop. Sie speichert Pad-Ereignisse und benötigt keinen Mikrofonzugriff. Pro Schritt ist ein Schlag möglich. Mute/Solo betreffen die Sequencer-Wiedergabe; Live-Pads bleiben zum Vorhören hörbar.

Die Leertaste startet/pausiert außerhalb von Formularen und Buttons. BPM verändert das Tempo. Drehregler werden horizontal gezogen und können mit den Pfeiltasten bedient werden. „Audio starten / Audio on“ setzt Audio zurück und spielt einen Testton bei 65 %.

## Speicherung

Das vollständige Projekt wird unter `forma-studio` in localStorage gespeichert. Bestehende `forma-pattern`-Beats werden beim ersten Start in Clip A übernommen; der alte Speichereintrag bleibt erhalten. „Projekt speichern“ lädt eine JSON-Sicherung herunter. Dateiimport und WAV-Export sind noch nicht enthalten.

## Verifikation und Grenzen

Produktionsbuild und sechs automatisierte Tests erfolgreich. Die Tests prüfen Audio-Aufrufe mit einem Mock, nicht den hörbaren Klang. Browser-/Hörprüfung ist in der Entwicklungsumgebung mangels Browser nicht möglich. Hosting war wegen blockiertem Netzwerk nicht erreichbar. Die Website steuert noch keine physische Hardware.

## Instrumenten-Grids und Soundbanks

Über die Instrument-Tabs wechselst du zwischen fünf eigenen 4×4-Grids für Kick, Snare, Hi-hat, Bass und Synth. Jedes Instrument merkt sich während der Sitzung seinen eigenen ausgewählten Clip A–D. Die anderen Spuren spielen weiter. Die fünfte Spur ist auch mit Taste 5 spielbar und hat wie der Bass eine Notenauswahl.

Die zwölf Drum-Sounds sind eigenständige PCM-WAV-One-Shots in `public/sounds/`, keine bloßen Filtervarianten desselben Samples. Sie wurden mit `python3 scripts/make-sounds.py` aus unterschiedlichen Syntheserezepten erzeugt; externe Samples werden nicht benötigt. Bass und Synth besitzen vier unterschiedliche Klangerzeuger. Ein Klick auf einen Sound spielt die Vorschau. Beim ersten Start werden alle kleinen WAV-Dateien lokal geladen und dekodiert.

„AFTER DARK“ lädt und spielt ein eigenes düsteres Rage-Beispiel bei 146 BPM: Clipped Kick, gestapelter Clap, metallische Hats, tiefe 808 und schwebende Synth-Melodie mit acht Takten Arrangement. Es ist eine eigene Komposition, keine Reproduktion eines veröffentlichten Songs. Vor dem Laden wird das bisherige Projekt unter `forma-before-demo` gesichert. „Vorheriges Projekt zurückholen“ stellt es wieder her. Wiederholtes Laden der Demo überschreibt diese Sicherung nicht.

Bestehende vier Spuren werden unverändert übernommen; die neue Synth-Spur ist bei der Migration zunächst leer. Aktueller Stand: neun automatisierte Tests und Produktionsbuild bestanden. Eine tatsächliche Hör- und Browserprüfung ist in dieser Umgebung weiterhin nicht möglich.

## Visuelle Melodie und geführter Einstieg

Synth und Bass verwenden ein Notenraster: 16 Spalten sind die Zeit, fünf Zeilen die Tonhöhen C, E♭, G, B♭, C. Oben ist höher. Klick setzt einen Ton und spielt ihn vor; ein Klick auf dieselbe Zelle entfernt ihn, ein Klick auf eine andere Höhe in derselben Spalte verschiebt ihn. Pro Schritt gibt es eine Note. Bestehende aktive Töne außerhalb der fünf Standardzeilen erhalten automatisch zusätzliche sichtbare Zeilen und werden nicht verändert.

„Hoch & runter einsetzen“ setzt acht Noten im aktuellen Instrumentenclip: C, E♭, G, B♭, hohes C, B♭, G, E♭. Die Klangfarbe bleibt erhalten. „Tief / Normal / Hoch“ verschiebt die ganze Instrumentenspur um eine Oktave. Es sind einzelne Noten; kontinuierliches Pitch-Glide und editierbare Notenlängen sind noch nicht enthalten.

Die aufklappbare Anleitung „Deinen eigenen Beat bauen“ bietet einen leeren Start bei 135 BPM und einzeln einsetzbare Drum-Startpatterns. „Leeren Beat starten“ sichert das vorherige Projekt über dieselbe Rückholfunktion wie die Demo. Anschlag und weitere Klangparameter sind unter „Fein einstellen“ aufklappbar. Die Beispiele sind eigene Übungen, keine Transkription von Catch a Kill. Offizielle Referenz: https://www.youtube.com/watch?v=TTcrWFZFGFI

Aktuelle Verifikation: zwölf Tests und Produktionsbuild erfolgreich. Browser-/Hörprüfung bleibt in dieser Umgebung nicht möglich.

## Dark guitar und VELVET STATIC

Das Menü „Deine Soundrichtung“ wählt einen vollständigen Satz aufeinander abgestimmter Sounds für alle fünf Spuren: Dark guitar (intern Nocturne), Dream / Cloud, Rage, Melodic oder Classic. Es verändert Klangfarbe, Spurpegel, Ausklang und Tonlage. Gesetzte Noten, Rhythmen, Tempo, Clips, Mute/Solo und Arrangement bleiben erhalten. Werden anschließend einzelne Soundkarten geändert, zeigt das Menü „Eigene Mischung“.

Die Nocturne-Bank enthält fünf neue originale WAV-Dateien: Shadow punch, Velvet clap, Dust tick, Low voltage 808 und Faded strings. Der Saitensound nutzt ein physikalisches Zupfmodell mit Quinte/Oktave, Verstärkersättigung und leichtem Doubling; es ist keine externe Gitarrenaufnahme. Erzeugen: `python3 scripts/make-nocturne.py`.

„VELVET STATIC“ ist eine eigene Komposition bei 136 BPM mit einer C–A♭–E♭–B♭-Bewegung, Saitenfigur, späterem Bass-Einsatz und Drum-Break. „Beat laden & spielen“ öffnet den editierbaren Acht-Takte-Ausschnitt im Song-Modus. Der ältere AFTER-DARK-Beat bleibt über die Demo-Auswahl verfügbar. Das vorherige Projekt wird über die bestehende Sicherung rückholbar gehalten.

Unter `public/demo/velvet-static.wav` liegt die ausgearbeitete 40-Takte-Fassung (73,59 Sekunden, mono, 22.050 Hz, 16 Bit): vier Takte Intro, acht Hook, acht Verse, vier Break, sechzehn finale Hook plus Ausklang. Sie verwendet dieselben Sounds und Clip-Noten und ist über den Banner herunterladbar. Die WAV ist eine fertige Demoversion; Live-Änderungen am Projekt aktualisieren sie nicht. Die zugehörigen Clips stehen in `public/demo/velvet-static.json`. Neu rendern mit `python3 scripts/render-nocturne.py`.

Verifikation: 16 Tests prüfen Projektlogik, Sampledateien, Soundrichtungen, neue Komposition und WAV-Dauer, Headroom sowie Intro/Drop-Dynamik. Die Audiosignale und der Build werden technisch geprüft; Browser- und Hörprüfung sind hier weiterhin nicht verfügbar.

## Dunklere Fassung

VELVET STATIC verwendet nun eine tiefere, engere Saitenmelodie (Spurtonlage −24 Halbtöne), weniger obere Saitenanteile, einen weicheren Anschlag, leise Hats und tiefere Filtergrenzen. Der Gleichspannungsanteil des Zupfmodells wird vor dem Normalisieren entfernt; zusätzlich hat die Wiedergabe einen Hochpass. Live-Demo und WAV wurden aktualisiert. Für die neue Fassung Seite neu laden und den Beat erneut laden. Der WAV-Export bleibt rund 74 Sekunden lang. „Sehr tief“ ist im Notenraster verfügbar.

## Vocal booth / LOW LIGHT

Über „Eigene Stimme aufnehmen“ zum neuen Bereich springen. Er spielt die fertige dunkle VELVET-STATIC-WAV; Änderungen im Instrumenten-Sequencer werden nicht automatisch übernommen. Alternativ eine eigene Instrumentaldatei laden. Eigene Instrumentals bleiben bis zum Neuladen im Arbeitsspeicher; Takes werden in IndexedDB gespeichert.

1. Kopfhörer verwenden. Hook, Verse oder eine eigene Startsekunde wählen.
2. „Stimme aufnehmen“ klicken, Mikrofon im Browser freigeben und den Vierer-Vorzähler abwarten. Kein Mikrofon-Monitoring: Es wird nur der Beat ausgegeben und die Stimme separat trocken aufgezeichnet.
3. Stoppen und „Beat + Stimme anhören“ klicken. Dark Lead, Ghost Layer oder Clean Guide wählen. Der Signalweg enthält Hoch-/Tiefpass, Kompression, sanfte Sättigung, Echo und dunklen Hall. Die Effekte verändern nicht das Original. Automatische Tonhöhenkorrektur ist nicht enthalten.
4. Neue Takes schalten frühere Takes im Mix zunächst aus. Mit den Häkchen mehrere Takes aktivieren. Pro Take stehen Lautstärke, Vocal-Preset und ±250 ms Timing-Korrektur bereit. Effektänderungen wirken beim nächsten Abspielen.
5. Die Originalaufnahme über das Downloadsymbol sichern. „Beat + aktivierte Stimmen als WAV“ rendert den gesamten Beat mit den ausgewählten Takes und Effekten in eine Stereo-WAV. Ein zusätzlicher Hallausklang wird berücksichtigt.

Mikrofonzugriff wird ausschließlich nach Klick angefragt und nach Stoppen oder Verlassen beendet. Aufnahmen werden nicht hochgeladen. Browser verweigert Mikrofonzugriff: Berechtigung prüfen und die Seite über localhost oder HTTPS öffnen. Aufnahme und tatsächliche Mikrofonlatenz konnten hier mangels verfügbarem Browser/Mikrofon nicht überprüft werden. Ein konstanter Versatz kann pro Take korrigiert werden.

Der eigene englische Text LOW LIGHT steht neben der Aufnahme und in `public/demo/low-light.txt`: acht Hook-Zeilen und acht Verse-Zeilen, eine Zeile pro Takt. Er ist für einen tiefen, halb gesungenen Vortrag gedacht.

Automatisierte Prüfung: 21 Tests für Projektlogik, neue dunkle Fassung, Audio-Signalweg, Vocal-Zeitpositionen, Wellenform und Stereo-WAV-Kodierung. Der Produktionsbuild wird geprüft. Die Tests ersetzen keinen echten Browser-/Mikrofon-/Hörtest.
# forma
