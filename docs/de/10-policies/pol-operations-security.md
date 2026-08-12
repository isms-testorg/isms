---
id: pol-operations-security
title: Richtlinie für Betriebssicherheit
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.37, A.8.6, A.8.7, A.8.8, A.8.9, A.8.13, A.8.15, A.8.16, A.8.17, A.8.19, A.8.32, A.8.34]
---

# Richtlinie für Betriebssicherheit

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Diese Richtlinie legt risikobasierte Mindestanforderungen für die verteilte Softwareentwicklung und den cloudgestützten Betrieb von dev-test fest. Sie unterstützt Vertraulichkeit, Integrität und Verfügbarkeit von Informationen und ist ausschließlich fiktiver Demonstrationsinhalt.

## 2. Anwendungsbereich

Sie gilt für Beschäftigte, Auftragnehmer, Führungskräfte, Repositorys, CI/CD, Endgeräte, Cloud- und SaaS-Dienste, Kundendaten, Geheimnisse, Dokumentation und das ISMS-Repository innerhalb des festgelegten dev-test-Geltungsbereichs. Dienstleisterkomponenten werden über Verträge und Nachweise einbezogen.

## 3. Rollen und Verantwortlichkeiten

Die Geschäftsführung genehmigt diese Richtlinie und akzeptiert eskalierte Risiken. Der CTO gibt die technische Richtung vor; der Engineering Lead setzt die Anforderungen in Entwicklung und Release um; der IT Lead betreibt Identität, Endgeräte und Dienste; die ISMS-Verantwortung pflegt das ISMS, koordiniert Prüfungen und berichtet Probleme. Alle Nutzer befolgen die Richtlinie und melden Abweichungen.

## 4. Anforderungen

Betriebssysteme nutzen genehmigte Baselines, Änderungssteuerung, Schwachstellenbehebung, Schadsoftware-Schutz, Backups, Protokollierung, Überwachung und synchronisierte Zeit. Kapazität und Verfügbarkeit kritischer Dienste werden geprüft. Software darf nur durch autorisierte Personen aus vertrauenswürdigen Quellen installiert werden. Protokolle werden vor Veränderung geschützt und gemäß Verpflichtungsregister aufbewahrt. Änderungen werden vor Veröffentlichung getestet und genehmigt; Auditprüfungen nutzen kontrollierte Zugriffe und schützen Produktionsinformationen.

## 5. Ausnahmen

Eine dokumentierte Ausnahme benötigt Geschäftsgrund, betroffene Informationen oder Maßnahmen, Risikobewertung, kompensierende Schutzmaßnahmen, Verantwortlichen, Enddatum und Genehmigung durch Richtlinienverantwortung und Geschäftsführung. Sicherheits- oder Rechtspflichten dürfen nicht aufgehoben werden; abgelaufene Ausnahmen werden geschlossen oder erneut genehmigt.

## 6. Überwachung und Konformität

Die ISMS-Verantwortung prüft stichprobenartig Aufzeichnungen und verfolgt Ziele, Vorfälle, Risiken, Zugriffsprüfungen, Lieferantenprüfungen und Korrekturmaßnahmen. Maßnahmenverantwortliche stellen Nachweise auf Anfrage bereit. Wesentliche Nichtkonformitäten werden an CTO und Geschäftsführung eskaliert. Die Richtlinie wird bis 12.08.2027 oder früher nach wesentlichen Änderungen, Vorfällen, Rechts- oder Dienständerungen geprüft.

## 7. Referenzen

ISO/IEC 27001:2022, Kapitel 4–10; ISMS-Kontext und Risikoregister von dev-test; anwendbare Verfahren; Anwendbarkeitserklärung; DSGVO, Kundenverträge und Verpflichtungsregister. Die Richtlinienverantwortung pflegt die Richtlinie und stellt sicher, dass anwendbare Maßnahmen in Verfahren, Registern und Schulungen berücksichtigt werden. Aufzeichnungen werden im ISMS-Repository kontrolliert geführt und enthalten keine erfundenen Betriebsnachweise.

## 8. Zugehörige Maßnahmen aus Anhang A

- **A.5.37** Dokumentierte Betriebsabläufe
- **A.8.6** Kapazitätssteuerung
- **A.8.7** Schutz gegen Schadsoftware
- **A.8.8** Handhabung von technischen Schwachstellen
- **A.8.9** Konfigurationsmanagement
- **A.8.13** Sicherung von Informationen
- **A.8.15** Protokollierung
- **A.8.16** Überwachungsaktivitäten
- **A.8.17** Uhrensynchronisation
- **A.8.19** Installation von Software auf Systemen im Betrieb
- **A.8.32** Änderungssteuerung
- **A.8.34** Schutz von Informationssystemen während Prüfungstests
