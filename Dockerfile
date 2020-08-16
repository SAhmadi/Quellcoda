FROM tiangolo/meinheld-gunicorn:python3.7-alpine3.8

ENV APP_HOME /app
WORKDIR $APP_HOME

# Get wget
RUN apk --no-cache add wget unzip

# Get Azul's OpenJDK (see https://docs.azul.com/zulu/zuludocs/ZuluUserGuide/InstallingZulu/InstallOnLinuxUsingAPKRepository.htm)
# Attach APK Repo
RUN wget https://cdn.azul.com/public_keys/alpine-signing@azul.com-5d5dc44c.rsa.pub
RUN cp alpine-signing@azul.com-5d5dc44c.rsa.pub /etc/apk/keys/
RUN echo "https://repos.azul.com/zulu/alpine" >> /etc/apk/repositories

# Install Zulu11
RUN apk --no-cache add zulu11-jdk-headless
ENV JAVA_HOME=/usr/lib/jvm/default-jvm
ENV PATH="$JAVA_HOME/bin:${PATH}"
RUN which javac
RUN which java

# Get Junit standalone jar
RUN wget https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.6.2/junit-platform-console-standalone-1.6.2.jar

# Get Gradle distribution zip
RUN wget https://downloads.gradle-dn.com/distributions/gradle-6.3-bin.zip
RUN unzip gradle-6.3-bin.zip

# Cleaning up not needed files
RUN rm -rf gradle-6.3-bin.zip
RUN rm gradle-6.3/LICENSE
RUN rm gradle-6.3/NOTICE
RUN rm gradle-6.3/README
RUN rm gradle-6.3/init.d/readme.txt

# Get Flask and deps
RUN pip install --upgrade pip
#RUN pip install Flask
#RUN pip install gunicorn
#RUN pip install flask_cors
COPY requirements.txt $APP_HOME
RUN pip install -r $APP_HOME/requirements.txt

COPY . $APP_HOME

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "--workers 2", "--threads 8", "--timeout 0"]
