#!/usr/bin/env bash
# ==============================================================================
# Antigravity AI-OS v1.0 - One-Click Project Installer & Scaffolder (Bash/POSIX)
#
# Installs and injects the Antigravity Enterprise Kit (.agent/, rules, skills, neural-os)
# into any existing or new project workspace safely with zero friction.
# ==============================================================================
set -euo pipefail

TARGET_DIR="${1:-.}"
MODE="${2:-enterprise}"
FORCE="${FORCE:-false}"
SKIP_VERIFY="${SKIP_VERIFY:-false}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$(cd "${TARGET_DIR}" 2>/dev/null && pwd || echo "${TARGET_DIR}")"

echo "============================================================"
echo "     ANTIGRAVITY AI-OS: AUTONOMOUS PROJECT INSTALLER        "
echo "============================================================"
echo "[*] Kaynak Dizin : ${SCRIPT_DIR}"
echo "[*] Hedef Dizin  : ${TARGET_DIR}"
echo "[*] Kurulum Modu : ${MODE}"

# 1. Check Python
echo ""
echo "[*] Python sürümü kontrol ediliyor..."
if command -v python3 >/dev/null 2>&1; then
    PY_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PY_BIN="python"
else
    echo "Hata: Python 3 bulunamadı! Lütfen Python 3.10+ kurun." >&2
    exit 1
fi
echo "  [+] $(${PY_BIN} --version) algılandı."

# 2. Check Target Dir
mkdir -p "${TARGET_DIR}"
TARGET_AGENT="${TARGET_DIR}/.agent"

if [ -d "${TARGET_AGENT}" ] && [ "${FORCE}" != "true" ] && [ "${SCRIPT_DIR}" != "${TARGET_DIR}" ]; then
    echo "Uyarı: Hedef dizinde zaten bir '.agent/' klasörü mevcut!"
    echo "Üzerine yazmak için FORCE=true ./install.sh kullanın."
    exit 0
fi

# 3. Copy Components
if [ "${SCRIPT_DIR}" != "${TARGET_DIR}" ]; then
    echo ""
    echo "[*] .agent/ bileşenleri kopyalanıyor..."
    cp -r "${SCRIPT_DIR}/.agent" "${TARGET_DIR}/"
    if [ -d "${SCRIPT_DIR}/.github" ]; then
        cp -r "${SCRIPT_DIR}/.github" "${TARGET_DIR}/"
        echo "  [+] GitHub Actions CI/CD iş akışı aktarıldı."
    fi
    echo "  [+] Ajanlar, beceriler, kurallar ve nöral zihin kasası aktarıldı."
else
    echo ""
    echo "[*] Kaynak ve hedef aynı dizin, dosya kopyalama atlandı."
fi

# 4. Safely merge .gitignore
GITIGNORE="${TARGET_DIR}/.gitignore"
touch "${GITIGNORE}"
grep -q "__pycache__/" "${GITIGNORE}" || cat << 'EOF' >> "${GITIGNORE}"

# Antigravity AI-OS Runtime Ignores
__pycache__/
*.py[cod]
.pytest_cache/
.env
.env.*
!.env.example
EOF
echo "  [+] .gitignore kuralları güncellendi."

# 5. Verification
if [ "${SKIP_VERIFY}" != "true" ]; then
    echo ""
    echo "[*] Kurulum doğrulaması çalıştırılıyor..."
    (
        cd "${TARGET_DIR}"
        "${PY_BIN}" .agent/scripts/validate_kit.py
    )
    echo "  [+] Kit bütünlük ve kilit doğrulaması BAŞARILI!"
fi

echo ""
echo "============================================================"
echo " [BAŞARILI] Antigravity AI-OS kurulumu tamamlandı!"
echo "============================================================"
