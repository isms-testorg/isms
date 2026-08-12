---
id: pol-business-continuity
title: Richtlinie für Business Continuity und IKT-Bereitschaft
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.29, A.5.30, A.8.14]
---

# Richtlinie für Business Continuity und IKT-Bereitschaft

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Diese Richtlinie legt risikobasierte Mindestanforderungen für die verteilte Softwareentwicklung und den cloudgestützten Betrieb von dev-test fest. Sie unterstützt Vertraulichkeit, Integrität und Verfügbarkeit von Informationen und ist ausschließlich fiktiver Demonstrationsinhalt.

## 2. Anwendungsbereich

Sie gilt für Beschäftigte, Auftragnehmer, Führungskräfte, Repositorys, CI/CD, Endgeräte, Cloud- und SaaS-Dienste, Kundendaten, Geheimnisse, Dokumentation und das ISMS-Repository innerhalb des festgelegten dev-test-Geltungsbereichs. Dienstleisterkomponenten werden über Verträge und Nachweise einbezogen.

## 3. Rollen und Verantwortlichkeiten

Die Geschäftsführung genehmigt diese Richtlinie und akzeptiert eskalierte Risiken. Der CTO gibt die technische Richtung vor; der Engineering Lead setzt die Anforderungen in Entwicklung und Release um; der IT Lead betreibt Identität, Endgeräte und Dienste; die ISMS-Verantwortung pflegt das ISMS, koordiniert Prüfungen und berichtet Probleme. Alle Nutzer befolgen die Richtlinie und melden Abweichungen.

## 4. Anforderungen

Für kritische Abhängigkeiten von GitHub, CI/CD, Identität, Cloud-Hosting, Geheimnisverwaltung und Backups sind Wiederherstellungsprioritäten und Ersatzkontakte dokumentiert. Notfallpläne bewahren Vertraulichkeit, Integrität und Verfügbarkeit bei Störungen. Backups und redundante Verarbeitung werden von der primären Ausfallquelle getrennt geschützt, Wiederherstellungsverfahren mindestens jährlich getestet und Erkenntnisse nachverfolgt. Sicherheit und Eskalation haben Vorrang vor Lieferzielen.

## 5. Ausnahmen

Eine dokumentierte Ausnahme benötigt Geschäftsgrund, betroffene Informationen oder Maßnahmen, Risikobewertung, kompensierende Schutzmaßnahmen, Verantwortlichen, Enddatum und Genehmigung durch Richtlinienverantwortung und Geschäftsführung. Sicherheits- oder Rechtspflichten dürfen nicht aufgehoben werden; abgelaufene Ausnahmen werden geschlossen oder erneut genehmigt.

## 6. Überwachung und Konformität

Die ISMS-Verantwortung prüft stichprobenartig Aufzeichnungen und verfolgt Ziele, Vorfälle, Risiken, Zugriffsprüfungen, Lieferantenprüfungen und Korrekturmaßnahmen. Maßnahmenverantwortliche stellen Nachweise auf Anfrage bereit. Wesentliche Nichtkonformitäten werden an CTO und Geschäftsführung eskaliert. Die Richtlinie wird bis 12.08.2027 oder früher nach wesentlichen Änderungen, Vorfällen, Rechts- oder Dienständerungen geprüft.

## 7. Referenzen

ISO/IEC 27001:2022, Kapitel 4–10; ISMS-Kontext und Risikoregister von dev-test; anwendbare Verfahren; Anwendbarkeitserklärung; DSGVO, Kundenverträge und Verpflichtungsregister. Die Richtlinienverantwortung pflegt die Richtlinie und stellt sicher, dass anwendbare Maßnahmen in Verfahren, Registern und Schulungen berücksichtigt werden. Aufzeichnungen werden im ISMS-Repository kontrolliert geführt und enthalten keine erfundenen Betriebsnachweise.

## 8. Zugehörige Maßnahmen aus Anhang A

- **A.5.29** Informationssicherheit während einer Störung
- **A.5.30** IKT-Bereitschaft für Business Continuity
- **A.8.14** Redundanz von informationsverarbeitenden Einrichtungen
