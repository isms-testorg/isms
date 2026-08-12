---
id: pol-asset-management
title: Richtlinie für Werteverwaltung und Informationsklassifizierung
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.9, A.5.12, A.5.13, A.7.10, A.7.14, A.8.10]
---

# Richtlinie für Werteverwaltung und Informationsklassifizierung

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Diese Richtlinie legt risikobasierte Mindestanforderungen für die verteilte Softwareentwicklung und den cloudgestützten Betrieb von dev-test fest. Sie unterstützt Vertraulichkeit, Integrität und Verfügbarkeit von Informationen und ist ausschließlich fiktiver Demonstrationsinhalt.

## 2. Anwendungsbereich

Sie gilt für Beschäftigte, Auftragnehmer, Führungskräfte, Repositorys, CI/CD, Endgeräte, Cloud- und SaaS-Dienste, Kundendaten, Geheimnisse, Dokumentation und das ISMS-Repository innerhalb des festgelegten dev-test-Geltungsbereichs. Dienstleisterkomponenten werden über Verträge und Nachweise einbezogen.

## 3. Rollen und Verantwortlichkeiten

Die Geschäftsführung genehmigt diese Richtlinie und akzeptiert eskalierte Risiken. Der CTO gibt die technische Richtung vor; der Engineering Lead setzt die Anforderungen in Entwicklung und Release um; der IT Lead betreibt Identität, Endgeräte und Dienste; die ISMS-Verantwortung pflegt das ISMS, koordiniert Prüfungen und berichtet Probleme. Alle Nutzer befolgen die Richtlinie und melden Abweichungen.

## 4. Anforderungen

Das Asset-Gruppenregister erfasst Informationen, Systeme, Geräte, Medien, Dienste und Verantwortliche. Verantwortliche klassifizieren Informationen als öffentlich, intern, vertraulich oder streng vertraulich, kennzeichnen sie soweit praktikabel und legen Handhabung sowie Aufbewahrung fest. Vertrauliche und streng vertrauliche Informationen werden nur mit autorisierten Empfängern geteilt. Medien und Endgeräte werden beim Transport geschützt und vor Aussonderung sicher gelöscht oder vernichtet; Löschungen werden dokumentiert.

## 5. Ausnahmen

Eine dokumentierte Ausnahme benötigt Geschäftsgrund, betroffene Informationen oder Maßnahmen, Risikobewertung, kompensierende Schutzmaßnahmen, Verantwortlichen, Enddatum und Genehmigung durch Richtlinienverantwortung und Geschäftsführung. Sicherheits- oder Rechtspflichten dürfen nicht aufgehoben werden; abgelaufene Ausnahmen werden geschlossen oder erneut genehmigt.

## 6. Überwachung und Konformität

Die ISMS-Verantwortung prüft stichprobenartig Aufzeichnungen und verfolgt Ziele, Vorfälle, Risiken, Zugriffsprüfungen, Lieferantenprüfungen und Korrekturmaßnahmen. Maßnahmenverantwortliche stellen Nachweise auf Anfrage bereit. Wesentliche Nichtkonformitäten werden an CTO und Geschäftsführung eskaliert. Die Richtlinie wird bis 12.08.2027 oder früher nach wesentlichen Änderungen, Vorfällen, Rechts- oder Dienständerungen geprüft.

## 7. Referenzen

ISO/IEC 27001:2022, Kapitel 4–10; ISMS-Kontext und Risikoregister von dev-test; anwendbare Verfahren; Anwendbarkeitserklärung; DSGVO, Kundenverträge und Verpflichtungsregister. Die Richtlinienverantwortung pflegt die Richtlinie und stellt sicher, dass anwendbare Maßnahmen in Verfahren, Registern und Schulungen berücksichtigt werden. Aufzeichnungen werden im ISMS-Repository kontrolliert geführt und enthalten keine erfundenen Betriebsnachweise.

## 8. Zugehörige Maßnahmen aus Anhang A

- **A.5.9** Inventar der Informationen und anderer damit verbundener Werte
- **A.5.12** Klassifizierung von Informationen
- **A.5.13** Kennzeichnung von Informationen
- **A.7.10** Speichermedien
- **A.7.14** Sichere Entsorgung oder Wiederverwendung von Geräten und Betriebsmitteln
- **A.8.10** Löschung von Informationen
