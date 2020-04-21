# Serverless Testing App
##### https://ba-serverless-testing-t6e6p4w6oa-ew.a.run.app  
>**Execute and test simple Java programs in an isolated environment.**

## Requirements  
1. Python 3.7
2. Flask 1.1.1
3. Google Cloud Platform Account (*to run Cloud Run & Container Registry*)

## Build & Run
1. `docker build -t flask/serverless-testing .`
2. `docker run --name serverless-testing -p 8080:8080 flask/serverless-testing`

## Build & Test
1. `docker build -t flask/serverless-testing .`
2. `docker run --name serverless-testing -p 8080:8080 flask/serverless-testing`
3. Open another cmd-tab and paste in:<br>`docker exec serverless-testing python3 -m unittest discover -v`

## Deploy
**[Google Cloud SDK](https://cloud.google.com/sdk/install?hl=de) & Project**

1. Create a Google Cloud Project and install `gcloud` (Google Cloud SDK)
2. Authorize gcloud: `gcloud auth login`
3. Configure gcp-project: `gcloud config set project [PROJECT_ID]`
4. Enable services: <br>
`gcloud services enable containerregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com`
5. Install beta components: `gcloud components install beta`
6. Update components: `gcloud components update`

**Push to [Google Container Registry](https://cloud.google.com/container-registry?hl=de) and [Google Cloud Run](https://cloud.google.com/run?hl=de)** <br>
Navigate to the `cloudbuild.yml` file inside the project: `cd ~/path/to/ba-ahmadi-code`
1. Run `gcloud builds submit`

# Exposé Sirat

**Deutscher Titel:**
Entwicklung einer serverlosen Anwendung für das Testen von Java Programmen in einer isolierten Umgebung

**Englischer Titel:**
Development of a serverless application to test Java programs in an isolated environment

Voraussichtlicher Beginn: Mitte März

* Erstgutachter: Prof. Mauve
* Zweitgutachter: Jens Bendisposto / Prof. Leuschel

## Problembeschreibung
Bei der Korrektur von Studentenabgaben neigt man als Korrektor schnell dazu den Quellcode sofort zu kompiliert und auszuführen, da dadurch bereits ein sehr aussagekräftiger Eindruck über die Qualität der Abgabe ersichtlich wird. Jedoch bringt das Ausführen von fremden und ungeprüften Programmen einige Gefahren mit sich. Es können Sicherheitslücken der Java Virtual-Machine (JVM) oder des eigenen Systems ausgenutzt werden, wodurch Schadprogramme eingeschleust werden können. Um dies zu verhindern kann man das Programm in einer isolierten Umgebung laufen lassen. Das manuelle Aufsetzen einer Virtual Machine (VM) auf dem eigenen Computer benötigt relativ viele Ressourcen und ist zugleich auch sehr aufwendig nur um ein kleines Programm auszuführen. Ein Ausweichen auf traditionelle, externe Dienste von Public Cloud Providern haben den Nachteil, dass man einen stündlichen bzw. monatlichen festen Betrag zahlen muss, auch wenn der Dienst nicht genutzt wird. Man muss sie selbst auf Sicherheitslücken prüfen und verwalten. Eine effizientere Lösung wäre eine serverlose Anwendung. Das Konzept des Serverless-Computing beinhaltet das Entwickeln und Bereitstellen von skalierbaren Anwendungen ohne komplexe Serververwaltung. Zusätzlich gilt, dass nur der eigentliche Verbrauch in Zahlung gestellt werden soll. Dafür bieten Cloud Provider Dienste an, welche von ihnen selbst verwaltet werden, sodass sich Entwickler nur auf die Implementierung ihrer Anwendungen konzentrieren müssen.

## Ziele
Das Ziel dieser Bachelorarbeit ist es eine serverlose Anwendung zu entwickeln, die es ermöglicht einfache Java Programme in einer isolierten Umgebung auszuführen und zu testen. Es soll nur bei der eigentlichen Nutzung der Anwendung Kosten anfallen bzw. bis zu einem gewissen Gesamtverbrauch komplett kostenlos sein. Die Anwendung wird über eine Rest-Schnittstelle mit zwei Endpunkten bereitgestellt und soll für Benutzer einfach zu verwenden sein. Dem Benutzer soll es möglich sein einzelne Javadateien oder eine Zipdatei mit dem Javaprojekt als Inhalt zu übergeben. Das enthalten Javaprojekt innerhalb der Zipdatei muss außerdem Gradle als Build-Management Tool verwenden. Durch die zwei Endpunkte kann der Benutzer entscheiden, ob das übergebene Projekt ausgeführt oder getestet werden soll.

## Erste Gedanken
Der Dienst stellt die view Endpunkte `/run/java` & `run/gradle` sowie `/test/java` & `/test/gradle` zur Verfügung.

Über den ersten Endpunkt `/run/java` kann der Benutzer seine Javadateien kompilieren und ausführen lassen. Durch den zusätzlich gesendeten Parameter `main_file` muss die Java-Klasse angegeben werden, welche die main-Methode enthält. Die Ausgabe des Programms wird dem Benutzer zurückgesendet. Der Benutzer kann dem Dienst über den Endpunkt `/run/gradle` auch eine einzige Zipdatei übergeben. Diese Datei muss das vollständige Javaprojekt enthalten, welches selbst Gradle als Build-Management Tool benutzt. Dann wird der `run`-Task ausgeführt.

**1. Vorraussetzung: Alle Gradle-Projekte müssen das Application-Plugin benutzen**

Über den Endpunkte `/test/java` kann der Benutzer seine Javadateien mittels JUnit testen. Auch hier stehen dem Benutzer die gleichen Möglichkeiten zur Verfügung. Über `/test/gradle` kann eine Zipdatei gesendet werden. Der Dienst führt dann die `test`-Task aus.


## Minimale Anforderungen
Die Minimalen Anforderungen lauten:

- Bereitstellen einer Rest-API
- Einzelne Javadateien mittels Post-Anfrage übergeben, kompilieren und ausführen lassen und die Ausgabe zurück senden.
- Eine Zipdatei übergeben, welches das Javaprojekt mit Gradle als Build-Management Tool enthält. Es können die `run`-Task und die `test`-Task ausgeführt werden. Gradle wird in den Modulen Programmierung und Professionelle Softwareentwicklung verwenden, wodurch Benutzer bzw. andere Dienste die Abgaben sehr leicht testen können.
- System baut auf dem Prinzip des Serverless-Computing auf. Es muss skalierbar sein, kein komplexes Servermanagement enthalten und es darf nur der eigentliche Verbrauch verrechnet werden.
- Die Abgaben werden mit dem OpenJDK11-Build von Azul und JUnit5 Jupiter getestet. Dementsprechend müssen die Abgaben kompatibel sein.

## Mögliche Erweiterungen
- Übergeben, Ausführen und Testen einer Zipdatei, mit enthaltenem Javaprojekt und Maven als Build-Management Tool.
- Ausführen von einzelnen Tests
- Entwicklung einer einfachen Weboberfläche für das Programmieren, Ausführen und Testen im Webbrowser (ähnlich wie [Repl.it](https://repl.it/))  **Da müssen wir drüber reden wenn es so weit ist. Es gibt prinzipiell bei uns schon das Tool eduCode, welches in der Vorlesung Programmierung verwendet wird**
- Andere Versionen von Java und JUnit unterstützen.
- Andere Programmiersprachen unterstützen. Beispielsweise müssen in den Modulen Algorithmen der Bioinformatik, naturwissenschaftliche Informatik sowie Machine Learning alle Abgaben in Python geschrieben werden. Im Modul Compilerbau dürfen Studenten sogar ihre Programmiersprache aussuchen.
- Die Idee auf andere Anwendungsbereiche überführen. Beispielsweise könnte das Öffnen einer Email samt Emailanhang in die isolierte Umgebung verlagert werden. Dem Benutzer wird dann der Inhalt der Email und Emailanhang angezeigt. Änderungen des Inhalts können als JSON-Objekte gesendet werden, welche vom Dienst entsprechend interpretiert werden. Ähnlich könnte man bei Office- und PDF-Dateien vorgehen.

## Verwendete Tools und Programmiersprachen
- Es wird [Google Cloud Run](https://cloud.google.com/run?hl=de) und [Docker](https://www.docker.com/) verwendet. Mit Cloud Run und Docker kann eine beliebige Umgebung verwendet werden. Ein Container kann bis zu 15 Minuten laufen und ist mit max. 2 vCPU und 2 GB Arbeitsspeicher mehr als aussreichend für einfache Javaprogramme.
- Es wird [Python3.7](https://www.python.org/downloads/) mit dem [Flask](https://palletsprojects.com/p/flask/) Framework und [Gunicorn](https://gunicorn.org/) als Http-Server verwendet, um die Rest-Schnittstelle bereitzustellen.
- Für das Ausführen und Testen der Abgaben wird das [OpenJDK11-Build von Azul](https://www.azul.com/downloads/zulu-community/?&architecture=x86-64-bit&package=jdk) verwendet, da das Dockerimage recht klein ist und Java11 eine LTS Version.
- Es wird die [Junit-Platform-Console-Standalone.jar](https://mvnrepository.com/artifact/org.junit.platform/junit-platform-console-standalone) verwendet.

## Ggf. Referenzen

---

# Bachelorarbeit Aufbau

Deckblatt
Kurzzusammenfassung
Inhaltsverzeichnis
Abbildungsverzeichnis
Glossar

### 1. Einleitung
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1.1** Motivation
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1.2** Überblick der Arbeit

### 2. Grundlagen
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.1** Serverless-Computing
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.2** Function as a Service
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.3** Eigenschaften serverloser Architekturen
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.4** Serverlose Dienste
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.4.1** AWS Lambda
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.4.3** Google Cloud Run & AWS Fragate

### 3. Anforderungen
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3.1** Nutzergruppe
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3.2** Minimale Anforderungen
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3.3** Erweiterungen


### 4. Entwicklung
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.1** Dienste und Tools
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.1.1** Docker & Google Container Registry
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.1.2** Google Cloud Run
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.1.3** Flask Framework
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.1.4** OpenJDK 11 & JUnit 5
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.2** Architektur
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.2.1** REST Endpunkte
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.2.2** Ausführen eines Programms
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.2.3** Testen eines Programms

### 5. Testen
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **5.1** Modulaufgaben Programmierung WS 2019
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **5.2** Cold Starts
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **5.3** Skalierbarkeit
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **5.4** Kosten

### 6. Fazit & weitere Anwendungsfälle
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **6.1** Fazit
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **6.2** Weitere Anwendungsfälle
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **6.2.1** Email
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **6.2.2** Dokumente
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **6.2.3** Webbrowser

Literaturverzeichnis
Ehrenwörtliche Erklärung

