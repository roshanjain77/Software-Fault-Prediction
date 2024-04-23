# install java 17

```
sudo apt install openjdk-17-jdk
```

# download jdt_ls release from github

```
https://github.com/eclipse-jdtls/eclipse.jdt.ls/tags
```

Some releases are not working, so you may need to try different versions.

# extract the downloaded file

```
tar -xvf /path/to/downloaded/file.tar.gz
```

cd into the extracted folder
run

```
./mvnw clean verify -DskipTests
```

jar file will be stored in
org.eclipse.jdt.ls.product/target/repository
