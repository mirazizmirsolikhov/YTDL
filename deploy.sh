#!/usr/bin/env bash
# Авто-деплой: тянет origin/main, пересобирает образы и перезапускает стек.
# При сбое сборки или если контейнеры не поднялись — откат на предыдущий коммит.
#
# Вызывается из GitHub Actions по SSH (.github/workflows/deploy.yml),
# но безопасно запускать и руками на VPS: ./deploy.sh
set -euo pipefail

cd "$(dirname "$0")"

BRANCH=main
PREV_COMMIT=$(git rev-parse HEAD)

echo "==> Fetching origin/$BRANCH"
git fetch --quiet origin "$BRANCH"
NEW_COMMIT=$(git rev-parse "origin/$BRANCH")

if [ "$PREV_COMMIT" = "$NEW_COMMIT" ]; then
  echo "==> Уже актуально ($PREV_COMMIT) — деплоить нечего."
  exit 0
fi

echo "==> Деплой $PREV_COMMIT -> $NEW_COMMIT"
git checkout -B "$BRANCH"
git reset --hard "$NEW_COMMIT"

rollback() {
  trap - ERR                       # не зацикливаться, если откат тоже упадёт
  echo "!!! Деплой провалился — откат на $PREV_COMMIT"
  git reset --hard "$PREV_COMMIT"
  docker compose up -d --build
  exit 1
}
trap rollback ERR

echo "==> Сборка образов"
docker compose build

echo "==> Перезапуск сервисов"
docker compose up -d

echo "==> Ждём, пока контейнеры устаканятся"
sleep 10

# Health-check: каждый сервис из compose должен быть в статусе running.
running=$(docker compose ps --status running --services | sort)
defined=$(docker compose config --services | sort)
if [ "$running" = "$defined" ]; then
  echo "==> Деплой OK — все сервисы подняты на $NEW_COMMIT"
else
  echo "!!! Не все сервисы работают:"
  docker compose ps
  rollback
fi

trap - ERR
