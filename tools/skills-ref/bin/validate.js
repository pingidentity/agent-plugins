#!/usr/bin/env node
/**
 * skills-ref validate — stub CLI entry point.
 *
 * Wraps scripts/validate_skills.py. Requires Python 3.11+.
 *
 * Usage:
 *   npx skills-ref validate           # from repo root
 *   npx skills-ref validate --root .  # explicit root
 */

const { execSync } = require("child_process");
const path = require("path");

const args = process.argv.slice(2);

if (args[0] === "validate" || args.length === 0) {
  // Find repo root by walking up until plugins/ is found
  let root = process.cwd();
  const fs = require("fs");
  while (root !== path.parse(root).root) {
    if (fs.existsSync(path.join(root, "plugins"))) break;
    root = path.dirname(root);
  }

  const script = path.join(root, "scripts", "validate_skills.py");
  if (!fs.existsSync(script)) {
    console.error("ERROR: scripts/validate_skills.py not found under " + root);
    console.error("Run from the repo root, or pass --root <path>.");
    process.exit(1);
  }

  try {
    execSync(`python3 "${script}" --root "${root}"`, { stdio: "inherit" });
  } catch (e) {
    process.exit(e.status || 1);
  }
} else if (args[0] === "--help" || args[0] === "-h") {
  console.log("skills-ref validate [--root <repo-root>]");
  console.log("");
  console.log("Validates all skill content against authoring rules:");
  console.log("  - SKILL.md frontmatter schema");
  console.log("  - SKILL.md ≤120 lines");
  console.log("  - name: matches directory name");
  console.log("  - Curated anchor frontmatter (title, product_family, capabilities, doc_type, status)");
  console.log("  - product_family matches directory path");
  console.log("  - Routing table cross-references resolve");
  console.log("  - index.json paths resolve");
  console.log("  - No forbidden URLs (/r/en-us/, apps.pingone.com, /latest/ AIC)");
  process.exit(0);
} else {
  console.error("Unknown command: " + args[0]);
  console.error("Usage: skills-ref validate");
  process.exit(1);
}
