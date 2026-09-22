# Развёртывание StreamForge в WSL2

Проект нужно клонировать в Linux-файловую систему WSL2, например в
`~/projects/streamforge`. Не размещай рабочую копию в `/mnt/c`: операции с
большим количеством небольших файлов, Docker bind mounts и права доступа там
работают хуже.

## Что установить на Windows

1. WSL2 с Ubuntu.
2. Docker Desktop с включённой WSL integration для установленной Ubuntu.
3. Git внутри Ubuntu.

Python, виртуальное окружение, `.env` и Docker volumes с Mac не переносятся.
Они создаются заново в WSL2.

## Клонирование

В терминале Ubuntu:

```bash
git config --global core.autocrlf input
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/AlwaysAfraidYolo/streamforge.git
cd streamforge
```

Если репозиторий требует авторизацию, сначала настрой доступ к GitHub внутри
WSL2. Не копируй macOS credentials или `.env` вручную.

## Первый запуск data-platform каркаса

Убедись, что Docker Desktop запущен и Ubuntu разрешена в настройках WSL
integration, затем:

```bash
make up
make test
make smoke
```

`make up` вызывает bootstrap и создаёт новый локальный `.env` с секретами.
Файл исключён из Git.

Дополнительный analytics-профиль:

```bash
make analytics
```

## Проверка переноса

```bash
git status --short
docker compose ps
curl --fail http://127.0.0.1:18000/ready
```

Ожидается чистый `git status`, запущенные контейнеры и HTTP 200 от `/ready`.

## C++ Core

C++-часть будет собираться непосредственно внутри Ubuntu. Не переносим macOS
build-каталоги и бинарники: CMake должен создать их заново для Linux.

После появления C++ workspace базовые команды будут такими:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
ctest --test-dir build --output-on-failure
```
