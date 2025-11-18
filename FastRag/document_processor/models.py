"""Унифицированные модели данных для представления документов."""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel, Field, field_validator

# TODO: Добавь сюда нормальную документацию


class ContentType(str, Enum):
    """Типы контента в документе."""

    TEXT = "text"
    TABLE = "table"
    IMAGE = "image"
    CODE = "code"
    FORMULA = "formula"
    list = "list"
    HEADING = "heading"
    LINK = "link"
    METADATA = "metadata"


class DocumentFormat(str, Enum):
    """Поддерживаемые форматы документов."""

    # Документы
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    ODT = "odt"
    RTF = "rtf"
    TXT = "txt"

    # Презентации
    PPTX = "pptx"
    PPT = "ppt"
    ODP = "odp"

    # Таблицы
    XLSX = "xlsx"
    XLS = "xls"
    CSV = "csv"
    ODS = "ods"

    # Разметка
    HTML = "html"
    XML = "xml"
    MARKDOWN = "markdown"
    RST = "rst"
    ASCIIDOC = "asciidoc"

    # Код
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    TYPESCRIPT = "typescript"

    # Изображения
    PNG = "png"
    JPEG = "jpeg"
    GIF = "gif"
    WEBP = "webp"
    SVG = "svg"
    TIFF = "tiff"

    # Видео
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    WEBM = "webm"

    # Аудио
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    FLAC = "flac"

    # Архивы
    ZIP = "zip"
    TAR = "tar"
    GZIP = "gzip"
    BZIP2 = "bzip2"
    RAR = "rar"
    SEVEN_ZIP = "7z"

    # Email
    MSG = "msg"
    EML = "eml"
    MBOX = "mbox"

    # Данные
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    PARQUET = "parquet"
    AVRO = "avro"

    # Геопространственные
    GEOJSON = "geojson"
    KML = "kml"
    SHAPEFILE = "shapefile"
    GPKG = "gpkg"

    # Научные
    HDF5 = "hdf5"
    NETCDF = "netcdf"

    UNKNOWN = "unknown"


class BoundingBox(BaseModel):
    """Координаты элемента на странице/изображении."""

    x: float = Field(..., description="X координата (левый верхний угол)")
    y: float = Field(..., description="Y координата (левый верхний угол)")
    width: float = Field(..., description="Ширина")
    height: float = Field(..., description="Высота")
    page: int | None = Field(None, description="Номер страницы")


