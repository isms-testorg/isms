---
id: proc-access-review
title: Verfahren für die Überprüfung von Zugangsrechten
lang: de
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: []
---

# Verfahren für die Überprüfung von Zugangsrechten

Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von dev-test. Es wird unter Versionskontrolle gepflegt; die signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis.

## 1. Zweck

Dieses Verfahren stellt sicher, dass Zugriffe auf GitHub, Repositories, CI/CD, Cloud-Dienste, SaaS-Plattformen, den Identitätsanbieter, die Geheimnisverwaltung, Backups, Endgeräte und das ISMS-Repository weiterhin zur Rolle und zum aktuellen Geschäftsbedarf der betreffenden Person passen.

## 2. Anwendungsbereich

Es gilt für Beschäftigte, Auftragnehmer, Dienstkonten, privilegierte Konten und externe Supportzugriffe innerhalb des ISMS-Geltungsbereichs von dev-test. Es umfasst Änderungen bei Eintritt, Rollenwechsel und Austritt sowie die planmäßige Überprüfung logischer und physischer Zugriffe, soweit dev-test die Entscheidung kontrolliert.

## 3. Rollen und Verantwortlichkeiten

Der IT-Leiter führt die Überprüfung des Identitätsanbieters und der Endgeräte durch und koordiniert Nachweise. Der Engineering Lead prüft Berechtigungen für Repositories, Branches, Deployments und CI/CD. Der ISMS-Verantwortliche koordiniert die Prüfung, kontrolliert die Vollständigkeit, erfasst Feststellungen und eskaliert überfällige Maßnahmen. Der Managing Director genehmigt die Akzeptanz wesentlicher verbleibender Zugriffsrisiken; der CTO genehmigt technische Ausnahmen. Vorgesetzte bestätigen den geschäftlichen Bedarf. Prüfer sollen, soweit praktikabel, unabhängig von der geprüften Zugriffsänderung sein.

## 4. Anforderungen

Die Zugriffsverantwortlichen stellen mindestens vierteljährlich sowie bei Änderungen von Rolle, Vertrag oder Lieferantenbeziehung aktuelle Mitgliedschafts- und Berechtigungsexporte bereit. Die Prüfer vergleichen jeden Eintrag mit Rolle, Beschäftigungs- oder Vertragsstatus, Zuordnung nach dem Prinzip der geringsten Rechte, MFA-Status, letzter Nutzung und genehmigten Ausnahmen. Nicht benötigte Zugriffe werden zeitnah entfernt, übermäßige Rechte reduziert, inaktive Konten deaktiviert und Eigentümer von privilegierten Konten und Dienstkonten dokumentiert. Zugriffe für neu Eintretende werden vor der Bereitstellung genehmigt, bei Rollenwechseln erneut bestätigt und bei Austritt spätestens zum Ende des Bedarfs entzogen. Eingaben sind Zugriffs-Exporte, Personal- und Lieferantenstatus, Rollenzuordnungen, Ticket- oder Pull-Request-Genehmigungen und frühere Feststellungen. Ausgaben sind der freigegebene Prüfdatensatz, Korrekturmaßnahmen, aktualisierte Mitgliedschaften und Eskalationsentscheidungen. Der ISMS-Verantwortliche holt die Genehmigung des Managing Directors für den Abschluss wesentlicher Feststellungen ein.

## 5. Ausnahmen

Vorübergehender Zugriff darf nur für einen bestimmten Zweck, mit benanntem Verantwortlichen, Ablaufdatum und Genehmigung gewährt werden. Würde die sofortige Entfernung einen kritischen Release oder eine Untersuchung unterbrechen, kann der IT-Leiter oder Engineering Lead sie kurz aufschieben, den Grund und eine kompensierende Maßnahme dokumentieren und den ISMS-Verantwortlichen informieren. Gesetzliche, vertragliche oder Sicherheitsanforderungen dürfen nicht durch eine Ausnahme außer Kraft gesetzt werden; ungelöster Zugriff mit hohem Risiko wird an den Managing Director eskaliert.

## 6. Überwachung und Konformität

Der ISMS-Verantwortliche verfolgt Abschluss, überfällige Maßnahmen, Ausnahmen für privilegierte Zugriffe, die fristgerechte Sperrung ausgeschiedener Personen und die MFA-Abdeckung. Vierteljährliche Datensätze werden anhand von Quell-Exporten und GitHub-Historie stichprobenartig geprüft; Abweichungen führen zu einer Nichtkonformität oder Korrekturmaßnahme. Ergebnisse werden in der Managementbewertung berichtet und im ISMS-Repository aufbewahrt. Das Verfahren wird zum nächsten Prüftermin oder nach einer wesentlichen Änderung an Identität, Plattform oder Regulierung überprüft.

## 7. Referenzen

ISO/IEC 27001:2022, Abschnitte 5.3, 7.5, 8.1, 8.2 und 8.3; die Richtlinie zur Zugriffskontrolle; Personal- und Lieferantenunterlagen; sowie Aufzeichnungen des Identitätsanbieters, von GitHub, CI/CD, Cloud, SaaS, Endgeräten, Geheimnisverwaltung, Backups und dem ISMS-Repository und das Verfahren für Nichtkonformität und Korrekturmaßnahmen.

## 8. Zugehörige Maßnahmen aus Anhang A

Keine unmittelbar. Dieses Dokument erfüllt eine Anforderung aus den Abschnitten 4 bis 10 der Norm.
