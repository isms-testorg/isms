---
id: ctx-roles
title: Informationssicherheitsrollen und -verantwortlichkeiten
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.2, A.5.3, A.5.4]
---

# Informationssicherheitsrollen und -verantwortlichkeiten

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Dieses Dokument definiert Befugnisse, Verantwortlichkeit und Aufgabentrennung für das fiktive ISMS-Demonstrationssystem von dev-test. Es stellt sicher, dass Entscheidungen benannten Rollen zugewiesen sind und wichtige Tätigkeiten, soweit praktisch möglich, unabhängig geprüft werden.

## 2. Anwendungsbereich

Es gilt für alle Beschäftigten und Auftragnehmer, das ISMS-Repository, Informationswerte, Entwicklungs- und Release-Tätigkeiten, die Verarbeitung von Kundendaten, unterstützende SaaS- und Cloud-Dienste sowie die innerhalb der ISMS-Grenze verwendeten GitHub-Teams und -Repositories.

## 3. Rollen und Verantwortlichkeiten

Der Managing Director (@isms-testorg/dev-managing-director) genehmigt ISMS-Anwendungsbereich, Richtlinien, Ziele, Risikoakzeptanzen auf Managementebene, Ressourcen und Ergebnisse der Managementbewertung. Der CTO (@isms-testorg/dev-cto) gibt die technische Richtung vor und stellt sicher, dass Sicherheit in Architektur- und Engineering-Entscheidungen integriert ist. Der Engineering Lead (@isms-testorg/dev-engineering-lead) verantwortet sichere Entwicklung, Code-Reviews, Branch-Schutz, Behebung von Abhängigkeitslücken und Release-Maßnahmen. Der IT Lead (@isms-testorg/dev-it-lead) verantwortet Identitäts- und Endgeräteverwaltung, Zugriffsprüfungen, Koordination von Sicherungen und Abhängigkeiten von Lieferantendiensten. Der ISMS Owner (@isms-testorg/dev-isms-owner) pflegt dokumentierte Informationen, koordiniert Risikobehandlung, überwacht Ziele und Compliance, bereitet Bewertungen vor und eskaliert Lücken.

Der Dokumenten-Owner ist für fachliche Richtigkeit, zweisprachige Konsistenz und die Review-Bereitschaft verantwortlich. Ein Autor schlägt Änderungen per Pull Request vor und kann der Owner oder ein anderer Mitwirkender sein. Der Approver ist Mitglied des erforderlichen CODEOWNER-Teams und genehmigt unabhängig die endgültige Pull-Request-Revision; GitHub und die Pipeline zeichnen diese Genehmigung auf. Owner und Autoren genehmigen nicht selbst.

Informations- und Dienstverantwortliche legen Schutzanforderungen fest und genehmigen Zugriffe. Mitwirkende befolgen Richtlinien, schützen Zugangsdaten und Geräte und melden Ereignisse. Für Genehmigungen, Rezertifizierung von Zugriffen, Risikoakzeptanz, interne Audits und den Abschluss von Korrekturmaßnahmen ist eine unabhängige Prüfung erforderlich, soweit die Organisation eine geeignete unabhängige prüfende Person stellen kann.

## 4. Anforderungen

Rollenzuweisungen werden in genehmigten Dokumenten und Repository-Berechtigungen festgehalten. Für privilegierte Zugriffe, produktive Änderungen, Releases, Risikoakzeptanzen und die Prüfung von Nachweisen gelten geringste Rechte, Vier-Augen-Prinzip und die Trennung von Antrag, Genehmigung, Umsetzung und Verifikation. Niemand darf den eigenen Zugriff, die eigene Risikoakzeptanz oder den Abschluss der eigenen Korrekturmaßnahme genehmigen. Verhindert die Personalstärke eine vollständige Trennung, dokumentiert der ISMS Owner die Einschränkung und eine kompensierende Prüfung.

## 5. Ausnahmen

Eine vorübergehende Delegation erfordert eine benannte Vertretung, einen festgelegten Befugnisumfang, Beginn und Ende sowie die Information der betroffenen Verantwortlichen. Interessenkonflikte und nicht verfügbare Genehmigende werden an Managing Director und ISMS Owner eskaliert. Eine Delegation überträgt weder die letztendliche Managementverantwortung noch hebt sie gesetzliche, vertragliche, datenschutzrechtliche oder sicherheitsbezogene Pflichten auf.

## 6. Überwachung und Konformität

Der ISMS Owner prüft Rollenzuweisungen, Repository-Berechtigungen, Ausnahmen von der Aufgabentrennung, Schulungsstatus und überfällige Verantwortlichkeiten mindestens jährlich und nach wesentlichen Änderungen. Führungskräfte überwachen die Erfüllung anhand von Zielen, Zugriffsprüfungen, Vorfällen, Audits und Managementbewertung. Abweichungen werden erfasst, risikobewertet, zugewiesen und bis zum Abschluss verfolgt. Dieses fiktive Dokument behauptet weder tatsächliche Wirksamkeit im Betrieb noch eine Zertifizierung.

## 7. Referenzen

Referenzen sind ISO/IEC 27001:2022, Abschnitte 5.3, 5.4, 7.2, 7.3 und 9.3, die Anwendungsbereichserklärung, Verfahren für Zugriffskontrolle, sichere Entwicklung, Änderungsmanagement, Vorfälle, Audits und Korrekturmaßnahmen, Repository-Team-Berechtigungen sowie Ziel- und Risikoregister.

## 8. Zugehörige Maßnahmen aus Anhang A

- **A.5.2** Informationssicherheitsrollen und -verantwortlichkeiten
- **A.5.3** Aufgabentrennung
- **A.5.4** Verantwortlichkeiten der Leitung
