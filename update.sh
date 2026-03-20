#!/bin/bash
set -e  # Останавливаем скрипт при ошибке
set -o pipefail  # Учитываем статус выхода из команд в конвейере

DOCKER_COMPOSE_FILE=""

if [[ $1 == "master" ]]; then
   DOCKER_COMPOSE_FILE=docker-compose.prod.yml
elif [[ $1 == "develop" ]]; then
   DOCKER_COMPOSE_FILE=docker-compose.dev.yml
else
   echo "Ошибка. Нет ветки такой"
   exit 1
fi

# Функция для обработки ошибок
error_handler() {
    echo "Произошла ошибка в строке $1."
    exit 1
}

log_time() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Обработчик ошибок
trap 'error_handler $LINENO' ERR

log_time "Проверка обновленного репозитория..."
git fetch --all
git reset --hard origin/$1
log_time "Переключаемся на ветку исполнения..."
git checkout $1

log_time "Останавливаем и удаляем старые контейнеры и образы..."
docker compose -f ${DOCKER_COMPOSE_FILE} down --rmi all

log_time "Запускаем контейнеры в фоне..."
docker compose -f ${DOCKER_COMPOSE_FILE} up -d

log_time "Проверяем состояние контейнеров..."

# Получаем список всех контейнеров
containers=$(docker compose -f ${DOCKER_COMPOSE_FILE} ps --services)

failed=0

sleep 5

for container in $containers; do
    # Проверяем статус контейнера
    status=$(docker inspect --format='{{.State.Status}}' "$container")

    if [ "$status" == "running" ]; then
        log_time "Контейнер $container имеет статут $status. Идет проверка на количество аварийных перезапусков"
    elif [ "$status" == "exited" ]; then
        # Проверяем код завершения контейнера
        exit_code=$(docker inspect --format='{{.State.ExitCode}}' "$container")
        if [ "$exit_code" -eq 0 ]; then
            log_time "Контейнер $container завершился успешно."
        else
            log_time "Контейнер $container завершился с ошибкой. Код выхода: $exit_code. Получаем логи..."
            docker logs "$container"
            failed=1
        fi
    else
        log_time "Контейнер $container не запущен или имеет неизвестный статус: $status."
        docker logs "$container"
        failed=1
    fi


    # Проверяем количество рестартов контейнера
    restarts=$(docker inspect --format='{{.RestartCount}}' "$container")

    if [ "$restarts" -gt 3 ]; then
        log_time "Контейнер $container перезапускался $restarts раз(а). Проверьте возможные проблемы."
	      docker logs "$container"
        failed=1
    fi
done

if [ $failed -ne 0 ]; then
    echo "Один или более контейнеров имеют проблемы (не запущены или часто перезапускаются). См. логи выше."
    exit 1
fi

log_time "Все контейнеры работают корректно!"