#!/usr/bin/env bash

resolve_path()
{
    if [[ "$1" = /* ]]; then
        echo "$1"
    else
        echo "${REPO_DIR}/$1"
    fi
}

set -euo pipefail

# ============================================================
# Paths
# ============================================================

# Directory containing this script:
# <literature-qa>/scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Root directory of the literature-qa repository.
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# ============================================================
# Arguments
# ============================================================

usage()
{
    echo "Usage:"
    echo "  $0 [options] <literature-dir> <output-dir> <number-of-papers>"
    echo
    echo "Options:"
    echo "  -n, --newest-first  Process newer PDFs before older PDFs."
    echo "                      Falls back to modification time when creation time is unavailable."
    echo "  -e, --exclude-subdirectory NAME"
    echo "                      Skip PDFs below directories named NAME. May be repeated."
    echo "  -z, --zotero-storage"
    echo "                      Read Zotero item keys from PDF parent directories and add metadata."
    echo "  -h, --help          Show this help message."
    echo "  --                  Stop parsing options."
    echo
    echo "Example:"
    echo "  $0 tests/fixtures/literature .dtemp 3 --newest-first"
}

SORT_NEWEST_FIRST=false
ZOTERO_STORAGE=false
EXCLUDED_SUBDIRECTORIES=()
POSITIONAL_ARGUMENTS=()

parse_arguments()
{
    while (( $# > 0 )); do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            -n|--newest-first)
                SORT_NEWEST_FIRST=true
                ;;
            -e|--exclude-subdirectory)
                if (( $# < 2 )); then
                    echo "Error: $1 requires a subdirectory name." >&2
                    return 1
                fi
                EXCLUDED_SUBDIRECTORIES+=("$2")
                shift
                ;;
            -z|--zotero-storage)
                ZOTERO_STORAGE=true
                ;;
            --)
                shift
                POSITIONAL_ARGUMENTS+=("$@")
                break
                ;;
            -*)
                echo "Error: unknown option: $1" >&2
                usage >&2
                return 1
                ;;
            *)
                POSITIONAL_ARGUMENTS+=("$1")
                ;;
        esac
        shift
    done
}

parse_arguments "$@"
set -- "${POSITIONAL_ARGUMENTS[@]}"

if [[ $# -ne 3 ]]; then
    usage
    exit 1
fi

LITERATURE_DIR="$(resolve_path "$1")"
OUTPUT_DIR="$(resolve_path "$2")"
BATCH_SIZE="$3"

TEMPLATE="${REPO_DIR}/templates/summarize-literature.md"

# ============================================================
# Validate arguments
# ============================================================

if [[ ! -d "${LITERATURE_DIR}" ]]; then
    echo "Error: literature directory does not exist:"
    echo "  ${LITERATURE_DIR}"
    exit 1
fi

if [[ ! -f "${TEMPLATE}" ]]; then
    echo "Error: workflow template does not exist:"
    echo "  ${TEMPLATE}"
    exit 1
fi

if ! [[ "${BATCH_SIZE}" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: number-of-papers must be a positive integer."
    exit 1
fi

for excluded_subdirectory in "${EXCLUDED_SUBDIRECTORIES[@]}"; do
    if [[ -z "${excluded_subdirectory}" ||
          "${excluded_subdirectory}" == "." ||
          "${excluded_subdirectory}" == ".." ||
          "${excluded_subdirectory}" == */* ]]; then
        echo "Error: excluded subdirectory must be a single directory name:"
        echo "  ${excluded_subdirectory}"
        exit 1
    fi
done

# make the output directory
mkdir -p "${OUTPUT_DIR}"

# create a log file for this bash script
LOG_FILE="${OUTPUT_DIR}/summarize_batch.log"
if [[ -f "${LOG_FILE}" ]]; then
    rm "${LOG_FILE}"
fi

log()
{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "${LOG_FILE}"
}

echo >> "${LOG_FILE}"
log "============================================================"
log "Starting summarize batch"
log "Literature directory: ${LITERATURE_DIR}"
log "Output directory: ${OUTPUT_DIR}"
log "Batch size: ${BATCH_SIZE}"
if (( ${#EXCLUDED_SUBDIRECTORIES[@]} > 0 )); then
    log "Excluded subdirectories: ${EXCLUDED_SUBDIRECTORIES[*]}"
fi

if [[ "${SORT_NEWEST_FIRST}" == true ]]; then
    mapfile -d '' PDF_FILES < <(
        while IFS= read -r -d '' pdf_file; do
            creation_time="$(stat -c '%w' -- "${pdf_file}")"
            if [[ "${creation_time}" == "-" ]]; then
                creation_time="$(stat -c '%y' -- "${pdf_file}")"
            fi
            printf '%s\t%s\0' "${creation_time}" "${pdf_file}"
        done < <(
            find "${LITERATURE_DIR}" \
                -type f \
                -iname '*.pdf' \
                -print0
        ) |
        sort -z -t $'\t' -k1,1r -k2,2 |
        while IFS= read -r -d '' pdf_record; do
            printf '%s\0' "${pdf_record#*$'\t'}"
        done
    )
else
    mapfile -d '' PDF_FILES < <(
        find "${LITERATURE_DIR}" \
            -type f \
            -iname '*.pdf' \
            -print0 |
        sort -z
    )
fi

pdf_is_excluded()
{
    local pdf_relative_path="${1#"${LITERATURE_DIR}/"}"
    local pdf_parent_path="${pdf_relative_path%/*}"
    local -a directory_parts=()
    local directory_part
    local excluded_subdirectory

    if [[ "${pdf_parent_path}" == "${pdf_relative_path}" ]]; then
        return 1
    fi

    IFS='/' read -r -a directory_parts <<< "${pdf_parent_path}"
    for directory_part in "${directory_parts[@]}"; do
        for excluded_subdirectory in "${EXCLUDED_SUBDIRECTORIES[@]}"; do
            if [[ "${directory_part}" == "${excluded_subdirectory}" ]]; then
                EXCLUDED_SUBDIRECTORY_MATCH="${excluded_subdirectory}"
                return 0
            fi
        done
    done

    return 1
}

FILTERED_PDF_FILES=()
EXCLUDED_SUBDIRECTORY_MATCH=""
for pdf_file in "${PDF_FILES[@]}"; do
    if pdf_is_excluded "${pdf_file}"; then
        log "Skipping excluded subdirectory PDF: $(basename "${pdf_file}") (${EXCLUDED_SUBDIRECTORY_MATCH})"
        continue
    fi
    FILTERED_PDF_FILES+=("${pdf_file}")
done
PDF_FILES=("${FILTERED_PDF_FILES[@]}")

log "PDF files discovered: ${#PDF_FILES[@]}"

# ============================================================
# Select literature for this batch
# ============================================================

ELIGIBLE_PDF_FILES=()

for pdf_file in "${PDF_FILES[@]}"; do
    pdf_name="$(basename "${pdf_file}")"
    pdf_stem="${pdf_name%.*}"

    if [[ "${ZOTERO_STORAGE}" == true ]]; then
        zotero_key="$(basename "$(dirname "${pdf_file}")")"

        for summary_file in "${OUTPUT_DIR}"/*.md; do
            if [[ -f "${summary_file}" ]] && grep -Fqx "zotero_key: ${zotero_key}" "${summary_file}"; then
                log "Skipping existing Zotero item: ${pdf_name} (${zotero_key})"
                continue 2
            fi
        done
    else
        if compgen -G "${OUTPUT_DIR}/${pdf_stem}*.md" > /dev/null; then
            log "Skipping existing summary: ${pdf_name}"
            continue
        fi
    fi

    ELIGIBLE_PDF_FILES+=("${pdf_file}")
done

BATCH_FILES=("${ELIGIBLE_PDF_FILES[@]:0:BATCH_SIZE}")
log "PDF files selected for batch: ${#BATCH_FILES[@]}"

# ============================================================
# Summarize literature
# ============================================================

for batch_index in "${!BATCH_FILES[@]}"; do
    pdf_file="${BATCH_FILES[batch_index]}"
    pdf_name="$(basename "${pdf_file}")"
    zotero_instructions=""

    if [[ "${ZOTERO_STORAGE}" == true ]]; then
        zotero_key="$(basename "$(dirname "${pdf_file}")")"
        zotero_instructions=$(cat <<EOF

Write the resulting Markdown summary directly under:

${OUTPUT_DIR}

Begin the generated Markdown file with exactly this YAML front matter:

---
zotero_key: ${zotero_key}
doi: <DOI from the PDF>
pdf: ${pdf_name}
---

Replace the DOI placeholder with the DOI stated in the PDF. If the DOI cannot be verified, use an empty value for doi. Do not invent a DOI.
EOF
)
    fi

    log "============================================================"
    log "Loop entry: ${pdf_name}"
    log "Starting Codex: ${pdf_name}"

    # --------------------------------------------------------
    # Construct Codex prompt
    # --------------------------------------------------------

    prompt=$(cat <<EOF

Switch to the literature-qa folder.

Follow the workflow defined in:

${TEMPLATE}

Summarize the following literature:

${pdf_file}

Write the resulting Markdown summary under:

${OUTPUT_DIR}

${zotero_instructions}

Follow the workflow exactly.
EOF
)

    # --------------------------------------------------------
    # Run Codex
    # --------------------------------------------------------

    codex exec \
        -C "${REPO_DIR}" \
        --sandbox workspace-write \
        --add-dir "${LITERATURE_DIR}" \
        "${prompt}"

    codex_status=$?

    log "Codex finished: ${pdf_name}; exit code=${codex_status}"
    log "Batch progress: $((batch_index + 1))/${#BATCH_FILES[@]}"

done

# ============================================================
# Summary
# ============================================================
log "============================================================"
log "Batch complete. Papers processed: ${#BATCH_FILES[@]}"
log "============================================================"