class TextBlock(BaseModel):
    """Блок текста с метаданными."""

    content: str = Field(..., description="Текстовое содержимое")
    type: ContentType = Field(ContentType.TEXT, description="Тип контента")
    bbox: BoundingBox | None = None
    style: dict[str, Any] = Field(
        default_factory=dict,
        description="Стили (шрифт, размер и т.д.)",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class TableCell(BaseModel):
    """Ячейка таблицы."""

    content: str
    row: int
    col: int
    rowspan: int = 1
    colspan: int = 1


class Table(BaseModel):
    """Таблица с данными."""

    id: UUID = Field(default_factory=uuid4)
    cells: list[TableCell]
    headers: list[str] | None = None
    rows: int
    cols: int
    bbox: BoundingBox | None = None
    caption: str | None = None


class ImageData(BaseModel):
    """Изображение с метаданными."""

    id: UUID = Field(default_factory=uuid4)
    path: Path | None = None
    data: bytes | None = None
    format: str
    width: int
    height: int
    bbox: BoundingBox | None = None
    caption: str | None = None
    ocr_text: str | None = None


class CodeBlock(BaseModel):
    """Блок исходного кода."""

    id: UUID = Field(default_factory=uuid4)
    content: str
    language: str
    line_start: int | None = None
    line_end: int | None = None
    ast: dict[str, Any] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentMetadata(BaseModel):
    """Метаданные документа."""

    title: str | None = None
    author: str | None = None
    created: datetime | None = None
    modified: datetime | None = None
    language: str | None = None
    page_count: int | None = None
    word_count: int | None = None
    file_size: int | None = None
    mime_type: str | None = None
    encoding: str | None = None
    keywords: list[str] = Field(default_factory=list)
    custom: dict[str, Any] = Field(default_factory=dict)


class DocumentNode(BaseModel):
    """Узел документа в иерархической структуре."""

    id: UUID = Field(default_factory=uuid4)
    type: ContentType
    content: TextBlock | Table | ImageData | CodeBlock | str
    children: list["DocumentNode"] = Field(default_factory=list)
    parent_id: UUID | None = None
    level: int = 0  # Уровень вложенности
    order: int = 0  # Порядок в документе


class UnifiedDocument(BaseModel):
    """
    Унифицированное представление документа.

    Это центральная модель данных для всех типов документов.
    Все парсеры преобразуют входные файлы в этот формат.
    """

    id: UUID = Field(default_factory=uuid4)
    source_path: Path | None = None
    format: DocumentFormat
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)

    # Структурированное содержимое
    nodes: list[DocumentNode] = Field(default_factory=list)

    # Быстрый доступ к элементам
    text_blocks: list[TextBlock] = Field(default_factory=list)
    tables: list[Table] = Field(default_factory=list)
    images: list[ImageData] = Field(default_factory=list)
    code_blocks: list[CodeBlock] = Field(default_factory=list)

    # Временные метки
    parsed_at: datetime = Field(default_factory=datetime.now)
    processing_time: float | None = None  # в секундах

    # Дополнительные данные
    raw_content: str | None = None  # Исходное содержимое
    extra: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    @field_validator("source_path")
    def validate_path(cls, value: Path | None) -> Path | None:
        """Валидация пути к файлу."""
        if value is not None and not isinstance(value, Path):
            return Path(value)
        return value

    # TODO: НЕ РАБОТАЕТ
    def to_markdown(self) -> str:
        """Экспорт в Markdown формат."""
        lines = []

        if self.metadata.title:
            lines.append(f"# {self.metadata.title}\n")

        for node in self.nodes:
            lines.extend(self._node_to_markdown(node))

        return "\n\n".join(lines)

    def _node_to_markdown(self, node: DocumentNode) -> str:
        """Конвертация узла в Markdown."""
        if node.type == ContentType.TEXT and isinstance(node.content, TextBlock):
            return node.content.content
        if node.type == ContentType.HEADING and isinstance(node.content, str):
            return f"{'#' * (node.level + 1)} {node.content}"
        if node.type == ContentType.CODE and isinstance(node.content, CodeBlock):
            return f"```{node.content.language}\n{node.content.content}\n```"
        if node.type == ContentType.TABLE and isinstance(node.content, Table):
            return self._table_to_markdown(node.content)
        return str(node.content)

    @classmethod
    def _table_to_markdown(cls, table: Table) -> str:
        """Конвертация таблицы в Markdown."""
        if not table.cells:
            return ""

        # Группировка ячеек по строкам
        rows: dict[int, list[TableCell]] = {}
        for cell in table.cells:
            if cell.row not in rows:
                rows[cell.row] = []
            rows[cell.row].append(cell)

        # Сортировка и форматирование
        lines = []
        for row_num in sorted(rows.keys()):
            cells = sorted(rows[row_num], key=lambda c: c.col)
            line = "| " + " | ".join(c.content for c in cells) + " |"
            lines.append(line)

            # Разделитель после заголовка
            if row_num == 0 and table.headers:
                lines.append("| " + " | ".join("---" for _ in cells) + " |")

        return "\n".join(lines)

    def to_json(self) -> str:
        """Экспорт в JSON."""

        return orjson.dumps(
            self.model_dump(mode="json"),
            option=orjson.OPT_INDENT_2,
        ).decode()

    def get_all_text(self) -> str:
        """Получить весь текст из документа."""
        texts = []

        for block in self.text_blocks:
            texts.extend(block.content)

        for table in self.tables:
            for cell in table.cells:
                texts.extend(cell.content)

        for code in self.code_blocks:
            texts.extend(code.content)

        return "\n\n".join(texts)


class ParsingResult(BaseModel):
    """Результат парсинга документа."""

    success: bool
    document: UnifiedDocument | None = None
    error: str | None = None
    warnings: list[str] = Field(default_factory=list)


