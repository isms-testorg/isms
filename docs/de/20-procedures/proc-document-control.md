---
id: proc-document-control
title: Lenkung dokumentierter Information
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 24
classification: internal
controls: []
---

# Lenkung dokumentierter Information

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Dieses Verfahren stellt sicher, dass dokumentierte ISMS-Informationen identifizierbar, genehmigt, für berechtigte Nutzer verfügbar, vor unbeabsichtigten Änderungen geschützt und einheitlich aufbewahrt oder gelöscht werden.

## 2. Anwendungsbereich

Es umfasst Richtlinien, Verfahren, Kontext, Register, die Anwendbarkeitserklärung, Ziele, Evidenzindizes, manuell erstellte Nachweise und kontrollierte Vorlagen im dev-test-Repository. Außerdem umfasst es erforderliche externe Dokumente, sofern deren Eigentümer und aktuelle Version bekannt sind.

## 3. Rollen und Verantwortlichkeiten

Der ISMS-Verantwortliche pflegt Dokumentenregister, Prüfkalender und Repository-Struktur. Ein Dokumenten-Owner bleibt für fachliche Richtigkeit, zweisprachige Konsistenz und Review-Bereitschaft verantwortlich. Autoren schlagen Änderungen vor. Ein Mitglied des erforderlichen CODEOWNER-Teams genehmigt unabhängig die endgültige Pull-Request-Revision; GitHub zeichnet den Approver auf. Der Engineering Lead pflegt Repository-Schutz und Automatisierung; der IT-Leiter unterstützt Zugriff und Backup; der Managing Director genehmigt Governance-Dokumente und wesentliche Änderungen.

## 4. Anforderungen

Jedes kontrollierte Dokument enthält in der Quelle Kennung, Titel, Sprache, Version, Owner, Prüfzyklus, Klassifizierung und anwendbare Maßnahmen. Die Pipeline leitet Lebenszyklusstatus, Approver, Genehmigungsdatum und nächstes Review-Datum aus dem endgültigen GitHub-Review und Merge-Nachweis ab. Autoren reichen Änderungen über einen geprüften Pull Request ein; der Owner kontrolliert Sprachgleichheit, Referenzen, Links und Schema; der CODEOWNER-Approver nimmt die Änderung an oder lehnt sie ab. Genehmigte Versionen werden über die bestehende Pipeline veröffentlicht. Die Repository-Historie ist der Änderungsnachweis; erzeugte Release-Ausgaben bleiben im Verantwortungsbereich der Pipeline. Überholte Inhalte werden entsprechend gesetzlichen, vertraglichen und geschäftlichen Aufbewahrungsanforderungen gekennzeichnet oder aufbewahrt; Zugriffe richten sich nach der Klassifizierung. Eingaben sind genehmigte Quelländerungen, Prüffeststellungen, Anforderungen und Betriebserkenntnisse. Ausgaben sind genehmigtes Dokument, Prüfaufzeichnung und abgeleitete Metadaten.

## 5. Ausnahmen

Dringende Korrekturen dürfen bei einem Sicherheits- oder Compliance-Risiko mit beschleunigter Prüfung eingespielt werden. Der Autor dokumentiert Grund und kompensierende Prüfung. Niemand darf erzeugte Build-Ausgaben, Collector-Ausgaben, Signaturen, Prüfsummen oder GitHub-Aufzeichnungen als Ersatz für eine Änderung am Quelldokument verändern.

## 6. Überwachung und Konformität

Der ISMS-Verantwortliche prüft monatlich überfällige Prüfungen, leere Metadaten, defekte Links, doppelte Kennungen, ungelöste Platzhalter, Sprachabweichungen und nicht genehmigte Änderungen. Validator und Pipeline-Prüfungen sind für die strukturelle Konsistenz maßgeblich. Abweichungen werden korrigiert oder als Nichtkonformität erfasst; die Managementbewertung erhält den Status der Dokumentenprüfungen und Aufbewahrungsprobleme. Die Prüfung erfolgt zum nächsten Prüftermin oder nach einer wesentlichen Änderung von Norm, Recht, Organisation oder Geltungsbereich.

## 7. Referenzen

ISO/IEC 27001:2022, Abschnitt 7.5; Beitragsregeln des Repositorys; Richtlinien für Klassifizierung, Aufbewahrung und Änderungssteuerung; `tools/check_isms.py`; sowie die bestehende Rendering- und Release-Pipeline.

## 8. Zugehörige Maßnahmen aus Anhang A

Keine unmittelbar. Dieses Dokument erfüllt eine Anforderung aus den Abschnitten 4 bis 10 der Norm.
