FROM tiangolo/meinheld-gunicorn:python3.7-alpine3.8

ENV APP_HOME /app
WORKDIR $APP_HOME

# Get wget
RUN apk --no-cache add wget

# Get Azul's OpenJDK (see https://docs.azul.com/zulu/zuludocs/ZuluUserGuide/InstallingZulu/InstallOnLinuxUsingAPKRepository.htm)
# Attach APK Repo
RUN wget https://cdn.azul.com/public_keys/alpine-signing@azul.com-5d5dc44c.rsa.pub
RUN cp alpine-signing@azul.com-5d5dc44c.rsa.pub /etc/apk/keys/
RUN echo "https://repos.azul.com/zulu/alpine" >> /etc/apk/repositories

# Install Zulu11
RUN apk --no-cache add zulu11-jdk-headless
ENV JAVA_HOME=/usr/lib/jvm/default-jvm
ENV PATH="$JAVA_HOME/bin:${PATH}"
RUN javac -version

# Get Junit standalone jar
RUN wget https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.6.0/junit-platform-console-standalone-1.6.0.jar

# Get Flask and deps
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN virtualenv venv
RUN source venv/bin/activate
RUN pip install Flask
RUN pip install gunicorn

COPY . $APP_HOME

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app", "--timeout 300"]