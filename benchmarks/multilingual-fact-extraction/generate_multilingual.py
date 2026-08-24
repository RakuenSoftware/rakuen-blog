#!/usr/bin/env python3
"""Generate multilingual fact-extraction rows from pinned open-source trees."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


LANGUAGES = ("fr", "de", "es", "zh", "it", "ru", "pl", "pt", "ja", "vi", "nl", "ar", "tr", "hi")
KEEP_SUFFIXES = {
    ".cfg", ".css", ".html", ".ini", ".js", ".json", ".md", ".mjs",
    ".po", ".py", ".rst", ".scss", ".ts", ".tsx", ".txt", ".vue",
    ".yaml", ".yml",
}
SKIP_PARTS = {".git", ".github", "node_modules", "public", "static", "vendor"}


TEMPLATES = {
    "fr": {
        "location": ["Dans {project}, {file} se trouve dans {directory}.", "Le fichier {file} de {project} est rangé dans {directory}."],
        "part": ["{file} fait partie du projet {project}.", "Le projet {project} comprend le fichier {file}."],
        "transient": ["Il est proposé de placer {file} dans {directory} lors d’une prochaine version de {project}.", "L’équipe envisage de déplacer {file} vers {directory} dans {project}."],
        "negation": ["Dans {project}, {file} ne se trouve pas dans {wrong_directory}.", "{file} n’est pas rangé sous {wrong_directory} dans {project}."],
        "ambiguous": ["Quelqu’un a mentionné {file} et {directory} à propos de {project}, sans préciser leur lien.", "La discussion sur {project} cite {file} et {directory}, mais le rapport entre eux reste flou."],
    },
    "de": {
        "location": ["In {project} liegt {file} im Verzeichnis {directory}.", "Die Datei {file} von {project} befindet sich unter {directory}."],
        "part": ["{file} gehört zum Projekt {project}.", "Das Projekt {project} enthält die Datei {file}."],
        "transient": ["Es gibt den Vorschlag, {file} in einer künftigen Version von {project} nach {directory} zu legen.", "Das Team erwägt, {file} in {project} nach {directory} zu verschieben."],
        "negation": ["In {project} liegt {file} nicht unter {wrong_directory}.", "{file} befindet sich in {project} nicht im Verzeichnis {wrong_directory}."],
        "ambiguous": ["Jemand erwähnte {file} und {directory} im Zusammenhang mit {project}, erklärte aber keine Verbindung.", "In der Diskussion über {project} fielen {file} und {directory}, ihr Zusammenhang blieb jedoch unklar."],
    },
    "es": {
        "location": ["En {project}, {file} se encuentra en el directorio {directory}.", "El archivo {file} de {project} está guardado en {directory}."],
        "part": ["{file} forma parte del proyecto {project}.", "El proyecto {project} incluye el archivo {file}."],
        "transient": ["Se propone colocar {file} en {directory} en una futura versión de {project}.", "El equipo está considerando mover {file} a {directory} dentro de {project}."],
        "negation": ["En {project}, {file} no se encuentra en {wrong_directory}.", "{file} no está guardado bajo {wrong_directory} en {project}."],
        "ambiguous": ["Alguien mencionó {file} y {directory} al hablar de {project}, pero no explicó su relación.", "La conversación sobre {project} cita {file} y {directory}, aunque no queda claro cómo se relacionan."],
    },
    "zh": {
        "location": ["在 {project} 中，{file} 位于 {directory} 目录。", "{project} 项目的 {file} 文件存放在 {directory}。"],
        "part": ["{file} 属于 {project} 项目。", "{project} 项目包含 {file} 文件。"],
        "transient": ["有人提议在 {project} 的未来版本中把 {file} 放到 {directory}。", "团队正在考虑把 {project} 中的 {file} 移到 {directory}。"],
        "negation": ["在 {project} 中，{file} 不位于 {wrong_directory}。", "{project} 的 {file} 文件并未存放在 {wrong_directory}。"],
        "ambiguous": ["有人在讨论 {project} 时提到了 {file} 和 {directory}，但没有说明二者的关系。", "关于 {project} 的讨论同时提到 {file} 与 {directory}，它们之间的联系并不明确。"],
    },
    "it": {
        "location": ["In {project}, {file} si trova nella directory {directory}.", "Il file {file} di {project} è conservato in {directory}."],
        "part": ["{file} fa parte del progetto {project}.", "Il progetto {project} include il file {file}."],
        "transient": ["È stato proposto di collocare {file} in {directory} in una futura versione di {project}.", "Il gruppo sta valutando di spostare {file} in {directory} all’interno di {project}."],
        "negation": ["In {project}, {file} non si trova in {wrong_directory}.", "{file} non è conservato sotto {wrong_directory} in {project}."],
        "ambiguous": ["Qualcuno ha menzionato {file} e {directory} parlando di {project}, senza chiarire il loro rapporto.", "La discussione su {project} cita {file} e {directory}, ma il collegamento resta poco chiaro."],
    },
    "ru": {
        "location": ["В проекте {project} файл {file} находится в каталоге {directory}.", "Файл {file} из {project} хранится в {directory}."],
        "part": ["Файл {file} является частью проекта {project}.", "Проект {project} включает файл {file}."],
        "transient": ["Предлагается поместить {file} в {directory} в будущей версии {project}.", "Команда рассматривает перенос {file} в {directory} внутри {project}."],
        "negation": ["В проекте {project} файл {file} не находится в {wrong_directory}.", "Файл {file} в {project} не хранится в каталоге {wrong_directory}."],
        "ambiguous": ["При обсуждении {project} кто-то упомянул {file} и {directory}, но не объяснил их связь.", "В разговоре о {project} названы {file} и {directory}, однако связь между ними неясна."],
    },
    "pl": {
        "location": ["W projekcie {project} plik {file} znajduje się w katalogu {directory}.", "Plik {file} z projektu {project} jest przechowywany w {directory}."],
        "part": ["Plik {file} jest częścią projektu {project}.", "Projekt {project} zawiera plik {file}."],
        "transient": ["Zaproponowano umieszczenie {file} w {directory} w przyszłej wersji {project}.", "Zespół rozważa przeniesienie {file} do {directory} w projekcie {project}."],
        "negation": ["W projekcie {project} plik {file} nie znajduje się w {wrong_directory}.", "Plik {file} nie jest przechowywany pod {wrong_directory} w projekcie {project}."],
        "ambiguous": ["Ktoś wspomniał o {file} i {directory} podczas rozmowy o {project}, ale nie wyjaśnił ich związku.", "Dyskusja o {project} wymienia {file} oraz {directory}, lecz ich powiązanie pozostaje niejasne."],
    },
    "pt": {
        "location": ["No projeto {project}, {file} fica no diretório {directory}.", "O ficheiro {file} de {project} está guardado em {directory}."],
        "part": ["{file} faz parte do projeto {project}.", "O projeto {project} inclui o ficheiro {file}."],
        "transient": ["Foi proposto colocar {file} em {directory} numa futura versão de {project}.", "A equipa está a considerar mover {file} para {directory} dentro de {project}."],
        "negation": ["No projeto {project}, {file} não se encontra em {wrong_directory}.", "{file} não está guardado sob {wrong_directory} em {project}."],
        "ambiguous": ["Alguém mencionou {file} e {directory} ao falar de {project}, mas não explicou a relação.", "A conversa sobre {project} cita {file} e {directory}, embora a ligação entre ambos não seja clara."],
    },
    "ja": {
        "location": ["{project} では、{file} は {directory} ディレクトリにあります。", "{project} の {file} ファイルは {directory} に保存されています。"],
        "part": ["{file} は {project} プロジェクトの一部です。", "{project} プロジェクトには {file} ファイルが含まれています。"],
        "transient": ["{project} の将来の版で {file} を {directory} に置く案が出ています。", "チームは {project} の {file} を {directory} へ移すことを検討しています。"],
        "negation": ["{project} では、{file} は {wrong_directory} にありません。", "{project} の {file} ファイルは {wrong_directory} には保存されていません。"],
        "ambiguous": ["{project} の話で {file} と {directory} が言及されましたが、両者の関係は説明されませんでした。", "{project} に関する議論では {file} と {directory} が挙がりましたが、そのつながりは不明です。"],
    },
    "vi": {
        "location": ["Trong dự án {project}, tệp {file} nằm trong thư mục {directory}.", "Tệp {file} của {project} được lưu tại {directory}."],
        "part": ["Tệp {file} là một phần của dự án {project}.", "Dự án {project} bao gồm tệp {file}."],
        "transient": ["Có đề xuất đặt {file} vào {directory} trong một phiên bản tương lai của {project}.", "Nhóm đang cân nhắc chuyển {file} sang {directory} trong {project}."],
        "negation": ["Trong {project}, tệp {file} không nằm ở {wrong_directory}.", "Tệp {file} không được lưu dưới {wrong_directory} trong {project}."],
        "ambiguous": ["Có người nhắc đến {file} và {directory} khi bàn về {project}, nhưng không giải thích mối liên hệ.", "Cuộc thảo luận về {project} đề cập {file} và {directory}, tuy nhiên quan hệ giữa chúng không rõ ràng."],
    },
    "nl": {
        "location": ["In {project} staat {file} in de map {directory}.", "Het bestand {file} van {project} is opgeslagen in {directory}."],
        "part": ["{file} maakt deel uit van het project {project}.", "Het project {project} bevat het bestand {file}."],
        "transient": ["Er is voorgesteld om {file} in een toekomstige versie van {project} in {directory} te plaatsen.", "Het team overweegt om {file} binnen {project} naar {directory} te verplaatsen."],
        "negation": ["In {project} staat {file} niet in {wrong_directory}.", "Het bestand {file} is in {project} niet onder {wrong_directory} opgeslagen."],
        "ambiguous": ["Iemand noemde {file} en {directory} tijdens een gesprek over {project}, maar legde hun verband niet uit.", "De discussie over {project} vermeldt {file} en {directory}, hoewel de relatie ertussen onduidelijk blijft."],
    },
    "ar": {
        "location": ["في مشروع {project}، يوجد الملف {file} داخل المجلد {directory}.", "يُحفظ ملف {file} الخاص بمشروع {project} في {directory}."],
        "part": ["الملف {file} جزء من مشروع {project}.", "يتضمن مشروع {project} الملف {file}."],
        "transient": ["هناك اقتراح لوضع {file} في {directory} في إصدار مستقبلي من {project}.", "يفكر الفريق في نقل {file} إلى {directory} داخل {project}."],
        "negation": ["في مشروع {project}، لا يوجد الملف {file} في {wrong_directory}.", "ملف {file} في {project} غير محفوظ تحت {wrong_directory}."],
        "ambiguous": ["ذكر أحدهم {file} و{directory} أثناء الحديث عن {project}، لكنه لم يوضح العلاقة بينهما.", "تذكر المناقشة حول {project} كلاً من {file} و{directory}، لكن الصلة بينهما غير واضحة."],
    },
    "tr": {
        "location": ["{project} projesinde {file}, {directory} dizininde bulunur.", "{project} içindeki {file} dosyası {directory} altında saklanır."],
        "part": ["{file}, {project} projesinin bir parçasıdır.", "{project} projesi {file} dosyasını içerir."],
        "transient": ["{project} projesinin gelecekteki bir sürümünde {file} dosyasının {directory} içine konması önerildi.", "Ekip, {project} içindeki {file} dosyasını {directory} konumuna taşımayı düşünüyor."],
        "negation": ["{project} projesinde {file}, {wrong_directory} altında değildir.", "{file} dosyası {project} içinde {wrong_directory} dizininde saklanmaz."],
        "ambiguous": ["Biri {project} hakkında konuşurken {file} ve {directory} adlarını andı, ancak aralarındaki ilişkiyi açıklamadı.", "{project} tartışmasında {file} ile {directory} geçiyor, fakat bağlantıları belirsiz kalıyor."],
    },
    "hi": {
        "location": ["{project} परियोजना में {file}, {directory} निर्देशिका में है।", "{project} की {file} फ़ाइल {directory} में रखी गई है।"],
        "part": ["{file}, {project} परियोजना का हिस्सा है।", "{project} परियोजना में {file} फ़ाइल शामिल है।"],
        "transient": ["{project} के आगामी संस्करण में {file} को {directory} में रखने का प्रस्ताव है।", "टीम {project} में {file} को {directory} पर ले जाने पर विचार कर रही है।"],
        "negation": ["{project} परियोजना में {file}, {wrong_directory} में नहीं है।", "{project} की {file} फ़ाइल {wrong_directory} के अंतर्गत नहीं रखी गई है।"],
        "ambiguous": ["{project} की चर्चा में किसी ने {file} और {directory} का उल्लेख किया, लेकिन उनका संबंध नहीं बताया।", "{project} से जुड़ी बातचीत में {file} और {directory} आए, पर उनके बीच का संबंध अस्पष्ट रहा।"],
    },
}


def git_paths(checkout: Path, commit: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(checkout), "ls-tree", "-r", "--name-only", commit],
            check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise ValueError(f"cannot read pinned commit {commit} in {checkout}: {exc.stderr}") from exc
    paths = []
    for value in result.stdout.splitlines():
        path = Path(value)
        if "/" not in value or path.suffix.lower() not in KEEP_SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        paths.append(value)
    if len(paths) < 100:
        raise ValueError(f"only {len(paths)} usable paths in {checkout} at {commit}")
    return sorted(paths)


def pick_distinct(paths: list[str], index: int, count: int) -> list[str]:
    chosen = []
    cursor = index * 17 + index // max(1, len(paths))
    while len(chosen) < count:
        candidate = paths[cursor % len(paths)]
        triple = (Path(candidate).name, str(Path(candidate).parent))
        if all((Path(old).name, str(Path(old).parent)) != triple for old in chosen):
            chosen.append(candidate)
        cursor += 137
    return chosen


def render(template: str, project: str, path: str, wrong_directory: str = "") -> str:
    item = Path(path)
    return template.format(
        project=project,
        file=item.name,
        directory=str(item.parent),
        wrong_directory=wrong_directory,
    )


def row_for(
    index: int,
    language: str,
    blueprint: dict[str, Any],
    project: dict[str, Any],
    paths: list[str],
    attempt: int = 0,
) -> dict[str, Any]:
    project_name = project["repository"]
    blueprint_category = blueprint["category"]
    category = (
        blueprint_category
        if blueprint_category
        in {"multi_fact", "transient", "negation", "ambiguous", "novel_pred"}
        else "third_person"
    )
    template_group = TEMPLATES[language]
    source_paths: list[str]
    gold: list[dict[str, str]]

    if category == "multi_fact":
        fact_count = max(2, min(3, len(blueprint["gold"])))
        source_paths = pick_distinct(paths, index + attempt * 997, fact_count)
        sentences = []
        gold = []
        for offset, path in enumerate(source_paths):
            variant = template_group["location"][(index + offset) % 2]
            sentences.append(render(variant, project_name, path))
            item = Path(path)
            gold.append({"subject": item.name, "relation": "located_in", "object": str(item.parent)})
        note = " ".join(sentences)
        template_name = "multi_fact"
    elif category in {"transient", "negation", "ambiguous"}:
        source_paths = pick_distinct(paths, index + attempt * 997, 1)
        path = source_paths[0]
        wrong = ""
        if category == "negation":
            actual = Path(path)
            path_set = set(paths)
            wrong = str(Path("retired") / actual.parent)
            while str(Path(wrong) / actual.name) in path_set:
                wrong = str(Path("retired") / wrong)
        variant = template_group[category][index % 2]
        note = render(variant, project_name, path, wrong)
        gold = []
        template_name = category
    elif category == "novel_pred":
        source_paths = pick_distinct(paths, index + attempt * 997, 1)
        path = source_paths[0]
        variant = template_group["part"][index % 2]
        note = render(variant, project_name, path)
        gold = [{"subject": Path(path).name, "relation": "part_of", "object": project_name}]
        template_name = "part"
    else:
        source_paths = pick_distinct(paths, index + attempt * 997, 1)
        path = source_paths[0]
        variant = template_group["location"][index % 2]
        note = render(variant, project_name, path)
        item = Path(path)
        gold = [{"subject": item.name, "relation": "located_in", "object": str(item.parent)}]
        template_name = "location"

    tier = 1 if index < 999 else 2 if index < 1998 else 3
    return {
        "domain": "code",
        "category": category,
        "note": note,
        "gold": gold,
        "template": f"oss.{language}.{template_name}.{index % 2}",
        "source": {
            "repo": project["repository"],
            "url": project["url"],
            "sha": project["commit"],
            "paths": source_paths,
        },
        "tier": tier,
        "stratum": f"ML{index % 10 + 1}",
        "provenance": "generated-from-open-source",
        "language": language,
        "id": f"ml{index + 1:06d}",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--projects", type=Path, default=Path(__file__).with_name("source-projects.json"))
    parser.add_argument("--blueprint", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    config = json.loads(args.projects.read_text(encoding="utf-8"))
    projects = config["projects"]
    blueprint = [json.loads(line) for line in args.blueprint.read_text(encoding="utf-8").splitlines()]
    if len(blueprint) != 10000:
        raise SystemExit(f"blueprint must contain 10000 rows, found {len(blueprint)}")

    inventories = {}
    for language in LANGUAGES:
        project = projects[language]
        inventories[language] = git_paths(args.source_root / project["checkout"], project["commit"])

    rows = []
    notes = set()
    for index in range(10000):
        language = LANGUAGES[index % len(LANGUAGES)]
        for attempt in range(len(inventories[language])):
            row = row_for(
                index,
                language,
                blueprint[index],
                projects[language],
                inventories[language],
                attempt,
            )
            if row["note"] not in notes:
                break
        else:
            raise SystemExit(f"could not create a unique note at ml{index + 1:06d}")
        notes.add(row["note"])
        for fact in row["gold"]:
            if fact["subject"] not in row["note"] or fact["object"] not in row["note"]:
                raise SystemExit(f"ungrounded gold at {row['id']}: {fact}")
        rows.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"wrote {len(rows)} rows to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
