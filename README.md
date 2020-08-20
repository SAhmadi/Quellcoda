# Serverless Testing App
###Execute and test simple Java programs in an isolated environment.
Live: https://ba-serverless-testing-t6e6p4w6oa-ew.a.run.app  

## All repositories
- In tihs repo you will find the code for the serverless Backendd
    - Inside `tests/programmierung_testaufgaben_ws18` you will find the a few changed excercies for the 
    course `Programmierung WS 18`. If you want to test them by sending them to `/run/gradle` and `/test/gradle`
    endpoints, make sure to add the necessary query-strings `?args1=Value1&args2=Value...`. Look inside the
    source files to see want arguments are needed and what they do.
    - In `benchmark_scripts` you will find the scipts and manually added results for the benchmarks.

- Thesis Repo:\
https://gitlab.cs.uni-duesseldorf.de/cn-tsn/students/bachelor/ba-ahmadi-thesis
- Frontend Repo (Christian sollte Zugriff haben, habe ihn als Developer hinzugefügt):\
https://gitlab.cs.uni-duesseldorf.de/ahmadi/ba-ahmadi-ui

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

If you want to `run` the container multiple times, change the name of it `--name serverless-testing-<version>`.
Otherwise the names will collide with the already running container.
Dont forget to change step the name in step 3 too.

