#!/usr/bin/env bash
# Install the ticktick-routine skill for Claude Code, Codex and/or OpenCode.
#
#   ./install.sh                 install for every agent found on this machine
#   ./install.sh --claude        only Claude Code   (~/.claude/skills)
#   ./install.sh --codex         only Codex         ($CODEX_HOME/skills, default ~/.codex/skills)
#   ./install.sh --opencode      only OpenCode      (~/.config/opencode/skills)
#   ./install.sh --claude-ai     build dist/ticktick-routine.skill for claude.ai (bundles your map)
#   ./install.sh --uninstall     remove the skill (your map in ~/.config/ticktick-routine stays)
#   ./install.sh --force         replace symlinked installs and install for OpenCode even if
#                                it already sees the Claude Code copy
#
# Your personal map lives outside the skill folder, in
# ${XDG_CONFIG_HOME:-~/.config}/ticktick-routine/map.md, so every agent shares it and
# reinstalling never erases it. A map left inside an old install is moved there first.
set -euo pipefail

SKILL="ticktick-routine"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO_DIR/skills/$SKILL"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/$SKILL"
MAP="$CONFIG_DIR/map.md"

CLAUDE_DIR="$HOME/.claude/skills/$SKILL"
CODEX_DIR="${CODEX_HOME:-$HOME/.codex}/skills/$SKILL"
OPENCODE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills/$SKILL"

want_claude=0 want_codex=0 want_opencode=0 want_claude_ai=0 uninstall=0 force=0

for arg in "$@"; do
  case "$arg" in
    --claude) want_claude=1 ;;
    --codex) want_codex=1 ;;
    --opencode) want_opencode=1 ;;
    --all) want_claude=1; want_codex=1; want_opencode=1 ;;
    --claude-ai) want_claude_ai=1 ;;
    --uninstall) uninstall=1 ;;
    --force) force=1 ;;
    -h|--help) sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $arg (see --help)" >&2; exit 1 ;;
  esac
done

say() { printf '%s\n' "$*"; }

if [ ! -f "$SRC/SKILL.md" ]; then
  say "Cannot find $SRC/SKILL.md — run this script from the repository root." >&2
  exit 1
fi

# No target flags: pick the agents that are present on this machine.
if [ $((want_claude + want_codex + want_opencode + want_claude_ai)) -eq 0 ]; then
  { [ -d "$HOME/.claude" ] || command -v claude >/dev/null 2>&1; } && want_claude=1
  { [ -d "${CODEX_HOME:-$HOME/.codex}" ] || command -v codex >/dev/null 2>&1; } && want_codex=1
  { [ -d "${XDG_CONFIG_HOME:-$HOME/.config}/opencode" ] || command -v opencode >/dev/null 2>&1; } && want_opencode=1
  if [ $((want_claude + want_codex + want_opencode)) -eq 0 ]; then
    say "No Claude Code, Codex or OpenCode found. Pass --claude, --codex or --opencode explicitly."
    exit 1
  fi
fi

# Keep a personal map from an older install that stored it inside the skill folder.
rescue_map() {
  local old="$1/references/ticktick-map.md"
  if [ -f "$old" ] && [ ! -f "$MAP" ]; then
    mkdir -p "$CONFIG_DIR"
    cp "$old" "$MAP"
    say "  • moved your map to $MAP"
  fi
}

install_to() {
  local label="$1" dest="$2"
  if [ -L "$dest" ] && [ "$force" -eq 0 ]; then
    say "• $label: $dest is a symlink (managed by \`npx skills\`?) — skipped, use --force to replace"
    return
  fi
  rescue_map "$dest"
  rm -rf "$dest"
  mkdir -p "$(dirname "$dest")"
  cp -R "$SRC" "$dest"
  rm -f "$dest/references/ticktick-map.md"
  find "$dest" -name '__pycache__' -prune -exec rm -rf {} +
  say "• $label: installed to $dest"
}

remove_from() {
  local label="$1" dest="$2"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    rescue_map "$dest"
    rm -rf "$dest"
    say "• $label: removed $dest"
  fi
}

if [ "$uninstall" -eq 1 ]; then
  [ $((want_claude + want_codex + want_opencode)) -eq 0 ] && { want_claude=1; want_codex=1; want_opencode=1; }
  [ "$want_claude" -eq 1 ] && remove_from "Claude Code" "$CLAUDE_DIR"
  [ "$want_codex" -eq 1 ] && remove_from "Codex" "$CODEX_DIR"
  [ "$want_opencode" -eq 1 ] && remove_from "OpenCode" "$OPENCODE_DIR"
  [ -f "$MAP" ] && say "Your map is kept at $MAP — delete it by hand if you no longer need it."
  exit 0
fi

say "Installing $SKILL"
[ "$want_claude" -eq 1 ] && install_to "Claude Code" "$CLAUDE_DIR"
[ "$want_codex" -eq 1 ] && install_to "Codex" "$CODEX_DIR"
if [ "$want_opencode" -eq 1 ]; then
  if [ -d "$CLAUDE_DIR" ] && [ "$force" -eq 0 ]; then
    say "• OpenCode: already sees $CLAUDE_DIR (OpenCode reads ~/.claude/skills) — no second copy needed"
  else
    install_to "OpenCode" "$OPENCODE_DIR"
  fi
fi

if [ "$want_claude_ai" -eq 1 ]; then
  out="$REPO_DIR/dist/$SKILL.skill"
  mkdir -p "$REPO_DIR/dist"
  python3 - "$SRC" "$MAP" "$out" <<'PY'
import sys, zipfile
from pathlib import Path
src, map_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(src.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts and f.name != "ticktick-map.md":
            z.write(f, Path(src.name) / f.relative_to(src))
    if map_path.is_file():
        z.write(map_path, Path(src.name) / "references" / "ticktick-map.md")
print(f"• claude.ai: built {out}" + (" (with your map)" if map_path.is_file() else " (no map yet — the skill will run setup in chat)"))
PY
  say "  Upload it in claude.ai → Settings → Capabilities → Skills. Keep it private: it contains your map."
fi

cat <<EOF

Next: connect the official TickTick MCP (https://mcp.ticktick.com/, sign-in via OAuth).
EOF
[ "$want_claude" -eq 1 ] && cat <<'EOF'
  Claude Code : claude mcp add --transport http --scope user ticktick https://mcp.ticktick.com/
                then run /mcp inside Claude Code and sign in
                (skip this if TickTick is already connected as a claude.ai connector)
EOF
[ "$want_codex" -eq 1 ] && cat <<'EOF'
  Codex       : codex mcp add ticktick --url https://mcp.ticktick.com/
                codex mcp login ticktick
EOF
[ "$want_opencode" -eq 1 ] && cat <<'EOF'
  OpenCode    : opencode mcp add ticktick --url https://mcp.ticktick.com/
                opencode mcp auth ticktick
EOF
if [ -f "$MAP" ]; then
  say ""
  say "Your map: $MAP"
else
  say ""
  say "First run: send any link to your agent — the skill maps your TickTick and asks 3–4 questions."
fi
