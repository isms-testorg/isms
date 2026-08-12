---
id: proc-incident-response
title: Verfahren für die Reaktion auf Vorfälle
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.25, A.5.26, A.5.27, A.5.28]
---

# Verfahren für die Reaktion auf Vorfälle

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Dieses Verfahren steuert die Reaktion auf vermutete oder bestätigte Informationssicherheitsereignisse, damit dev-test Schäden begrenzt, vertrauenswürdige Dienste wiederherstellt, Meldepflichten erfüllt und aus Vorfällen lernt.

## 2. Anwendungsbereich

Es umfasst Ereignisse mit Quellcode, Kundendaten, Zugangsdaten und Geheimnissen, Endgeräten, GitHub, CI/CD, Cloud- und SaaS-Diensten, Identität, Backups, dem ISMS-Repository und Lieferanten. Es gilt für Erkennung, Triage, Eindämmung, Beseitigung, Wiederherstellung, Kommunikation und Beweissicherung.

## 3. Rollen und Verantwortlichkeiten

Wer ein Ereignis bemerkt, meldet es unverzüglich über den freigegebenen internen Kanal an den IT-Leiter oder ISMS-Verantwortlichen. Der IT-Leiter koordiniert technische Eindämmung; der Engineering Lead bearbeitet Repositories, Builds und Releases; der CTO leitet wesentliche technische Entscheidungen; der ISMS-Verantwortliche führt den Vorfalldatensatz und die Compliance-Bewertung; der Managing Director genehmigt wesentliche geschäftliche oder kundenseitige Kommunikation. Bei Ereignissen mit personenbezogenen Daten wird rechtliche oder datenschutzrechtliche Beratung eingeholt. Der Incident Lead verteilt Aufgaben und hält Entscheidungsbefugnisse klar.

## 4. Anforderungen

Der Melder dokumentiert Zeitpunkt, Quelle, betroffenen Dienst, beobachtete Fakten und sichere Kontaktdaten. Der Incident Lead weist eine Schwere zu, unterscheidet Ereignis und Vorfall, sichert relevante Logs und flüchtige Beweise soweit möglich und eröffnet einen Vorfalldatensatz. Das Team grenzt die Bedrohung ein, rotiert offengelegte Geheimnisse, isoliert Systeme, sichert Umfang und Ursache, beseitigt missbräuchlichen Zugriff und stellt aus vertrauenswürdigen Versionen oder Backups wieder her. Kommunikation ist sachlich, auf das erforderliche Wissen beschränkt und vor Veröffentlichung genehmigt. Der ISMS-Verantwortliche bewertet GDPR/DSGVO-, Vertrags-, Lieferanten- und Behördenpflichten und koordiniert Fristen mit Managing Director und Beratern. Für den Abschluss werden Auswirkung, Zeitlinie, Beweise, Maßnahmen, verbleibendes Risiko, betroffene Parteien und Erkenntnisse dokumentiert. Eingaben sind Alarme, Meldungen, Logs, Zugriffshistorie, Backup-Status und Lieferantenmitteilungen. Ausgaben sind Vorfalldatensatz, gesicherte Beweise, Wiederherstellungsbestätigung, erforderliche Meldungen und Korrekturmaßnahmen.

## 5. Ausnahmen

Notfallmaßnahmen zur Eindämmung dürfen ohne vorherige Genehmigung erfolgen, wenn Verzögerung den Schaden vergrößern würde; der Incident Lead dokumentiert die Entscheidung und informiert CTO und ISMS-Verantwortlichen so bald wie möglich. Beweise dürfen nicht unnötig verändert werden. Ist eine Meldefrist oder Kundenvereinbarung gefährdet, wird unverzüglich an den Managing Director eskaliert.

## 6. Überwachung und Konformität

Der ISMS-Verantwortliche prüft nach jedem Vorfall und mindestens vierteljährlich Schwereentscheidungen, Reaktionszeiten, Eindämmung, Meldeentscheidungen, Vollständigkeit der Beweise, Wiederherstellungstests und wiederkehrende Ursachen. Wesentliche Vorfälle lösen Korrekturmaßnahmen und eine Managementbewertung aus. Das Verfahren wird regelmäßig geübt und jährlich oder nach einem wesentlichen Vorfall, einer Rechts- oder Plattformänderung geprüft.

## 7. Referenzen

ISO/IEC 27001:2022, Abschnitte 7.5, 8.1, 8.2 und 10.2; Richtlinien für Vorfallmanagement, Zugriffskontrolle, Backup, Datenschutz, Lieferanten und Kommunikation; GDPR/DSGVO- und Kundenvertragsanforderungen; sowie die unten aufgeführten Maßnahmen A.5.25–A.5.28.

## 8. Zugehörige Maßnahmen aus Anhang A

- **A.5.25** Beurteilung und Entscheidung über Informationssicherheitsereignisse
- **A.5.26** Reaktion auf Informationssicherheitsvorfälle
- **A.5.27** Erkenntnisse aus Informationssicherheitsvorfällen
- **A.5.28** Sammeln von Beweismaterial