## Deploy
**[Google Cloud SDK](https://cloud.google.com/sdk/install?hl=de) & Project**

1. Create a Google Cloud Project and install `gcloud` (Google Cloud SDK)
2. Setup you Google Cloud Account (https://cloud.google.com/run/docs/quickstarts/build-and-deploy?hl=de)
see step 2 of the link. A credit card needs to be added to the account (even if the service has a free tier)
3. Authorize gcloud: `gcloud auth login`
4. Configure gcp-project: `gcloud config set project [PROJECT_ID]`
5. Enable services: <br>
`gcloud services enable containerregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com`
6. Install beta components: `gcloud components install beta`
7. Update components: `gcloud components update`
8. `gcloud builds submit --tag eu.gcr.io/ba-serverless-testing/ba-serverless-testing-image`
9. `gcloud run deploy ba-serverless-testing --image eu.gcr.io/ba-serverless-testing/ba-serverless-testing-image --region europe-west1 --platform managed --allow-unauthenticated`

Once setup, you will only need step 8 and 9.
If you want to deploy a new revision of the backend service, use command 8 and 9
or push to master branch, it will automatically push to Google Cloud Run Service. 

## Sending curl request to the REST-API
1. 


# Exposé Sirat

**Deutscher Titel:**
Entwicklung einer serverlosen Anwendung für das Testen von Java Programmen in einer isolierten Umgebung

**Englischer Titel:**
Development of a serverless application to test Java programs in an isolated environment

Voraussichtlicher Beginn: Mitte März
Abgabedatum: 20.08.2020

* Erstgutachter: Prof. Mauve
* Zweitgutachter: Prof. Leuschel

## Problembeschreibung
Während meiner Korrektor-Tätigkeit neigte ich schnell dazu den Quellcode der Studenten sofort zu kompilieren
und das resultierende Programm auszuführen, 
weil dadurch bereits ein sehr aussagekräftiger Eindruck über die Qualität der Abgabe ersichtlich wird. 
Jedoch bringt das Ausführen von fremden und ungeprüften Programmen einige Gefahren mit sich.
Es können Sicherheitslücken der \textit{Java Runtime Environment} (JRE) \cite{Jre}
oder des eigenen Systems ausgenutzt werden, wodurch Schadprogramme eingeschleust
werden können \cite{CveJreVuln}.
Um dies zu verhindern, kann man das Programm in einer isolierten Umgebung laufen lassen.
Das manuelle Aufsetzen einer \textit{Virtual-Machine} (VM) \cite{RedHatVM} auf dem eigenen Computer
benötigt relativ viele Ressourcen und ist zugleich auch viel Aufwand nur um ein kleines Programm auszuführen.
Das Ausweichen auf traditionelle externe Dienste von \textit{Cloud-Providern} hat den Nachteil,
dass man einen stündlichen bzw. monatlichen festen Betrag zahlen muss,
auch wenn der Dienst nicht genutzt wird. Man muss im Vorhinein grob die Auslastung abschätzen,
um den Server passend einzustellen. Außerdem muss der Server regelmäßig auf
Sicherheitslücken geprüft und dementsprechend aktualisiert werden.
Effizienter wäre eine serverlose (engl. \textit{serverless}) Anwendung, dass den
Quellcode in einer sicheren Umgebung baut und ausführt.

## Ziele
Das Ziel dieser Arbeit ist es eine serverlose Anwendung für das sichere Ausführen und Testen
von einfachen Java und Gradle Konsolenanwendungen zu entwickeln. Der Quellcode soll über eine
REST-API an den Dienst gesendet werden, wo er anschließend gebaut und ausgeführt oder getestet
wird.

## Erste Gedanken
Der Dienst stellt die view Endpunkte `/run/java` & `run/gradle` sowie `/test/java` & `/test/gradle` zur Verfügung.

Über den ersten Endpunkt `/run/java` kann der Benutzer seine Javadateien kompilieren und ausführen lassen. Durch den zusätzlich gesendeten Parameter `main_file` muss die Java-Klasse angegeben werden, welche die main-Methode enthält. Die Ausgabe des Programms wird dem Benutzer zurückgesendet. Der Benutzer kann dem Dienst über den Endpunkt `/run/gradle` auch eine einzige Zipdatei übergeben. Diese Datei muss das vollständige Javaprojekt enthalten, welches selbst Gradle als Build-Management Tool benutzt. Dann wird der `run`-Task ausgeführt.

**1. Vorraussetzung: Alle Gradle-Projekte müssen das Application-Plugin benutzen**

Über den Endpunkte `/test/java` kann der Benutzer seine Javadateien mittels JUnit testen. Auch hier stehen dem Benutzer die gleichen Möglichkeiten zur Verfügung. Über `/test/gradle` kann eine Zipdatei gesendet werden. Der Dienst führt dann die `test`-Task aus.


## Minimale Anforderungen
Die Minimalen Anforderungen lauten:

- Bereitstellen einer Rest-API
- Einzelne Javadateien mittels Post-Anfrage übergeben, kompilieren und ausführen lassen und die Ausgabe zurück senden.
- Eine Zipdatei übergeben, welches das Javaprojekt mit Gradle als Build-Management Tool enthält. Es können die `run`-Task und die `test`-Task ausgeführt werden.
- System baut auf dem Prinzip des Serverless-Computing auf. Evaluieren ob Serverless für die Anwendung geeignet ist.
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

Deckblatt<br>
Kurzzusammenfassung<br>
Inhaltsverzeichnis<br>
Abbildungsverzeichnis<br>

### 1. Einleitung
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1.1** Motivation<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1.2** Ziel der Arbeit
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1.3** Aufbau der Arbeit

### 2. Grundlagen
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.1** Serverless-Computing<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.1.1** Function as a Service<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.1.2** Serverless Containers<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.1.3** Eigenschaften von Serverless<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.1.4** Nachteile von Serverless<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.1.5** Open Source serverless Platform<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.1.6** Aufbau einer serverless Platform<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.2** Sichere Umgebung für Serverless<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.2.1** Virtual-Machine<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.2.2** Container<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.2.3** Ideale Virtualisierung für Serverless<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.2.4** AWS Firecracker<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2.2.5** Google gVisor<br>

### 3. Entwicklung
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3.1** Dienste und Tolls<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3.2** Architektur<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3.3** Serverless Backend<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3.3.1** Endpunkte<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3.3.2** Ablauf<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3.4** Frontend<br>

### 4. Probleme und Entscheidungen
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.1** JUnit Tests<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.2** Gradle Wrapper<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.3** Google Cloud Run Konfiguration<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.4** Endpunkte entfernt<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **4.5** Zustandslosigkeit<br>

### 5. Evaluation
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **5.1** Google Cloud Run Konfiguration<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **5.2** Probleme der Gradle Endpunkte<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **5.3** Antwortzeiten<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **5.4** Modulaufgaben der Programmierung WS 2018<br>

### 6. Fazit

Literaturverzeichnis<br>
Ehrenwörtliche Erklärung<br>

