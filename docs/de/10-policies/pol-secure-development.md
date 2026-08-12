---
id: pol-secure-development
title: Richtlinie für sichere Entwicklung
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.8.4, A.8.25, A.8.26, A.8.27, A.8.28, A.8.29, A.8.30, A.8.31, A.8.33]
---

# Richtlinie für sichere Entwicklung

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Diese Richtlinie legt risikobasierte Mindestanforderungen für die verteilte Softwareentwicklung und den cloudgestützten Betrieb von dev-test fest. Sie unterstützt Vertraulichkeit, Integrität und Verfügbarkeit von Informationen und ist ausschließlich fiktiver Demonstrationsinhalt.

## 2. Anwendungsbereich

Sie gilt für Beschäftigte, Auftragnehmer, Führungskräfte, Repositorys, CI/CD, Endgeräte, Cloud- und SaaS-Dienste, Kundendaten, Geheimnisse, Dokumentation und das ISMS-Repository innerhalb des festgelegten dev-test-Geltungsbereichs. Dienstleisterkomponenten werden über Verträge und Nachweise einbezogen.

## 3. Rollen und Verantwortlichkeiten

Die Geschäftsführung genehmigt diese Richtlinie und akzeptiert eskalierte Risiken. Der CTO gibt die technische Richtung vor; der Engineering Lead setzt die Anforderungen in Entwicklung und Release um; der IT Lead betreibt Identität, Endgeräte und Dienste; die ISMS-Verantwortung pflegt das ISMS, koordiniert Prüfungen und berichtet Probleme. Alle Nutzer befolgen die Richtlinie und melden Abweichungen.

## 4. Anforderungen

Sicherheit wird von den Anforderungen bis zur Wartung in den Softwarelebenszyklus integriert. Sicherheits- und Datenschutzanforderungen, Bedrohungsbetrachtungen, genehmigte Architektur, sichere Programmierung, Abhängigkeitsprüfung, Peer-Review, automatisierte Prüfungen und Abnahmetests werden dokumentiert. Entwicklungs-, Test- und Produktionszugriffe sowie Daten werden getrennt. Testdaten sind synthetisch oder minimiert und geschützt. Ausgelagerte Entwicklung folgt denselben Anforderungen, Repository-Kontrollen, Review-Gates und Vorgaben zur Schwachstellenbehebung.

## 5. Ausnahmen

Eine dokumentierte Ausnahme benötigt Geschäftsgrund, betroffene Informationen oder Maßnahmen, Risikobewertung, kompensierende Schutzmaßnahmen, Verantwortlichen, Enddatum und Genehmigung durch Richtlinienverantwortung und Geschäftsführung. Sicherheits- oder Rechtspflichten dürfen nicht aufgehoben werden; abgelaufene Ausnahmen werden geschlossen oder erneut genehmigt.

## 6. Überwachung und Konformität

Die ISMS-Verantwortung prüft stichprobenartig Aufzeichnungen und verfolgt Ziele, Vorfälle, Risiken, Zugriffsprüfungen, Lieferantenprüfungen und Korrekturmaßnahmen. Maßnahmenverantwortliche stellen Nachweise auf Anfrage bereit. Wesentliche Nichtkonformitäten werden an CTO und Geschäftsführung eskaliert. Die Richtlinie wird bis 12.08.2027 oder früher nach wesentlichen Änderungen, Vorfällen, Rechts- oder Dienständerungen geprüft.

## 7. Referenzen

ISO/IEC 27001:2022, Kapitel 4–10; ISMS-Kontext und Risikoregister von dev-test; anwendbare Verfahren; Anwendbarkeitserklärung; DSGVO, Kundenverträge und Verpflichtungsregister. Die Richtlinienverantwortung pflegt die Richtlinie und stellt sicher, dass anwendbare Maßnahmen in Verfahren, Registern und Schulungen berücksichtigt werden. Aufzeichnungen werden im ISMS-Repository kontrolliert geführt und enthalten keine erfundenen Betriebsnachweise.

## 8. Zugehörige Maßnahmen aus Anhang A

- **A.8.4** Zugang zum Quellcode
- **A.8.25** Sicherer Entwicklungslebenszyklus
- **A.8.26** Anforderungen an die Anwendungssicherheit
- **A.8.27** Sichere Systemarchitektur und Prinzipien für die Systemtechnik
- **A.8.28** Sicheres Codieren
- **A.8.29** Sicherheitsprüfung in Entwicklung und Abnahme
- **A.8.30** Ausgegliederte Entwicklung
- **A.8.31** Trennung von Entwicklungs-, Test- und Produktionsumgebungen
- **A.8.33** Testinformationen