MIME_TO_FORMAT = {
    # Документы
    "application/pdf": DocumentFormat.PDF,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocumentFormat.DOCX,
    "application/msword": DocumentFormat.DOC,
    "application/vnd.oasis.opendocument.text": DocumentFormat.ODT,
    "application/rtf": DocumentFormat.RTF,
    "text/plain": DocumentFormat.TXT,
    # Презентации
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": DocumentFormat.PPTX,
    "application/vnd.ms-powerpoint": DocumentFormat.PPT,
    "application/vnd.oasis.opendocument.presentation": DocumentFormat.ODP,
    # Таблицы
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": DocumentFormat.XLSX,
    "application/vnd.ms-excel": DocumentFormat.XLS,
    "text/csv": DocumentFormat.CSV,
    "application/vnd.oasis.opendocument.spreadsheet": DocumentFormat.ODS,
    # HTML/XML
    "text/html": DocumentFormat.HTML,
    "application/xhtml+xml": DocumentFormat.HTML,
    "text/xml": DocumentFormat.XML,
    "application/xml": DocumentFormat.XML,
    # Изображения
    "image/png": DocumentFormat.PNG,
    "image/jpeg": DocumentFormat.JPEG,
    "image/gif": DocumentFormat.GIF,
    "image/webp": DocumentFormat.WEBP,
    "image/svg+xml": DocumentFormat.SVG,
    "image/tiff": DocumentFormat.TIFF,
    # Видео
    "video/mp4": DocumentFormat.MP4,
    "video/x-msvideo": DocumentFormat.AVI,
    "video/x-matroska": DocumentFormat.MKV,
    "video/webm": DocumentFormat.WEBM,
    # Аудио
    "audio/mpeg": DocumentFormat.MP3,
    "audio/wav": DocumentFormat.WAV,
    "audio/ogg": DocumentFormat.OGG,
    "audio/flac": DocumentFormat.FLAC,
    # Архивы
    "application/zip": DocumentFormat.ZIP,
    "application/x-tar": DocumentFormat.TAR,
    "application/gzip": DocumentFormat.GZIP,
    "application/x-bzip2": DocumentFormat.BZIP2,
    "application/x-rar": DocumentFormat.RAR,
    "application/x-7z-compressed": DocumentFormat.SEVEN_ZIP,
    # Email
    "application/vnd.ms-outlook": DocumentFormat.MSG,
    "message/rfc822": DocumentFormat.EML,
    "application/mbox": DocumentFormat.MBOX,
    # Данные
    "application/json": DocumentFormat.JSON,
    "application/x-yaml": DocumentFormat.YAML,
    "application/toml": DocumentFormat.TOML,
    # Геопространственные
    "application/geo+json": DocumentFormat.GEOJSON,
    "application/vnd.google-earth.kml+xml": DocumentFormat.KML,
}
EXTENSION_TO_FORMAT = {
    # Документы
    ".pdf": DocumentFormat.PDF,
    ".docx": DocumentFormat.DOCX,
    ".doc": DocumentFormat.DOC,
    ".odt": DocumentFormat.ODT,
    ".rtf": DocumentFormat.RTF,
    ".txt": DocumentFormat.TXT,
    # Презентации
    ".pptx": DocumentFormat.PPTX,
    ".ppt": DocumentFormat.PPT,
    ".odp": DocumentFormat.ODP,
    # Таблицы
    ".xlsx": DocumentFormat.XLSX,
    ".xls": DocumentFormat.XLS,
    ".csv": DocumentFormat.CSV,
    ".ods": DocumentFormat.ODS,
    # Разметка
    ".html": DocumentFormat.HTML,
    ".htm": DocumentFormat.HTML,
    ".xml": DocumentFormat.XML,
    ".md": DocumentFormat.MARKDOWN,
    ".markdown": DocumentFormat.MARKDOWN,
    ".rst": DocumentFormat.RST,
    ".adoc": DocumentFormat.ASCIIDOC,
    # Код
    ".py": DocumentFormat.PYTHON,
    ".js": DocumentFormat.JAVASCRIPT,
    ".ts": DocumentFormat.TYPESCRIPT,
    ".java": DocumentFormat.JAVA,
    ".cpp": DocumentFormat.CPP,
    ".cc": DocumentFormat.CPP,
    ".c": DocumentFormat.C,
    ".cs": DocumentFormat.CSHARP,
    ".go": DocumentFormat.GO,
    ".rs": DocumentFormat.RUST,
    # Изображения
    ".png": DocumentFormat.PNG,
    ".jpg": DocumentFormat.JPEG,
    ".jpeg": DocumentFormat.JPEG,
    ".gif": DocumentFormat.GIF,
    ".webp": DocumentFormat.WEBP,
    ".svg": DocumentFormat.SVG,
    ".tif": DocumentFormat.TIFF,
    ".tiff": DocumentFormat.TIFF,
    # Видео
    ".mp4": DocumentFormat.MP4,
    ".avi": DocumentFormat.AVI,
    ".mkv": DocumentFormat.MKV,
    ".webm": DocumentFormat.WEBM,
    # Аудио
    ".mp3": DocumentFormat.MP3,
    ".wav": DocumentFormat.WAV,
    ".ogg": DocumentFormat.OGG,
    ".flac": DocumentFormat.FLAC,
    # Архивы
    ".zip": DocumentFormat.ZIP,
    ".tar": DocumentFormat.TAR,
    ".gz": DocumentFormat.GZIP,
    ".bz2": DocumentFormat.BZIP2,
    ".rar": DocumentFormat.RAR,
    ".7z": DocumentFormat.SEVEN_ZIP,
    # Email
    ".msg": DocumentFormat.MSG,
    ".eml": DocumentFormat.EML,
    ".mbox": DocumentFormat.MBOX,
    # Данные
    ".json": DocumentFormat.JSON,
    ".yaml": DocumentFormat.YAML,
    ".yml": DocumentFormat.YAML,
    ".toml": DocumentFormat.TOML,
    ".parquet": DocumentFormat.PARQUET,
    ".avro": DocumentFormat.AVRO,
    # Геопространственные
    ".geojson": DocumentFormat.GEOJSON,
    ".kml": DocumentFormat.KML,
    ".shp": DocumentFormat.SHAPEFILE,
    ".gpkg": DocumentFormat.GPKG,
    # Научные
    ".h5": DocumentFormat.HDF5,
    ".hdf5": DocumentFormat.HDF5,
    ".nc": DocumentFormat.NETCDF,
}
