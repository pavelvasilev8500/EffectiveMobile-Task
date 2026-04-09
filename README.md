## Тестовое задание от Effective Mobile на позцию DevOps junior

---

## Сборка приложения
В каталоге backend находится простой веб-сервер, написанный на python, а также Dockerfile, для сбрки контейнера.
Основой контейнера выступает образ alpine содержащий python 3.12. Для запуска приложения был создан отдельный пользователь.

Для сборки контейнера нужно выполнить команду:

```bash
docker build -f Dockerfile -t backend .
```

> Если пользователь от которого запускается команда не находится в группе docker, то команду необходимо запускать от sudo.

> Аргумент -f позволяет указать файл сборки образа, а аргумент -t позволяет указать имя выходного образа.

---

## Настройка nginx

В каталоге nginx содержится файл конфигурации сервера. Поскольку а данном этапе домен не известен, то вместо будет использован специальный обработчик который сможет перехватывать все запросы которые не подходят по уже настроенные server_name.

Дополнительно настроено логирование в отдельные файлы.

> Помимо обычной настройки для http в файле app.conf, дополнительно пердставлена настройка для https в файле app-ssl.conf.
> Для работы этого файла конфигурации небходмо сгенерировать ssl сертификат следующими командами
>> ```bash 
>> openssl genrsa -out backendkey.pem 2048
>> openssl req -new -key backendkey.pem -out backend.csr -config backend.cnf
>> openssl x509 -req -in backend.csr -key backendkey.key -out backend.pem -days 31 -sha256 -extfile backend.cnf -extensions v3_ext
>> ```

Для настройки конфигурации необходимо заменить файл default.conf на app.conf в volume nginxconf котейнера nginx по пути:

```bash
/var/lib/docker/volumes/nginxconf/_data/
```

> Для работы https также необходимо поместить ssl сертификат и ключ в volume sslfolder по пути
> ```bash
> /var/lib/docker/volumes/sslfolder/_data/app
> ```

## Запуск проекта

Для запуска проекта в корне содержиться файл docker-compose.yaml
В данном файле описаны контейнеры и их настройки для их коррекной работы.
Для контейнеров указаны версии образов, имена, тома, политика перезагрузки, порты а также сеть. Дополнительно реализована проверка состояния работоспособности контейнеров.
Backend контейнер выделет в отдельную изолированную сеть и взаимодействаут только с proxy контейнером.

> Помомо обычного docker-compose для http также доавлен docker-compose файл и для https. 

Для запуска docker-compose файла необходимо выполнить команду

```bash
docker compose -f docker-compose.yaml up -d
```

Для проверки можно выполнить команду с хоста на котором запущены контейнеры

```bash 
curl -v http://localhost
```

В результате можно увидеть примерно такой ответ:
```bash
* Host localhost:80 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:80...
* Connected to localhost (::1) port 80
> GET / HTTP/1.1
> Host: localhost
> User-Agent: curl/8.5.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Server: nginx/1.29.8
< Date: Thu, 09 Apr 2026 18:51:21 GMT
< Content-Type: text/html; charset=utf-8
< Transfer-Encoding: chunked
< Connection: keep-alive
< 
* Connection #0 to host localhost left intact
Hello from Effective Mobile!
```

Для второго способа проверки можно перейти в барузер по ip адресу и увидеть ответ от сервера
Hello from Effective Mobile!

> Для тестирования https также можно использовать curl, однока при использовании самоподписанного ssl сертификата нужно использовать ключ -k
> ```bash
> curl -vk http://localhost
> ```

## Работа схемы

[Пользователь] -> (интернет/локальная сеть) -> 80/443 -> [сервер с проектом] -> (bridge сеть docker) ->[proxy сервер nginx] -> (изолированная bridge сеть docker) -> [backend server]