# Develop

## Lib

Docling

## Setup

Right click   `FastRag` -> Mark directory as -> Sources root


### Скачать репозиторий с помощью UV

### Скачать зависимости

```shell
uv install
```


### Запустить и установить pre-commit

#### Configure pre-commit

```shell
pre-commit autoupdate
pre-commit install
```

```shell
pre-commit run
```


## Запуск

## Особенности

Библиотеки распознавания самостоятельно выбирают железо для запуска

## Ошибки

#### Ошибка скачивания модели

```text
Failed to download https://www.modelscope.cn/models/RapidAI/RapidOCR/resolve/v3.4.0/torch/PP-OCRv4/det/ch_PP-OCRv4_det_infer.pth
requests.exceptions.ConnectionError: NameResolutionError: Failed to resolve 'cdn-lfs-cn-1.modelscope.cn'

```

Используйте VPN / отключите модель / используйте локальную версию
#TODO: Доделай раздел
